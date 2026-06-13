---
name: n8n Slack & Notion Automation Skill
description: A comprehensive guide and template for building robust Slack bots integrated with Notion and n8n, handling timeouts, challenges, and complex logic.
---

# n8n Slack & Notion Automation Skill

This skill provides a standardized way to build Slack bots that integrate with Notion and other tools using n8n. It addresses common challenges such as Slack's 3-second timeout, URL verification challenges, and complex data processing.

## Core Interactive Pattern ("Ack-First")

Slack requires a response within 3 seconds. To handle this, we use an "Ack-First" pattern:

1.  **Receive Webhook**: The entry point for Slack events.
2.  **Immediate Verification/Filtering**:
    - Check for `url_verification` challenge.
    - Filter out bot messages and retries.
3.  **Split Logic**:
    - If it's a challenge -> Respond with the challenge value immediately.
    - If it's a valid message -> Respond with HTTP 200 OK (empty body) to satisfy Slack's timeout.
4.  **Asynchronous Processing**:
    - After the immediate response, continue processing (e.g., query Notion, run Python scripts).
    - Send the final result back to Slack using the `Slack` node (chat.postMessage).

## Best Practices

- **Handle Challenges**: Always include logic to respond to `url_verification` events.
- **Filter Bots**: Ignore events where `bot_id` is present to prevent infinite loops.
- **Ignore Retries**: Check `x-slack-retry-num` to avoid processing the same message multiple times if Slack retries due to a timeout (even if you responded, network latency can cause retries).
- **Secure Implementation**:
  - Verify Slack signatures if possible (though the challenge/retry logic covers most "noise").
  - Use Base64 encoding when passing user input to shell commands to prevent injection.
- **Error Handling**: Use n8n's Error Trigger or Try/Catch nodes to report failures back to a monitoring channel or the user.

### A Note on Command Execution

- **"Execute Command" vs "Execute a command"**:
  - The built-in `Execute Command` node is often disabled for security reasons in modern n8n environments.
  - **Recommendation**: Use the **SSH** node (often named "Execute a command" in workflows) to run commands. It allows you to execute scripts on the local machine (via `localhost` SSH) or a remote server securely and reliably.
  - This skill's template uses the SSH node pattern for this reason.

## Directory Structure

```
.agent/skills/n8n-slack-notion-automation/
├── SKILL.md              # This file
├── templates/            # Workflow templates
│   └── slack_bot_template.json    # Base template with Ack-First logic
├── scripts/              # Helper scripts (optional)
│   └── assistant.py      # Example Python script for complex logic
```

## Setup Instructions

1.  **Import Template**: Import `templates/slack_bot_template.json` into n8n.
2.  **Configure Credentials**:
    - **Slack**: Create a Slack App, enable Event Subscriptions, and set the Request URL to your n8n Production Webhook URL. Add the `Slack API` credential in n8n.
    - **Notion**: Create a Notion Integration, share database(s) with it, and add the `Notion API` credential in n8n.
    - **SSH (Optional)**: If using external scripts, configure `SSH` credentials (often localhost).
3.  **Environment Variables**: Ensure necessary environment variables (e.g., `SLACK_BOT_TOKEN`, `NOTION_TOKEN`) are set if referenced in scripts.

## Usage Guide

1.  **Basic Bot**: Use the template's "Process Message" section to add simple logic (e.g., switch based on keywords).
2.  **Advanced Logic**: Use the "Execute a command" (SSH) node pattern (from the template) to run external scripts (Python/Node.js) for complex reasoning or data processing that is hard to do in n8n nodes.
3.  **Notion Integration**: Use the Notion node to Create/Update pages based on Slack input.

## Common Issues

- **"Dispatch failed"**: Usually means the Slack App is not properly installed in the channel or the workspace.
- **Timeout / Multiple Replies**: Ensure the "Ack" node is executed _before_ any heavy processing.
- **Infinite Loops**: Double-check the bot filter logic (`if (event.bot_id) ...`).
