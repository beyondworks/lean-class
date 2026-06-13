"""Stdlib HTTP clients for Groq and OpenAI Whisper APIs."""
from __future__ import annotations

import json
import mimetypes
import uuid
from pathlib import Path
from typing import Optional
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen


GROQ_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
GROQ_MODEL = "whisper-large-v3"
OPENAI_URL = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_MODEL = "whisper-1"


class WhisperError(Exception):
    pass


def pick_backend(
    *,
    groq_key: Optional[str],
    openai_key: Optional[str],
    forced: Optional[str],
) -> Optional[str]:
    """Return 'groq', 'openai', or None.

    Forced backend wins iff its key is present. Otherwise prefer Groq, then OpenAI.
    """
    if forced == "groq":
        return "groq" if groq_key else None
    if forced == "openai":
        return "openai" if openai_key else None
    if groq_key:
        return "groq"
    if openai_key:
        return "openai"
    return None


def _build_multipart(audio: Path, model: str) -> tuple[bytes, str]:
    """Encode a multipart/form-data body for the audio + model fields."""
    boundary = f"----whisper-{uuid.uuid4().hex}"
    crlf = b"\r\n"
    parts: list[bytes] = []
    # Field: model
    parts.append(f"--{boundary}".encode())
    parts.append(b'Content-Disposition: form-data; name="model"')
    parts.append(b"")
    parts.append(model.encode())
    # Field: response_format = verbose_json (gives us segments with timestamps)
    parts.append(f"--{boundary}".encode())
    parts.append(b'Content-Disposition: form-data; name="response_format"')
    parts.append(b"")
    parts.append(b"verbose_json")
    # Field: file
    mime = mimetypes.guess_type(audio.name)[0] or "application/octet-stream"
    parts.append(f"--{boundary}".encode())
    parts.append(
        f'Content-Disposition: form-data; name="file"; filename="{audio.name}"'.encode()
    )
    parts.append(f"Content-Type: {mime}".encode())
    parts.append(b"")
    parts.append(audio.read_bytes())
    parts.append(f"--{boundary}--".encode())
    parts.append(b"")
    body = crlf.join(parts)
    return body, boundary


def _post(url: str, audio: Path, *, model: str, api_key: str) -> list[dict]:
    """POST audio + model + response_format=verbose_json to a Whisper endpoint.

    Returns: [{"t_start": float, "t_end": float, "text": str}, ...]
    Raises: WhisperError on any network, HTTP, JSON, or response-shape failure.
    """
    body, boundary = _build_multipart(audio, model)
    req = Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        },
    )
    try:
        with urlopen(req, timeout=300) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        segs = payload.get("segments") or []
        return [
            {
                "t_start": float(s["start"]),
                "t_end": float(s["end"]),
                "text": s["text"].strip(),
            }
            for s in segs
        ]
    except HTTPError as e:
        # Surface the API's JSON error body so users see "Invalid API Key" etc.
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        raise WhisperError(f"HTTP {e.code} {e.reason}: {detail}") from e
    except Exception as e:
        # Network, JSON parse, missing keys on segments — all surface as WhisperError.
        raise WhisperError(str(e)) from e


def transcribe_groq(audio: Path, *, api_key: str) -> list[dict]:
    return _post(GROQ_URL, audio, model=GROQ_MODEL, api_key=api_key)


def transcribe_openai(audio: Path, *, api_key: str) -> list[dict]:
    return _post(OPENAI_URL, audio, model=OPENAI_MODEL, api_key=api_key)
