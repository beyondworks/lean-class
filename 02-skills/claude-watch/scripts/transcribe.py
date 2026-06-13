"""Caption extraction (VTT) + dedupe + speaker-break heuristic + Whisper orchestration."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Optional

from scripts import whisper

_TS_RX = re.compile(
    r"(?:(\d+):)?(\d{1,2}):(\d{2})(?:[.,](\d{1,3}))?\s*-->\s*"
    r"(?:(\d+):)?(\d{1,2}):(\d{2})(?:[.,](\d{1,3}))?"
)


def _ts_to_s(h: str | None, m: str, s: str, ms: str | None) -> float:
    return (int(h) if h else 0) * 3600 + int(m) * 60 + int(s) + (int(ms) / 1000.0 if ms else 0.0)


def parse_vtt(text: str) -> list[dict]:
    """Parse a WebVTT file into cues. Strips formatting tags like <c.colorXXXX>."""
    cues: list[dict] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = _TS_RX.search(lines[i])
        if not m:
            i += 1
            continue
        t_start = _ts_to_s(m.group(1), m.group(2), m.group(3), m.group(4))
        t_end = _ts_to_s(m.group(5), m.group(6), m.group(7), m.group(8))
        i += 1
        text_lines: list[str] = []
        while i < len(lines) and lines[i].strip():
            text_lines.append(re.sub(r"<[^>]+>", "", lines[i]).strip())
            i += 1
        joined = " ".join(t for t in text_lines if t).strip()
        if joined:
            cues.append({"t_start": t_start, "t_end": t_end, "text": joined})
    return cues


_ROLLING_OVERLAP_MIN = 10  # chars of suffix/prefix overlap to count as a rolling caption


def dedupe_cues(cues: list[dict]) -> list[dict]:
    """Collapse adjacent rolling/duplicate cues from VTT (especially YouTube auto-caps).

    Handles four patterns:
    1. Identical text → extend prev's t_end.
    2. `c.text` starts with `prev.text` (rolling extension) → replace prev's text with c's longer text.
    3. `prev.text` ends with `c.text` (c is a tail already shown) → extend prev's t_end, drop c.
    4. Suffix of prev matches prefix of c (>= 10 chars) → emit only the new tail of c.
    Otherwise keep both as separate cues.
    """
    out: list[dict] = []
    for c in cues:
        if not out:
            out.append(dict(c))
            continue
        prev = out[-1]
        # 1. Identical
        if prev["text"] == c["text"]:
            prev["t_end"] = max(prev["t_end"], c["t_end"])
            continue
        # 2. Rolling extension: c is the longer continuation of prev
        if len(c["text"]) > len(prev["text"]) and c["text"].startswith(prev["text"]):
            prev["t_end"] = c["t_end"]
            prev["text"] = c["text"]
            continue
        # 3. c is already contained at the tail of prev
        if prev["text"].endswith(c["text"]):
            prev["t_end"] = max(prev["t_end"], c["t_end"])
            continue
        # 4. Suffix of prev = prefix of c → emit only the new tail
        max_check = min(len(prev["text"]), len(c["text"]))
        overlap = 0
        for k in range(max_check, _ROLLING_OVERLAP_MIN - 1, -1):
            if prev["text"][-k:] == c["text"][:k]:
                overlap = k
                break
        if overlap > 0:
            tail = c["text"][overlap:].lstrip()
            if tail:
                out.append({"t_start": c["t_start"], "t_end": c["t_end"], "text": tail})
            else:
                prev["t_end"] = max(prev["t_end"], c["t_end"])
            continue
        # 5. Unrelated → keep both
        out.append(dict(c))
    return out


def insert_speaker_breaks(cues: list[dict], threshold_s: float = 2.0) -> list[dict]:
    """Mark cues that follow a pause > threshold as a speaker_break.

    This is a heuristic — it doesn't identify WHO is speaking, just that
    something changed. Useful for interviews/panels where downstream notes
    benefit from a section boundary.
    """
    out: list[dict] = []
    for i, c in enumerate(cues):
        marked = dict(c)
        if i > 0:
            gap = c["t_start"] - cues[i - 1]["t_end"]
            marked["speaker_break"] = gap > threshold_s
        else:
            marked["speaker_break"] = False
        out.append(marked)
    return out


def slice_to_window(
    cues: list[dict], start_s: Optional[float], end_s: Optional[float]
) -> list[dict]:
    """Keep only cues that overlap the [start, end] window. None bounds = open."""
    if start_s is None and end_s is None:
        return cues
    s = start_s if start_s is not None else float("-inf")
    e = end_s if end_s is not None else float("inf")
    return [c for c in cues if c["t_end"] >= s and c["t_start"] <= e]


def fetch_native_captions(video_url: str, work_dir: Path) -> Optional[Path]:
    """Try to pull native + auto-generated subs via yt-dlp. Returns the .vtt path or None."""
    work_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", "en.*",
        "--sub-format", "vtt",
        "-o", str(work_dir / "%(id)s.%(ext)s"),
        video_url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return None
    vtts = sorted(work_dir.glob("*.vtt"))
    return vtts[0] if vtts else None


def extract_audio_for_whisper(video: Path, out_audio: Path) -> None:
    """Mono 16kHz audio for Whisper. ~0.5MB/min — well under the 25MB limit for ~50 min."""
    out_audio.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-nostdin",
            "-i", str(video),
            "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k",
            str(out_audio),
        ],
        check=True,
    )


def transcribe_via_whisper(
    audio: Path,
    *,
    backend: str,
    groq_key: Optional[str],
    openai_key: Optional[str],
) -> list[dict]:
    if backend == "groq":
        if not groq_key:
            raise whisper.WhisperError("Groq backend selected but GROQ_API_KEY is unset")
        return whisper.transcribe_groq(audio, api_key=groq_key)
    if backend == "openai":
        if not openai_key:
            raise whisper.WhisperError("OpenAI backend selected but OPENAI_API_KEY is unset")
        return whisper.transcribe_openai(audio, api_key=openai_key)
    raise whisper.WhisperError(f"Unknown backend: {backend}")
