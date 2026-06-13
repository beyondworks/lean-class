"""yt-dlp download wrapper + local file linker."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path


def download_video(url: str, out_dir: Path, *, basename: str = "video") -> Path:
    """Download to `out_dir/<basename>.<ext>` via yt-dlp. Returns the downloaded file."""
    out_dir.mkdir(parents=True, exist_ok=True)
    template = str(out_dir / f"{basename}.%(ext)s")
    cmd = [
        "yt-dlp",
        "--no-playlist",
        "-f", "best[ext=mp4]/best",
        "-o", template,
        url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {proc.stderr.strip()}")
    matches = sorted(out_dir.glob(f"{basename}.*"))
    if not matches:
        raise RuntimeError(f"yt-dlp returned 0 but no {basename}.* file in {out_dir}")
    return matches[0]


def copy_local(src: Path, out_dir: Path, *, basename: str = "video") -> Path:
    """For local sources, symlink (cheap, no copy) into out_dir/<basename>.<ext>.
    Falls back to a regular file copy if symlink fails."""
    out_dir.mkdir(parents=True, exist_ok=True)
    src = src.expanduser().resolve()
    dst = out_dir / f"{basename}{src.suffix}"
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    try:
        os.symlink(src, dst)
    except OSError:
        dst.write_bytes(src.read_bytes())
    return dst
