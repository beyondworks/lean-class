# Intent Bridge Skill

Use this skill when the user gives an under-specified coding request in natural language.

Your job:
- translate intent into AgentSpec v1
- keep user-facing questions simple
- prefer assumptions over unnecessary questioning
- use project context tools first
- use Metric Lock on every task

When to use:
- feature requests
- bug fixes
- refactors
- UI changes
- test requests
- infrastructure/devops changes

Do not use for:
- pure conversation
- translation only
- unrelated brainstorming with no implementation intent

Artifacts in this skill:
- agentspec-schema.json
- clarification-rules.md
- examples.md
