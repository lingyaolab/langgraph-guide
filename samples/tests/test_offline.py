"""Offline tests for the LangGraph samples. No API key or network needed."""

from __future__ import annotations

import pytest

from lg_samples.s01_hello_graph import build as build_hello
from lg_samples.s02_state_reducer import build as build_reducer
from lg_samples.s03_router import build as build_router
from lg_samples.s04_map_reduce import build as build_map_reduce
from lg_samples.s05_checkpoint import build as build_checkpoint
from lg_samples.s06_time_travel import build as build_time_travel
from lg_samples.s07_hitl import build as build_hitl
from lg_samples.s11_tool_agent import build as build_tool_agent
from lg_samples.s13_memory_store import build as build_store


def test_hello_graph():
    assert build_hello().invoke({"text": "hi"})["text"] == "HI"


def test_reducer_merges():
    out = build_reducer().invoke({"total": 0, "logs": []})
    assert out["total"] == 3
    assert out["logs"] == ["add_one", "add_two"]


def test_router_takes_billing():
    out = build_router().invoke({"question": "退款", "route": "", "answer": ""})
    assert out["answer"] == "进入退款流程"


def test_map_reduce_merges_all_docs():
    docs = [{"id": "a", "text": "alpha"}, {"id": "b", "text": "beta"}]
    out = build_map_reduce().invoke({"docs": docs, "summaries": [], "report": ""})
    assert len(out["summaries"]) == 2
    assert "0:alpha" in out["report"]


def test_checkpoint_keeps_history():
    graph = build_checkpoint()
    cfg = {"configurable": {"thread_id": "test"}}
    graph.invoke({"messages": [("user", "hi")]}, cfg)
    out = graph.invoke({"messages": [("user", "again")]}, cfg)
    assert len(out["messages"]) >= 3


def test_time_travel_fork():
    graph = build_time_travel()
    cfg = {"configurable": {"thread_id": "tt"}}
    for _ in range(3):
        graph.invoke({"n": 0}, cfg)
    history = list(graph.get_state_history(cfg))
    fork = graph.update_state(history[-2].config, {"n": 10}, as_node="inc")
    assert graph.invoke(None, fork)["n"] == 10


def test_hitl_resume():
    from langgraph.types import Command

    graph = build_hitl()
    cfg = {"configurable": {"thread_id": "h"}}
    graph.invoke({"action": "x", "approved": False}, cfg)
    out = graph.invoke(Command(resume=True), cfg)
    assert out["approved"] is True


def test_tool_loop_is_deterministic():
    out = build_tool_agent().invoke({"messages": [("user", "北京天气")]})
    assert out["messages"][-1].content == "北京 18C，晴。"
    assert any(type(m).__name__ == "ToolMessage" for m in out["messages"])


def test_store_is_cross_thread():
    graph = build_store()
    out = graph.invoke({"user_id": "alice", "action": "remember", "tone": "", "message": ""})
    assert out["tone"] == "concise"
    out2 = graph.invoke({"user_id": "alice", "action": "recall", "tone": "", "message": ""})
    assert out2["tone"] == "concise"
    out3 = graph.invoke({"user_id": "bob", "action": "recall", "tone": "", "message": ""})
    assert out3["tone"] == "default"
