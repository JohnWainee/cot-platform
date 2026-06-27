"""Console entry point: ``cot-memory``.

Scaffold only — starts the MCP stdio server once implemented.
"""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    """Start the cot-memory MCP server over stdio."""
    _ = argv if argv is not None else sys.argv[1:]
    raise NotImplementedError("cot-memory is a scaffold; see docs/ARCHITECTURE.md")


if __name__ == "__main__":
    raise SystemExit(main())
