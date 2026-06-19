"use client";

import { Agentation } from "agentation";

const endpoint =
  process.env.NEXT_PUBLIC_AGENTATION_ENDPOINT ?? "http://127.0.0.1:4747";

export function AgentationDevToolbar() {
  if (process.env.NODE_ENV !== "development") return null;

  return <Agentation endpoint={endpoint} />;
}
