# Screen Studio `project.json` schema (reverse-engineered)

> Schema captured against Screen Studio 3.6.0-4214 (`requiredVersion: 2.4.0-beta`). Subject to change in future app versions.

## Top level

```jsonc
{
  "json": {
    "id": "<10-char nanoid>",
    "name": "...",
    "createdAt": "ISO-8601",
    "updatedAt": "ISO-8601",
    "lastSavedAt": "ISO-8601 | null",
    "config": { /* §1 global effects */ },
    "meta": { "recordingFlags": [] },
    "scenes": [ /* §2 timeline */ ]
  },
  "meta": { "values": { "createdAt": ["Date"], "updatedAt": ["Date"], "lastSavedAt": ["Date"] } }
}
```

## §1 `config` — global effects

| key | type | notes |
|---|---|---|
| `backgroundType` | `"system"` `"color"` `"gradient"` `"image"` | controls which of the next four wins |
| `backgroundColor` | hex `"#RRGGBB"` | |
| `backgroundGradient` | `{start:{x,y}, end:{x,y}, stops:[{color,at}]}` | start/end normalized 0-1 |
| `backgroundSystemName` | string | e.g. `"macOS/tahoe-light.jpg"` |
| `backgroundImage` | path or null | |
| `backgroundBlur` | float | px |
| `backgroundPaddingRatio` | float 0-1 | |
| `insetPadding` | `{top,right,bottom,left}` | px |
| `insetColor` / `insetAlpha` | hex / float 0-1 | |
| `motionBlurAmount` | float | global multiplier |
| `motionBlurCursorAmount` | float | |
| `motionBlurScreenMoveAmount` | float | |
| `motionBlurScreenZoomAmount` | float | |
| `cursorSize` | float | 1.0 = native |
| `cursorSet` | `{id, variants}` | id like `"macos-tahoe"` |
| `cursorRotateOnXMovementRatio` | float 0-1 | |
| `cursorBaseRotation` | float | degrees |
| `useDefaultCursorIfAppCursorHasLowResolution` | bool | |
| `alwaysUseDefaultCursor` | bool | |
| `hideNotMovingCursorAfterMs` | int / null | |
| `loopCursorPositionBeforeEndMs` | int / null | |
| `removeCurshorShakeTreshold` | int (ms) | **typo preserved verbatim** in app |
| `optimizeOriginalCursorTypes` | bool | |
| `clickEffect` | string id / null | |
| `clickSoundEffect` | string id / null | |
| `clickSoundEffectVolume` | 0-1 | |
| `mouseMovementSpring` | `{stiffness, damping, mass}` | spring physics |
| `screenMovementSpring` | `{stiffness, damping, mass}` | |
| `mouseClickSpring` | `{stiffness, damping, mass}` | |
| `disableMouseMovementSpring` | bool | |
| `defaultOutputAspectRatio` | string / null | |
| `windowBorderRadius` | px | |
| `alwaysKeepZoomedIn` | bool | |
| `shadowIntensity` | 0-1 | |
| `shadowAngle` | degrees | |
| `shadowDistance` | px | |
| `shadowBlur` | px | |
| `shadowIsDirectional` | bool | |
| `hideCamera` | bool | |
| `mirrorCamera` | bool | |
| `cameraRoundness` | 0-1 | |
| `cameraSize` | 0-1 | of frame |
| `cameraPosition` | `"top-left"`, `"top-right"`, `"bottom-left"`, `"bottom-right"` | |
| `cameraPositionPoint` | `{x,y}` 0-1 | |
| `cameraScaleDuringZoom` | 0-1 | |
| `cameraAspectRatio` | `"square"` `"original"` ... | |
| `stopCursorMovementInLastPartMs` | int | |
| `showShortcuts` | bool | |
| `showShortcutsWithSingleLetters` | bool | |
| `hiddenShortcuts` | object | |
| `shortcutsSizeRatio` | float | |
| `showTranscript` | bool | |
| `transcriptSizeRatio` | float | |
| `audioVolume` | 0-1 | global |
| `muteMicrophone` | bool | |
| `muteSystemAudio` | bool | |
| `muteExternalDeviceAudio` | bool | |
| `improveMicrophoneAudio` | bool | |
| `backgroundAudioFileName` | string / null | |
| `muteBackgroundAudio` | bool | |
| `backgroundAudioVolume` | 0-1 | |
| `microphoneInStereoMode` | bool | |
| `deviceFrameKey` | string / null | |
| `enableDeviceMockup` | bool | |
| `adjustDeviceFrameToRecordingSize` | bool | |
| `defaultLayout` | `{type, cameraSize, cameraPositionPoint}` | |
| `recordingRange` | `[startMs, endMs]` | overall trim window in source time |
| `recordingCrop` | `{x, y, width, height}` | normalized 0-1 |

Unknown keys: leave them alone. The app may add fields in future versions.

## §2 `scenes[]`

```jsonc
{
  "id": "<id>",
  "name": "Default",
  "type": "recording",
  "sessionIndex": 0,
  "zoomRanges": [ /* §2.1 */ ],
  "slices":     [ /* §2.2 — THE TIMELINE */ ],
  "layouts":    [],
  "masks":      [],
  "resolvedTypingSpeedIncreaseSuggestions": []
}
```

### §2.1 `zoomRanges[]`

```jsonc
{
  "id": "<id>",
  "zoom": 1.7,                                 // float, 1.0 = no zoom
  "type": "follow-click-groups",               // also seen: presumably "manual", others
  "snapToEdgesRatio": 0.25,
  "manualTargetPoint": {"x": 0.5, "y": 0.5},   // normalized
  "glideDirection": null,
  "glideSpeed": 0.5,
  "isDisabled": false,
  "startTime": 370210,                          // SOURCE ms (NOT output)
  "endTime":   373084,                          // SOURCE ms
  "isSystem": false,
  "hasInstantAnimation": false
}
```

Cuts that overlap a zoom break the zoom. The `screenstudio-cut` skill checks for overlaps and aborts/drops by default.

### §2.2 `slices[]` — the timeline (we edit this)

```jsonc
{
  "id": "<id>",
  "timeScale": 1,                  // 0.5 = 2× slower; 2.0 = 2× faster; >0
  "sourceStartMs": 0,              // source-time start
  "sourceEndMs": 956101.39,        // source-time end
  "volume": 1,
  "systemAudioVolume": 1,
  "externalDeviceAudioVolume": 1,
  "hideCursor": false,
  "disableSmoothMouseMovement": false
}
```

Adjacent slices may have non-contiguous source ranges — gaps in source time = cuts.

### §2.3 `layouts[]` and `masks[]`

Empty in every recording observed so far. Schema unknown. Do **not** synthesize entries; if a user asks, have them add one in the app first, then read the resulting fields.

## §3 Time coordinate rules

- Every numeric time field in `project.json` is **source-recording milliseconds** unless documented otherwise.
- Output time (what the viewer sees) is computed by walking `slices[]`:
  ```
  for each slice in order:
      out_t += (sourceEndMs - sourceStartMs) / timeScale
  ```
- The user's playback timeline is output time. Any time the user gives you that came from playback must be converted back to source time before editing.

## §4 IDs

- Shape: 10-character alphanumeric (mixed case + digits). Example: `OxTpC9dKsN`.
- Generate fresh IDs for new slices. Do **not** reuse the original slice id (Screen Studio may key on `id` for change tracking).
- Do **not** change IDs of zoomRanges, scenes, or the project root unless you're deliberately renaming.

## §5 Versioning

`meta.json`:
```json
{
  "version": "3.6.0-4214",        // app that wrote it
  "requiredVersion": "2.4.0-beta", // minimum app version that can open it
  "createdAt": "..."
}
```

**Never raise `requiredVersion`.** Lowering it is also unsafe (you have no way to verify older parsers handle current fields). Leave it alone.

## §6 Recording sidecar files (read-only references)

Inside `recording/`:

### `mouseclicks-0.json`, `mousemoves-0.json`, `keystrokes-0.json`
Arrays of input events. Field shape:
```jsonc
{
  "activeModifiers": [],
  "button": "left",                // mouseclicks only
  "cursorId": "arrow",
  "processTimeMs": 372890.05,      // SOURCE TIME (ms from recording start)
  "unixTimeMs": 1778226043175.99,  // wall-clock unix time (informational)
  "type": "mouseDown",             // mouseDown / mouseUp / mouseMoved
  "x": 2229.04, "y": 454.00        // SCREEN PIXEL coordinates (raw display)
}
```
**Use `processTimeMs`** — it matches `project.json` source time. `unixTimeMs` is wall-clock and not aligned to project timeline.

Click bursts are the auto-zoom triggers. A `zoomRange` near a click in source time was probably auto-generated.

### `cursors.json` and `cursors/`
System cursor catalog. Each cursor: `{id, hotSpot:{x,y}, standardSize:{width,height}, systemCursor:bool}`. The `cursors/` folder holds the bitmap variants. Don't touch.

### `metadata.json` / `metadata-raw.json`
Polyrecorder configuration: which channels were recorded, file names, durations. Read-only reference for understanding the bundle. `metadata-raw.json` is the Swift-serialized form; `metadata.json` is the JSON-normalized version. Either works for inspection.

### `polyrecorder.log`
Plain text log from the recording session. Useful for debugging recording-time issues, irrelevant for cut editing.

### `*.m3u8`, `*.m4s`, `*.mp4`, `*.m4a`
HLS streaming format. The `m3u8` is the manifest, `m4s` are the chunks, `mp4`/`m4a` are concatenated outputs. Screen Studio plays from these at render time. Do not reorder, rename, or delete any of them.
