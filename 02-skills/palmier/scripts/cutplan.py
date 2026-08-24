#!/usr/bin/env python3
"""Build the frame ranges to ripple-delete from a Palmier Pro timeline.

    cutplan.py gaps.raw src.json cuts.json [--fps 30] [--tighten 1.0]

gaps.raw   ffmpeg silencedetect output (use -35dB / d=0.18 — see SKILL.md §6)
src.json   inspect_media result with wordTimestamps=true (source seconds)
cuts.json  written: [[startFrame, endFrame], ...] for ripple_delete_ranges

Two sources are merged:
  · silence gaps  -> keep a graded amount of breathing room, delete the rest
  · stutters      -> an immediately repeated word, cut whole (frames, not indices;
                     remove_words shifts indices mid-call and cuts the wrong words)
"""
import json
import re
import sys

# Korean emphatic doubling — these are style, not stutters.
KEEP = {'하나씩', '매출', '정말', '진짜', '점점', '빨리', '다시', '조금',
        '하나', '계속', '또', '조금씩', '천천히'}

# gap length -> breathing room to leave behind (seconds)
KEEP_TABLE = [(0.30, 0.14), (0.50, 0.16), (0.80, 0.19),
              (1.50, 0.26), (3.00, 0.36), (float('inf'), 0.50)]

GUARD = 0.03      # never cut within 30ms of detected speech
MIN_CUT = 0.06    # skip cuts shorter than this — they read as glitches


def keep_for(gap, tighten):
    for limit, keep in KEEP_TABLE:
        if gap < limit:
            return keep * tighten
    return KEEP_TABLE[-1][1] * tighten


def parse_gaps(path):
    starts, ends = [], []
    for line in open(path):
        m = re.search(r'silence_start:\s*([\d.]+)', line)
        if m:
            starts.append(float(m.group(1)))
        m = re.search(r'silence_end:\s*([\d.]+)', line)
        if m:
            ends.append(float(m.group(1)))
    return list(zip(starts, ends))


def main():
    gaps_path, src_path, out_path = sys.argv[1:4]
    fps = 30
    tighten = 1.0
    if '--fps' in sys.argv:
        fps = int(sys.argv[sys.argv.index('--fps') + 1])
    if '--tighten' in sys.argv:
        tighten = float(sys.argv[sys.argv.index('--tighten') + 1])

    ranges, silence_s = [], 0.0
    for s, e in parse_gaps(gaps_path):
        inner_s, inner_e = s + GUARD, e - GUARD
        if inner_e <= inner_s:
            continue
        cut = (inner_e - inner_s) - keep_for(e - s, tighten)
        if cut < MIN_CUT:
            continue
        mid = (inner_s + inner_e) / 2
        a, b = round((mid - cut / 2) * fps), round((mid + cut / 2) * fps)
        if b > a:
            ranges.append([a, b])
            silence_s += (b - a) / fps
    gap_n = len(ranges)

    words = json.load(open(src_path))['transcription']['words']
    norm = lambda s: re.sub(r'[^\w가-힣]', '', s)
    stutter_n, stutter_s = 0, 0.0
    for k in range(len(words) - 1):
        a, b = norm(words[k][0]), norm(words[k + 1][0])
        if a and a == b and len(a) <= 4 and a not in KEEP:
            x, y = round(words[k][1] * fps), round(words[k + 1][1] * fps)
            if y > x:
                ranges.append([x, y])
                stutter_n += 1
                stutter_s += (y - x) / fps

    ranges.sort()
    merged = []
    for r in ranges:
        if merged and r[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], r[1])
        else:
            merged.append(r)
    json.dump(merged, open(out_path, 'w'))

    total = sum((b - a) / fps for a, b in merged)
    dur = json.load(open(src_path))['durationSeconds']
    new = dur - total
    print(f"갭 {gap_n}구간 / {silence_s:.0f}s + 말더듬 {stutter_n}건 / {stutter_s:.1f}s")
    print(f"병합 {len(merged)}구간, {total:.0f}s 제거")
    print(f"→ {new:.0f}s = {int(new // 60)}분 {int(new % 60)}초 "
          f"({dur:.0f}s 대비 -{total / dur * 100:.1f}%)")


if __name__ == '__main__':
    main()
