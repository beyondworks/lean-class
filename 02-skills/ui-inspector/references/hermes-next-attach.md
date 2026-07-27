# Hermes / Next.js attach workflow

Use this reference when a Hermes profile needs to run a live Next.js app through UI Inspector but the direct MCP tool names (`preview_attach`, `preview_select_element`, etc.) are not exposed as first-class Hermes tools.

## Goal

Attach UI Inspector to an already-running Next.js/Vite dev server through the inspector proxy, then open the proxy URL and enable Inspector mode so the user can click elements and ask for targeted UI fixes.

## Standard sequence

1. Confirm the app dev server is actually healthy before attaching:
   - page route returns `200`
   - key API route(s) return `200`
   - if a stale listener is wedged, stop it and restart the dev server cleanly
2. Start the project dev server in a tracked background process, preferably with PTY for Next.js dev output:
   ```bash
   ./node_modules/.bin/next dev -p <app_port>
   ```
3. If Hermes does not expose UI Inspector MCP tools directly, create a temporary MCP client script inside the UI Inspector server working directory, not `/tmp`, so Node can resolve dependencies:
   ```js
   import { Client } from '@modelcontextprotocol/sdk/client/index.js';
   import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

   const transport = new StdioClientTransport({
     command: 'node',
     args: ['/absolute/path/to/ui-inspector/servers/inspector-server.mjs'],
     cwd: '/absolute/path/to/ui-inspector/servers',
   });
   const client = new Client({ name: 'hermes-ui-inspector-attach', version: '1.0.0' });
   await client.connect(transport);
   const result = await client.callTool({
     name: 'preview_attach',
     arguments: {
       url: 'http://localhost:<app_port>',
       project_name: '<ProjectName>',
       port: <proxy_port>,
     },
   });
   console.log(JSON.stringify(result, null, 2));
   setInterval(() => {}, 1_000_000);
   ```
4. Run that script in the background from the UI Inspector `servers/` directory.
5. Verify the proxy HTML contains injected inspector markers such as `Inspector`, `inspector`, `data-at`, and a WebSocket URL.
6. Open the proxy URL in the browser, e.g. `http://localhost:<proxy_port>`.
7. Turn on Inspector mode via the bottom-right toggle or `preview_select_element` if available.
8. Ask the user to click the target element. On follow-up requests like “이 부분”, call `inspector_get_selection` first.

## Pitfalls

- Do not run the temporary MCP client from `/tmp` with bare package imports unless dependency resolution is configured. Put it under the UI Inspector `servers/` directory or use import paths that Node can resolve.
- Do not judge the app through the proxy until the underlying app URL is healthy; proxy timeouts often mean the target server is wedged.
- If a stale Next.js listener remains after killing a parent process, kill the actual port listener, then restart dev and re-verify HTTP `200` before attaching.
- Remove temporary helper scripts after successful attach unless they are intentionally promoted into a reusable script.
