---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in TypeScript (recommended) or Python.
metadata:
  author: anthropic
  version: "1.0.0"
allowed-tools: []
---

# MCP Server Development Guide

Create MCP servers that enable LLMs to interact with external services through well-designed tools.

## Overview

The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

**Recommended Stack:**

- **Language**: TypeScript (high-quality SDK, good AI code generation)
- **Transport**: Streamable HTTP for remote, stdio for local

---

## Phase 1: Research & Planning

### 1.1 Modern MCP Design Principles

**API Coverage vs Workflow Tools:**
Balance comprehensive API coverage with specialized workflow tools. When uncertain, prioritize comprehensive API coverage.

**Tool Naming:**
Clear, descriptive names with consistent prefixes:

- `github_create_issue`, `github_list_repos`
- `slack_send_message`, `slack_list_channels`

**Context Management:**
Return focused, relevant data. Support filtering and pagination.

**Actionable Errors:**
Error messages should guide agents toward solutions.

### 1.2 Study Documentation

**MCP Protocol:**

```
https://modelcontextprotocol.io/sitemap.xml
```

Fetch specific pages with `.md` suffix for markdown.

**TypeScript SDK:**

```
https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md
```

**Python SDK:**

```
https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md
```

### 1.3 Plan Implementation

1. Review service API documentation
2. Identify key endpoints and auth requirements
3. Prioritize by common operations

---

## Phase 2: Implementation

### 2.1 Project Structure

**TypeScript:**

```
my-mcp-server/
├── src/
│   ├── index.ts       # Entry point
│   ├── tools/         # Tool implementations
│   └── utils/         # Shared utilities
├── package.json
└── tsconfig.json
```

### 2.2 Core Infrastructure

Create shared utilities:

- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

### 2.3 Tool Implementation

**Input Schema (Zod for TypeScript):**

```typescript
const CreateIssueSchema = z.object({
  title: z.string().describe("Issue title"),
  body: z.string().optional().describe("Issue body in markdown"),
  labels: z.array(z.string()).optional(),
});
```

**Tool Description:**

- Concise summary
- Parameter descriptions
- Return type schema

**Annotations:**

```typescript
{
  readOnlyHint: false,
  destructiveHint: false,
  idempotentHint: true,
  openWorldHint: false
}
```

**Implementation Pattern:**

```typescript
server.registerTool({
  name: "service_action",
  description: "What it does and when to use it",
  inputSchema: ActionSchema,
  handler: async (input) => {
    try {
      const result = await apiClient.action(input);
      return {
        content: [{ type: "text", text: JSON.stringify(result) }],
        structuredContent: result,
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Error: ${error.message}. Try...` }],
        isError: true,
      };
    }
  },
});
```

---

## Phase 3: Review & Test

### 3.1 Code Quality Checklist

- [ ] No duplicated code (DRY)
- [ ] Consistent error handling
- [ ] Full type coverage
- [ ] Clear tool descriptions

### 3.2 Testing

**TypeScript:**

```bash
npm run build
npx @modelcontextprotocol/inspector
```

**Python:**

```bash
python -m py_compile your_server.py
# Test with MCP Inspector
```

---

## Phase 4: Create Evaluations

Create 10 evaluation questions to test effectiveness.

### Requirements

- **Independent**: Not dependent on other questions
- **Read-only**: Non-destructive operations only
- **Complex**: Multiple tool calls required
- **Realistic**: Real use cases
- **Verifiable**: Clear, single answer
- **Stable**: Answer won't change over time

### Output Format

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about...</question>
    <answer>3</answer>
  </qa_pair>
  <!-- More qa_pairs -->
</evaluation>
```

---

## Best Practices

### Tool Design

- Use clear, prefixed naming
- Include examples in descriptions
- Support pagination for list operations
- Return focused data

### Error Handling

- Include actionable next steps
- Suggest alternatives when operations fail
- Validate inputs early

### Security

- Never log credentials
- Use environment variables for secrets
- Validate all inputs

### Performance

- Batch operations where possible
- Cache when appropriate
- Set reasonable timeouts

---

## References

- [MCP Protocol Spec](https://modelcontextprotocol.io)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
