"""Smoke tests — the package imports and the surface exists.

Behavioural tests come with implementation (the scaffold raises NotImplementedError).
"""

import cot_memory
from cot_memory import server, store


def test_version() -> None:
    assert cot_memory.__version__ == "0.0.0"


def test_tool_surface() -> None:
    assert "wks_memory_capture" in server.TIER1_TOOLS
    assert "wks_memory_search" in server.TIER1_TOOLS
    assert "wks_memory_status" in server.TIER1_TOOLS


def test_store_class_present() -> None:
    assert hasattr(store, "MemoryStore")
