"""Slug, cache, and manifest helpers for claude-watch's persistent library."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LIBRARY_ROOT = Path.home() / "claude-watch" / "library"

_SLUG_BAD = re.compile(r"[^a-z0-9]+")


def sanitize_title(title: str) -> str:
    """Lowercase, replace any non-[a-z0-9] run with a single dash, strip ends."""
    s = _SLUG_BAD.sub("-", title.lower()).strip("-")
    return s or "untitled"


def slug_for(meta: dict) -> str:
    """`YYYY-MM-DD-<sanitized-title>-<short-hash>` where hash = sha1(source + focus)[:4]."""
    date = meta.get("watched_at") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = sanitize_title(meta.get("title", "untitled"))
    src = meta.get("source", "")
    focus = meta.get("focus_range_str", "")
    h = hashlib.sha1((src + "|" + focus).encode("utf-8")).hexdigest()[:4]
    return f"{date}-{title}-{h}"


def cache_lookup(slug: str, source_hash: str) -> Path | None:
    """Return the library dir if it exists and meta.source_hash matches; else None."""
    d = LIBRARY_ROOT / slug
    meta_path = d / "meta.json"
    if not meta_path.exists():
        return None
    try:
        data = json.loads(meta_path.read_text())
    except json.JSONDecodeError:
        return None
    return d if data.get("source_hash") == source_hash else None


def write_manifest(
    *,
    path: Path,
    meta: dict[str, Any],
    scenes: list[dict[str, Any]],
    frames: list[dict[str, Any]],
    transcript_path: str,
    focus_range: tuple[float, float] | None,
) -> None:
    """Write manifest.json that Claude consumes."""
    payload = {
        "meta": meta,
        "scenes": scenes,
        "frames": frames,
        "transcript_path": transcript_path,
        "focus_range": (
            None
            if focus_range is None
            else {"start_s": focus_range[0], "end_s": focus_range[1]}
        ),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
