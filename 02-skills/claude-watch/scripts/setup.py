"""Cross-platform preflight + installer for claude-watch.

Exit codes (read by SKILL.md):
    0  ready
    2  needs_install
    3  needs_key
    4  needs_install_and_key
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

CONFIG_DIR = Path.home() / ".config" / "claude-watch"
ENV_PATH = CONFIG_DIR / ".env"
LIBRARY_ROOT = Path.home() / "claude-watch" / "library"
REQUIRED_BINS = ("ffmpeg", "ffprobe", "yt-dlp")


def _which(name: str) -> Optional[str]:
    return shutil.which(name)


def _read_env() -> dict[str, str]:
    """Read CONFIG_DIR/.env if present. Falls back to process env if file absent."""
    env: dict[str, str] = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("GROQ_API_KEY", "OPENAI_API_KEY", "SETUP_COMPLETE"):
        if k in os.environ and not env.get(k):
            env[k] = os.environ[k]
    return env


def status_for() -> dict:
    missing = [b for b in REQUIRED_BINS if not _which(b)]
    env = _read_env()
    has_key = bool(env.get("GROQ_API_KEY") or env.get("OPENAI_API_KEY"))
    if missing and not has_key:
        status = "needs_install_and_key"
    elif missing:
        status = "needs_install"
    elif not has_key:
        status = "needs_key"
    else:
        status = "ready"
    return {
        "status": status,
        "missing_binaries": missing,
        "has_api_key": has_key,
        "whisper_backend": (
            "groq" if env.get("GROQ_API_KEY")
            else "openai" if env.get("OPENAI_API_KEY")
            else None
        ),
        "config_file": str(ENV_PATH),
        "platform": platform.system().lower(),
        "first_run": not env.get("SETUP_COMPLETE"),
    }


def exit_code_for(status: str) -> int:
    return {"ready": 0, "needs_install": 2, "needs_key": 3, "needs_install_and_key": 4}[status]


def _scaffold_env() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    LIBRARY_ROOT.mkdir(parents=True, exist_ok=True)
    if ENV_PATH.exists():
        return
    ENV_PATH.write_text(
        "# claude-watch credentials\n"
        "# Get a Groq key (preferred — cheaper, faster): https://console.groq.com/keys\n"
        "# Or OpenAI: https://platform.openai.com/api-keys\n"
        "# GROQ_API_KEY=\n"
        "# OPENAI_API_KEY=\n"
        "SETUP_COMPLETE=false\n"
    )
    os.chmod(ENV_PATH, 0o600)


def _print_install_instructions() -> None:
    sysname = platform.system().lower()
    missing = [b for b in REQUIRED_BINS if not _which(b)]
    if not missing:
        return
    if sysname == "darwin":
        # macOS — try brew automatically
        if _which("brew"):
            print(f"Installing missing tools via brew: {', '.join(missing)}", file=sys.stderr)
            subprocess.run(["brew", "install", *missing], check=False)
            return
        print("Homebrew not found. Install brew, then re-run setup.py.", file=sys.stderr)
    elif sysname == "linux":
        print("Run one of:", file=sys.stderr)
        print(f"  sudo apt-get install -y {' '.join(missing)}", file=sys.stderr)
        print(f"  sudo dnf install -y {' '.join(missing)}", file=sys.stderr)
        print(f"  pipx install yt-dlp  # (if 'yt-dlp' isn't in apt)", file=sys.stderr)
    elif sysname == "windows":
        print("Run:", file=sys.stderr)
        for b in missing:
            if b == "yt-dlp":
                print(f"  pip install --user yt-dlp", file=sys.stderr)
            else:
                print(f"  winget install --id Gyan.FFmpeg", file=sys.stderr)
    else:
        print(f"Unsupported platform '{sysname}'. Install manually: {', '.join(missing)}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="Silent on success; exit code reflects state")
    p.add_argument("--json", action="store_true", help="Emit structured JSON status")
    args = p.parse_args(argv)
    s = status_for()
    if args.json:
        print(json.dumps(s))
        return exit_code_for(s["status"])
    if args.check:
        return exit_code_for(s["status"])
    # Full install / scaffold flow
    _scaffold_env()
    _print_install_instructions()
    s2 = status_for()
    return exit_code_for(s2["status"])


if __name__ == "__main__":
    raise SystemExit(main())
