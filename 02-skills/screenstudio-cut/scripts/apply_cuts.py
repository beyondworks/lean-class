#!/usr/bin/env python3
"""Apply a list of cuts to a Screen Studio bundle's project.json.

Behavior:
  1. Refuses to run if Screen Studio is currently running (auto-save would clobber edits)
  2. Backs up the bundle's project.json (caller is expected to back up the whole bundle separately;
     this script also keeps a project.json-only backup as a second safety net)
  3. Loads project.json, finds scenes[0].slices (must currently contain a single slice — this skill
     is designed for fresh recordings; passing a previously-cut bundle works too but cuts are
     applied against the union of existing kept ranges)
  4. Sorts and merges overlapping cut ranges
  5. Splits the original kept range(s) into new slices that exclude the cut regions
  6. Writes back, JSON-validates by reloading
  7. Prints original/output durations, slice count, zoom overlap report

Usage:
  python3 apply_cuts.py --bundle "<...>.screenstudio" --cuts cuts.json [--force-app-running]

cuts.json schema:
  {
    "cuts": [
      {"start_ms": 79140, "end_ms": 88560, "reason": "FS: ..."},
      ...
    ]
  }
  OR a flat list:
  [{"start_ms": ..., "end_ms": ..., "reason": "..."}, ...]
"""
from __future__ import annotations
import argparse, json, random, shutil, string, subprocess, sys, time
from pathlib import Path


def is_screenstudio_running() -> bool:
    try:
        r = subprocess.run(["pgrep", "-x", "Screen Studio"], capture_output=True, text=True)
        return r.returncode == 0 and r.stdout.strip() != ""
    except FileNotFoundError:
        return False


def gen_id(rng: random.Random, n: int = 10) -> str:
    return "".join(rng.choices(string.ascii_letters + string.digits, k=n))


def load_cuts(path: Path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict) and "cuts" in raw:
        raw = raw["cuts"]
    if not isinstance(raw, list):
        raise ValueError("cuts file must be a list or {cuts: [...]}")
    out = []
    for c in raw:
        s = float(c["start_ms"])
        e = float(c["end_ms"])
        if e <= s:
            raise ValueError(f"invalid cut: end<=start {c}")
        reason = c.get("reason", "")
        out.append((s, e, reason))
    out.sort(key=lambda x: x[0])
    # merge overlaps
    merged = []
    for s, e, why in out:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e), merged[-1][2] + " + " + why)
        else:
            merged.append((s, e, why))
    return merged


def output_time_at(source_ms: float, slices) -> float:
    """Project a sourceMs onto the output timeline of the given slice list."""
    out = 0.0
    for sl in slices:
        s, e = sl["sourceStartMs"], sl["sourceEndMs"]
        if source_ms < s:
            return out
        if source_ms <= e:
            return out + (source_ms - s)
        out += (e - s)
    return out


def check_zoom_overlap(zoom_ranges, cuts):
    overlaps = []
    for z in zoom_ranges or []:
        zs, ze = z["startTime"], z["endTime"]
        for s, e, why in cuts:
            if zs < e and s < ze:
                overlaps.append({"zoom_id": z["id"], "zoom": [zs, ze], "cut": [s, e], "reason": why})
    return overlaps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--cuts", required=True)
    ap.add_argument("--force-app-running", action="store_true",
                    help="Apply even if Screen Studio is running (DANGEROUS — auto-save may clobber)")
    ap.add_argument("--zoom-policy", choices=["abort", "drop", "keep"], default="abort",
                    help="abort = stop on overlap; drop = remove overlapping zooms; keep = leave them (may break)")
    args = ap.parse_args()

    bundle = Path(args.bundle)
    if not bundle.is_dir():
        print(f"ERROR: bundle not found: {bundle}", file=sys.stderr); sys.exit(2)
    project = bundle / "project.json"
    if not project.is_file():
        print(f"ERROR: project.json not found in bundle", file=sys.stderr); sys.exit(2)

    if is_screenstudio_running() and not args.force_app_running:
        print("ERROR: Screen Studio is running. Quit it (⌘Q) before applying cuts.", file=sys.stderr)
        print("       Or pass --force-app-running (NOT recommended).", file=sys.stderr)
        sys.exit(4)

    cuts = load_cuts(Path(args.cuts))
    if not cuts:
        print("No cuts to apply."); sys.exit(0)

    # Per-file backup of project.json (in addition to whatever bundle-level backup the caller made)
    ts = time.strftime("%Y%m%dT%H%M%S")
    project_bak = project.with_suffix(f".json.backup-{ts}")
    shutil.copy2(project, project_bak)

    data = json.loads(project.read_text(encoding="utf-8"))
    scenes = data["json"]["scenes"]
    if not scenes:
        print("ERROR: project.json has no scenes", file=sys.stderr); sys.exit(2)
    scene = scenes[0]

    # Compute existing kept ranges from current slices
    existing_ranges = [(sl["sourceStartMs"], sl["sourceEndMs"]) for sl in scene["slices"]]
    if not existing_ranges:
        print("ERROR: scene has no slices", file=sys.stderr); sys.exit(2)
    src_start = existing_ranges[0][0]
    src_end   = existing_ranges[-1][1]

    # Zoom overlap check
    overlaps = check_zoom_overlap(scene.get("zoomRanges", []), cuts)
    if overlaps:
        if args.zoom_policy == "abort":
            print("ERROR: cuts overlap with zoomRanges (--zoom-policy=abort).", file=sys.stderr)
            for o in overlaps:
                print(f"  zoom {o['zoom_id']} {o['zoom']} ↔ cut {o['cut']}  ({o['reason']})", file=sys.stderr)
            sys.exit(5)
        elif args.zoom_policy == "drop":
            keep_zooms = []
            dropped = []
            for z in scene.get("zoomRanges", []):
                if any(o["zoom_id"] == z["id"] for o in overlaps):
                    dropped.append(z["id"])
                else:
                    keep_zooms.append(z)
            scene["zoomRanges"] = keep_zooms
            print(f"WARN: dropped {len(dropped)} overlapping zoom(s): {dropped}")

    # Subtract cuts from existing kept ranges
    def subtract(ranges, cuts):
        out = []
        for rs, re_ in ranges:
            cur = rs
            for cs, ce, _ in cuts:
                if ce <= cur or cs >= re_: continue
                if cs > cur:
                    out.append((cur, min(cs, re_)))
                cur = max(cur, ce)
                if cur >= re_: break
            if cur < re_:
                out.append((cur, re_))
        return out

    new_ranges = subtract(existing_ranges, cuts)
    if not new_ranges:
        print("ERROR: cuts cover the entire recording — nothing left.", file=sys.stderr)
        shutil.copy2(project_bak, project)
        sys.exit(6)

    # Build new slices using common fields from the FIRST existing slice
    template = dict(scene["slices"][0])
    template_keep_keys = ("timeScale","volume","systemAudioVolume","hideCursor",
                          "disableSmoothMouseMovement","externalDeviceAudioVolume")
    common = {k: template[k] for k in template_keep_keys if k in template}

    rng = random.Random(int(time.time() * 1000) ^ 0xC0FFEE)
    new_slices = []
    for s, e in new_ranges:
        sl = dict(common)
        sl["id"] = gen_id(rng)
        sl["sourceStartMs"] = s
        sl["sourceEndMs"]   = e
        new_slices.append(sl)
    scene["slices"] = new_slices

    # Write atomically
    tmp = project.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    json.loads(tmp.read_text(encoding="utf-8"))  # validate round-trip
    tmp.replace(project)

    # Report
    orig_dur = (src_end - src_start) / 1000
    final_dur = sum((sl["sourceEndMs"] - sl["sourceStartMs"]) for sl in new_slices) / 1000
    cut_total = sum(e - s for s, e, _ in cuts) / 1000

    print(f"Bundle    : {bundle}")
    print(f"Backup    : {project_bak}")
    print(f"Original  : {orig_dur:.2f}s ({int(orig_dur//60)}:{int(orig_dur%60):02d})")
    print(f"Final     : {final_dur:.2f}s ({int(final_dur//60)}:{int(final_dur%60):02d})")
    print(f"Cuts      : {len(cuts)}  total={cut_total:.2f}s")
    print(f"Slices    : {len(new_slices)} (was {len(existing_ranges)})")
    print(f"Zoom overlaps: {len(overlaps)} ({'dropped' if args.zoom_policy=='drop' and overlaps else 'none/kept'})")
    print()
    print("To revert: cp", str(project_bak), str(project))


if __name__ == "__main__":
    main()
