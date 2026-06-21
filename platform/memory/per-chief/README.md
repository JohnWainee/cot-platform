# Per-Chief memory (Tier 1) — vault layout

PACE-derived. Each Chief gets an **isolated** vault (its own files + its own SQLite
FTS5 index). Human-readable, grep-able, git-ignorable runtime state. **No vector DB
here** — that's Tier 2.

```text
<chief>/vault/
├── memories/
│   ├── working/        # today's captures (always loaded; soft cap 16k / hard 32k chars)
│   ├── long_term/      # stable facts (promoted; #person/#decision/#high-signal exempt)
│   └── archived/       # aged-out, search-only
├── projects/<name>/{summary.md, notes/}
├── followups/          # proactive inbox; <id>.md + done/
└── system/
    ├── index.db        # SQLite FTS5 (rebuildable — see rebuild-memory-index runbook)
    ├── config.yaml     # budgets, retention, heartbeat opt-in
    └── logs/
```

## Lazy maintenance (no cron)

`wks_memory_status` returns `needs_compact` (24h+), `needs_review` (7d+),
`needs_heartbeat` (opt-in). The Chief runs whatever's flagged **silently after**
replying to the first message of a session. Nothing is ever deleted; review archives.

## Promotion / retention (conservative)

Promote to long_term when an entry is ≥N days old **and** referenced, **or** carries
a long-term tag, **or** would overflow the working budget. Never evict
`#user` / `#high-signal` / `#decision`.

> Patterns adopted from PACE; see ADR-0006. Runtime vaults are **git-ignored**.
