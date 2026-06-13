---
name: vercel-react-best-practices
description: React and Next.js best practices from Vercel Engineering. Use when building React/Next.js applications, optimizing performance, implementing React Server Components (RSC), configuring App Router data fetching, or when asked to "review React code", "optimize Next.js", "implement RSC patterns", or "improve web vitals".
metadata:
  author: vercel-labs (optimized 2026-01)
  version: "2.0.0"
allowed-tools: []
---

# React & Next.js Best Practices (2026)

Optimized guidelines for modern React 19 and Next.js 15+ applications.

## Server Components (RSC) Patterns

### Default to Server Components

- Components are Server Components by default in App Router
- Only add `'use client'` when using hooks, browser APIs, or event handlers
- Keep `'use client'` boundaries as low as possible in the component tree

### Data Fetching in Server Components

```tsx
// Static data (cached indefinitely)
const data = await fetch(url, { cache: "force-cache" });

// Dynamic data (no cache)
const data = await fetch(url, { cache: "no-store" });

// Revalidated data (time-based)
const data = await fetch(url, { next: { revalidate: 60 } });
```

### Component Composition Pattern

```tsx
// Server Component fetches data
export default async function Page() {
  const data = await getData();
  return <ClientComponent data={data} />;
}

// Client Component handles interactivity
("use client");
function ClientComponent({ data }) {
  const [state, setState] = useState(data);
  // ...
}
```

## Performance Optimization

### Core Web Vitals

- **LCP < 2.5s**: Optimize largest image, use `priority` prop
- **INP < 200ms**: Minimize JS bundle, defer non-critical scripts
- **CLS < 0.1**: Set explicit `width`/`height` on images

### Image Optimization

```tsx
import Image from 'next/image'

// Above-fold: priority loading
<Image src={hero} alt="" priority width={1200} height={600} />

// Below-fold: lazy loading (default)
<Image src={card} alt="" width={400} height={300} />
```

### Dynamic Imports

```tsx
import dynamic from "next/dynamic";

const HeavyComponent = dynamic(() => import("./HeavyComponent"), {
  loading: () => <Skeleton />,
  ssr: false, // if client-only
});
```

## Caching Strategies

### Route Segment Config

```tsx
// Force dynamic rendering
export const dynamic = "force-dynamic";

// Force static rendering
export const dynamic = "force-static";

// Revalidate every N seconds
export const revalidate = 60;
```

### On-Demand Revalidation

```tsx
import { revalidatePath, revalidateTag } from "next/cache";

// Revalidate specific path
revalidatePath("/blog");

// Revalidate by tag
revalidateTag("posts");
```

## State Management

### URL State (Recommended)

```tsx
import { useSearchParams } from "next/navigation";

// Use URL for shareable state: filters, pagination, tabs
const searchParams = useSearchParams();
const page = searchParams.get("page") || "1";
```

### Server State

- Use React Query or SWR for client-side data fetching
- Prefer Server Components for initial data load

## Common Anti-Patterns

### Avoid

- `'use client'` at page level (push down to leaf components)
- Fetching data in Client Components when Server Components can do it
- `useEffect` for data fetching (use Server Components or SWR)
- Large client-side bundles (code-split aggressively)
- Prop drilling across many levels (use context or composition)

### Prefer

- Parallel data fetching with `Promise.all()`
- Streaming with `<Suspense>` boundaries
- Incremental Static Regeneration (ISR) for semi-static content
- Edge Runtime for latency-sensitive routes

## TypeScript Best Practices

```tsx
// Typed Server Actions
"use server";
export async function createPost(
  formData: FormData,
): Promise<{ success: boolean; error?: string }> {
  // ...
}

// Typed Route Params
type Props = {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ page?: string }>;
};
```

## References

- [Next.js Docs](https://nextjs.org/docs)
- [React Server Components](https://react.dev/reference/rsc/server-components)
- [Vercel Best Practices](https://vercel.com/docs)
