"""Chapter 07: interrupt and resume."""

from __future__ import annotations

from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    action: str
    approved: bool


def ask(state: State) -> dict:
    answer = interrupt({"question": f"是否执行 {state['action']}？"})
    return {"approved": bool(answer)}


def act(state: State) -> dict:
    return {"action": state["action"] + (" 已执行" if state["approved"] else " 已取消")}


def build():
    builder = StateGraph(State)
    builder.add_node("ask", ask)
    builder.add_node("act", act)
    builder.add_edge(START, "ask")
    builder.add_edge("ask", "act")
    builder.add_edge("act", END)
    return builder.compile(checkpointer=InMemorySaver())


def main() -> None:
    graph = build()
    config = {"configurable": {"thread_id": "hitl-1"}}
    graph.invoke({"action": "删除 /tmp/a.txt", "approved": False}, config)
    print("paused at:", graph.get_state(config).next)
    out = graph.invoke(Command(resume=True), config)
    print(out)


if __name__ == "__main__":
    main()
