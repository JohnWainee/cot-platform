"""MCP stdio server exposing the ``wks_memory_*`` tools.

Scaffold only. Tool handlers raise ``NotImplementedError``; wire them to
:class:`cot_memory.store.MemoryStore` (Tier 1) and, in P1, the pgvector backend
(Tier 2). Contracts: ``docs/contracts/``.
"""

from __future__ import annotations

# P0 tools (Tier 1 — per-Chief vault).
TIER1_TOOLS = ("wks_memory_capture", "wks_memory_search", "wks_memory_status")

# P1 tools (Tier 2 — shared semantic, read-only). Added behind the same server.
TIER2_TOOLS = ("wks_repo_search", "wks_repo_read")


def build_server() -> object:
    """Construct the MCP server and register the Tier-1 tools.

    Returns the MCP server instance. Not implemented yet.
    """
    raise NotImplementedError


def run() -> None:
    """Run the server over stdio. Entry point used by the CLI."""
    raise NotImplementedError
