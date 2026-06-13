---
name: remotion-best-practices
description: Best practices for building programmatic videos with Remotion. Use when creating video compositions, optimizing render performance, implementing animations, working with Remotion Player, or when asked to "build a video", "create animation", "optimize Remotion render", or "fix video flicker".
metadata:
  author: remotion-dev (optimized 2026-01)
  version: "2.0.0"
allowed-tools: []
---

# Remotion Best Practices (2026)

Guidelines for building high-quality programmatic videos with Remotion.

## Core Concepts

### Frame-Based Thinking

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

export const MyComponent: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return <div style={{ opacity }}>Content</div>;
};
```

### Determinism (Critical)

Always produce the same output for the same frame:

```tsx
// ❌ WRONG: Non-deterministic
const randomValue = Math.random()
const now = new Date()

// ✅ CORRECT: Use Remotion's random function
import { random } from 'remotion'
const randomValue = random('my-seed')

// ✅ Pass values as props
<MyVideo timestamp={Date.now()} />
```

## Animation Patterns

### Interpolation

```tsx
const opacity = interpolate(
  frame,
  [0, 30], // input range (frames)
  [0, 1], // output range
  { extrapolateRight: "clamp" },
);
```

### Spring Animation

```tsx
const scale = spring({
  frame,
  fps,
  config: {
    damping: 200,
    stiffness: 100,
    mass: 0.5,
  },
});
```

### Sequences & Series

```tsx
import { Sequence, Series } from 'remotion'

// Ordered sequences
<Series>
  <Series.Sequence durationInFrames={60}>
    <Intro />
  </Series.Sequence>
  <Series.Sequence durationInFrames={120}>
    <MainContent />
  </Series.Sequence>
</Series>

// Overlapping content
<Sequence from={0} durationInFrames={90}>
  <Background />
</Sequence>
<Sequence from={30} durationInFrames={60}>
  <Text />
</Sequence>
```

## Performance Optimization

### Memoize inputProps

```tsx
import { Player } from "@remotion/player";
import { useMemo } from "react";

export const App: React.FC = () => {
  const [text, setText] = useState("Hello");

  // Memoize to prevent unnecessary re-renders
  const inputProps = useMemo(() => ({ text }), [text]);

  return (
    <Player
      component={MyVideo}
      inputProps={inputProps}
      durationInFrames={120}
      fps={30}
      compositionWidth={1920}
      compositionHeight={1080}
    />
  );
};
```

### Video Handling

```tsx
// Use OffthreadVideo for better performance
import { OffthreadVideo } from "remotion";

<OffthreadVideo src={videoUrl} pauseWhenBuffering />;
```

### Asset Prefetching

```tsx
import { prefetch, delayRender, continueRender } from "remotion";

// Prefetch to prevent flicker
const { free, waitUntilDone } = prefetch(assetUrl);
await waitUntilDone();

// For heavy assets
const handle = delayRender();
try {
  await loadAsset();
  continueRender(handle);
} catch (err) {
  cancelRender(err);
}
```

### Pre-mounting for Smooth Transitions

```tsx
<Series>
  {videos.map((vid) => (
    <Series.Sequence
      key={vid.src}
      premountFor={4 * fps} // Pre-mount 4 seconds early
      durationInFrames={vid.durationInFrames}
    >
      <OffthreadVideo pauseWhenBuffering src={vid.src} />
    </Series.Sequence>
  ))}
</Series>
```

## Preventing Video Flicker

1. **Preload assets**: Use `delayRender()` and `continueRender()`
2. **Prefetch to blob**: `prefetch(url, { method: 'blob-url' })`
3. **Use OffthreadVideo**: Better memory management
4. **Premount sequences**: Prepare next content early
5. **pauseWhenBuffering**: Pause playback during loading

## Lambda Rendering (Cloud)

```tsx
import { renderMediaOnLambda } from "@remotion/lambda";

const { renderId } = await renderMediaOnLambda({
  region: "us-east-1",
  functionName: "remotion-render",
  composition: "MyVideo",
  inputProps: {
    /* ... */
  },
  codec: "h264",
});
```

## Common Anti-Patterns

### Avoid

- `Math.random()` in render path
- `new Date()` without passing as prop
- Heavy calculations without `useMemo`
- Fetching data in render function
- Using `Video` instead of `OffthreadVideo` for multiple videos

### Prefer

- Deterministic random: `random('seed')`
- Pre-calculated values as props
- Memoized heavy operations
- `delayRender()` for async loading
- `OffthreadVideo` for better performance

## References

- [Remotion Docs](https://www.remotion.dev/docs)
- [Player Best Practices](https://www.remotion.dev/docs/player/best-practices)
- [Troubleshooting Flicker](https://www.remotion.dev/docs/troubleshooting/video-flicker)
