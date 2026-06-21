# MCP tool contracts

One Markdown spec per tool. This is the human-readable source of truth a junior reads
before granting or calling a tool. Keep schemas small and explicit.

**Naming:** `wks_<area>_<verb>`, snake_case. **Every** contract states: purpose,
inputs, outputs, side effects, `kind` (read/write/write-block), `gate`
(none/human), and `egress` (none / endpoint).

See `contract-template.md` for the format. Stubs for the P0 tools live alongside.
