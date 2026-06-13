#!/usr/bin/env python3
"""Analyze a Whisper word-timestamps JSON and propose cuts for screenstudio-cut.

Outputs:
  - <output>      : JSON with {silences, fillers, prefix_repeats, words, segments}
  - <report>      : human-readable text report
  - words.json    : flat word list (sibling of <output>)

Usage:
  python3 analyze.py \
    --whisper-json mic.json \
    --silence-min 1.8 \
    --silence-keep-breath 0.4 \
    --prefix-min-words 2 \
    --output cuts_candidates.json \
    --report analysis_report.txt
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

# Korean fillers: only cut when isolated by a gap on at least one side.
FILLERS = {
    "어", "음", "그", "그..", "어..", "음..",
    "이제", "막", "뭐", "근데", "약간", "하여튼", "자", "아",
}

WORD_PUNCT_RX = re.compile(r"[\s.,!?…]+")


def clean(w: str) -> str:
    return WORD_PUNCT_RX.sub("", w)


def flatten(segments):
    out = []
    for si, s in enumerate(segments):
        for w in s.get("words", []):
            out.append({
                "start": float(w["start"]),
                "end": float(w["end"]),
                "word": w["word"].strip(),
                "key": clean(w["word"]),
                "seg": si,
            })
    return out


def find_silences(words, min_gap_s, keep_breath_s):
    """gaps between word i-1.end and word i.start >= min_gap → cut [end+breath, start]"""
    res = []
    for i in range(1, len(words)):
        gap = words[i]["start"] - words[i - 1]["end"]
        if gap >= min_gap_s:
            cut_start = round(words[i - 1]["end"] + keep_breath_s, 3)
            cut_end = round(words[i]["start"], 3)
            if cut_end - cut_start <= 0:
                continue
            ctx_b = " ".join(w["word"] for w in words[max(0, i - 3):i])
            ctx_a = " ".join(w["word"] for w in words[i:i + 3])
            res.append({
                "type": "silence",
                "gap_s": round(gap, 3),
                "cut_start": cut_start,
                "cut_end": cut_end,
                "ctx_before": ctx_b,
                "ctx_after": ctx_a,
                "reason": f"SIL {gap:.2f}s (kept {keep_breath_s}s breath)",
            })
    return res


def find_fillers(words):
    """Standalone fillers with at least one side gap >= 0.2s."""
    res = []
    for i, w in enumerate(words):
        token = w["word"].rstrip(".,?!… ")
        if token not in FILLERS:
            continue
        gap_b = (w["start"] - words[i - 1]["end"]) if i > 0 else 0
        gap_a = (words[i + 1]["start"] - w["end"]) if i + 1 < len(words) else 0
        if gap_b < 0.2 and gap_a < 0.2:
            continue
        ctx = " ".join(ww["word"] for ww in words[max(0, i - 3):i + 4])
        res.append({
            "type": "filler",
            "word": token,
            "cut_start": round(w["start"], 3),
            "cut_end": round(w["end"], 3),
            "gap_before_s": round(gap_b, 3),
            "gap_after_s": round(gap_a, 3),
            "ctx": ctx,
            "reason": f"FILLER '{token}' (gap_before {gap_b:.2f}s, gap_after {gap_a:.2f}s)",
        })
    return res


def find_prefix_repeats(words, min_words=2, max_gap_s=8.0, max_lookahead=30):
    """Detect candidate false-start patterns: same N-word prefix repeats within max_gap_s.

    HIGH FALSE-POSITIVE RATE. Empirically ~60% of candidates are legitimate phrase
    reuse, not stutters. Caller MUST inspect ctx_first/ctx_second before cutting.

    True false-start signals:
      - First instance ends with '...' or is mid-word truncated
      - Silence ≥ 1.0s between instances
      - Second instance restarts the same sentence (not just shares an opening phrase)

    Returns list of {first_word_idx, second_word_idx, prefix, gap_s, ...}.
    Caller decides whether to cut [first_start, second_start] (the safe choice).
    Skips matches where any prefix word is single-character (likely common particle)."""
    res = []
    seen = set()
    for i in range(len(words) - min_words * 2):
        keys_i = tuple(words[i + k]["key"] for k in range(min_words))
        if not all(keys_i):
            continue
        if any(len(k) < 2 for k in keys_i):
            continue
        end_first = words[i + min_words - 1]["end"]
        for j in range(i + min_words, min(i + max_lookahead, len(words) - min_words + 1)):
            keys_j = tuple(words[j + k]["key"] for k in range(min_words))
            gap = words[j]["start"] - end_first
            if gap > max_gap_s:
                break
            if keys_i == keys_j and gap > 0.2:
                pair = (i, j)
                if pair in seen:
                    continue
                seen.add(pair)
                ctx_first = " ".join(ww["word"] for ww in words[max(0, i - 2):i + min_words + 2])
                ctx_second = " ".join(ww["word"] for ww in words[max(0, j - 2):j + min_words + 2])
                res.append({
                    "type": "prefix_repeat",
                    "first_start": round(words[i]["start"], 3),
                    "first_end": round(end_first, 3),
                    "second_start": round(words[j]["start"], 3),
                    "gap_s": round(gap, 3),
                    "prefix": " ".join(words[i + k]["word"] for k in range(min_words)),
                    "ctx_first": ctx_first,
                    "ctx_second": ctx_second,
                    "suggested_cut": {
                        "start": round(words[i]["start"], 3),
                        "end":   round(words[j]["start"], 3),
                    },
                    "reason": f"PREFIX_REPEAT '{' '.join(words[i+k]['word'] for k in range(min_words))}'",
                })
                break
    return res


def write_report(report_path, data, params):
    lines = []
    L = lines.append
    L(f"# screenstudio-cut analysis")
    L(f"")
    L(f"params: silence-min={params['silence_min']}s "
      f"keep-breath={params['silence_keep_breath']}s "
      f"prefix-min-words={params['prefix_min_words']}")
    L(f"audio length covered: {data['duration_s']:.2f}s")
    L(f"segments: {data['n_segments']}, words: {data['n_words']}")
    L(f"")
    L(f"## 1) Long silences (>= {params['silence_min']}s) — {len(data['silences'])} found")
    for s in data["silences"]:
        L(f"  CUT [{s['cut_start']:7.2f} → {s['cut_end']:7.2f}]  gap {s['gap_s']:.2f}s  "
          f"…{s['ctx_before']} ▮▮ {s['ctx_after']}…")
    L(f"")
    L(f"## 2) Standalone fillers — {len(data['fillers'])} candidates (review before cutting)")
    for f in data["fillers"]:
        L(f"  CUT [{f['cut_start']:7.2f} → {f['cut_end']:7.2f}]  '{f['word']}'  ctx: …{f['ctx']}…")
    L(f"")
    L(f"## 3) Prefix repetitions (likely false starts) — {len(data['prefix_repeats'])}")
    for p in data["prefix_repeats"]:
        sc = p["suggested_cut"]
        L(f"  CUT [{sc['start']:7.2f} → {sc['end']:7.2f}]  prefix '{p['prefix']}' gap {p['gap_s']:.2f}s")
        L(f"    first : …{p['ctx_first']}…")
        L(f"    second: …{p['ctx_second']}…")
    L(f"")
    L(f"## 4) NOT detected by this analyzer (require manual transcript review):")
    L(f"  - Sentence-level repetition across a long pause")
    L(f"  - Mid-word stutters that Whisper transcribes as a single token")
    L(f"  - Topic restart with rephrasing (different words, same meaning)")
    L(f"")
    L(f"## 5) Full transcript (segment level)")
    for s in data["segments"]:
        L(f"  [{s['start']:7.2f} → {s['end']:7.2f}]  {s['text'].strip()}")
    Path(report_path).write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--whisper-json", required=True)
    ap.add_argument("--silence-min", type=float, default=1.8)
    ap.add_argument("--silence-keep-breath", type=float, default=0.4)
    ap.add_argument("--prefix-min-words", type=int, default=2)
    ap.add_argument("--output", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    wj = json.loads(Path(args.whisper_json).read_text(encoding="utf-8"))
    segs = wj.get("segments") or []
    if not segs:
        print("ERROR: Whisper JSON has no segments", file=sys.stderr)
        sys.exit(2)
    if not segs[0].get("words"):
        print("ERROR: Whisper JSON lacks word_timestamps. Re-run with --word_timestamps True.",
              file=sys.stderr)
        sys.exit(3)

    words = flatten(segs)
    silences = find_silences(words, args.silence_min, args.silence_keep_breath)
    fillers = find_fillers(words)
    prefix_repeats = find_prefix_repeats(words, args.prefix_min_words)

    duration = max((s["end"] for s in segs), default=0.0)
    out_data = {
        "language": wj.get("language"),
        "duration_s": duration,
        "n_segments": len(segs),
        "n_words": len(words),
        "params": {
            "silence_min": args.silence_min,
            "silence_keep_breath": args.silence_keep_breath,
            "prefix_min_words": args.prefix_min_words,
        },
        "silences": silences,
        "fillers": fillers,
        "prefix_repeats": prefix_repeats,
        "segments": [
            {"start": s["start"], "end": s["end"], "text": s["text"]}
            for s in segs
        ],
    }
    Path(args.output).write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(args.output).with_name("words.json").write_text(
        json.dumps(words, ensure_ascii=False, indent=0), encoding="utf-8"
    )
    write_report(args.report, out_data, out_data["params"])

    print(f"silences        : {len(silences)}")
    print(f"fillers         : {len(fillers)}")
    print(f"prefix_repeats  : {len(prefix_repeats)}")
    print(f"output          : {args.output}")
    print(f"report          : {args.report}")
    print(f"words           : {Path(args.output).with_name('words.json')}")


if __name__ == "__main__":
    main()
