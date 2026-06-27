"""Tier-1 vault storage engine (PACE-tiered Markdown + SQLite FTS5).

Adapted from smriti-mcp's ``MemoryStore``. Scaffold only — every method raises
``NotImplementedError`` until the Phase-0 plan unblocks implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class MemoryEntry:
    """One vault entry (a Markdown file with YAML frontmatter)."""

    id: str
    path: Path
    kind: str
    topic: str
    tags: tuple[str, ...] = ()


class MemoryStore:
    """Per-Chief, isolated vault: own files + own FTS5 index.

    Tiers: ``working`` -> ``long_term`` -> ``archived`` (plus ``projects/`` and
    ``followups/``). Lazy maintenance, no cron. Nothing is ever deleted; review
    archives. See ``docs/ARCHITECTURE.md``.
    """

    def __init__(self, vault_root: Path) -> None:
        self.vault_root = vault_root

    def initialize(self) -> bool:
        """Create the vault layout if absent. Returns False if it already existed."""
        raise NotImplementedError

    def capture(self, *, kind: str, topic: str, text: str, **meta: object) -> MemoryEntry:
        """Write one entry to the working tier and update the FTS5 index."""
        raise NotImplementedError

    def search(self, query: str, *, limit: int = 10) -> list[MemoryEntry]:
        """Full-text search the vault, ranked."""
        raise NotImplementedError

    def status(self) -> dict[str, object]:
        """Return lazy-maintenance flags (compact/review/heartbeat) + tier counts."""
        raise NotImplementedError

    def compact(self) -> None:
        """Promote/retain per policy and rebuild the index. Never deletes."""
        raise NotImplementedError
