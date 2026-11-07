"""Chapter 06: history, replay and fork."""

from __future__ import annotations

from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    n: int


def inc(state: State) -> dict:
    return {"n": state["n"] + 1}


def build():
    builder = StateGraph(State)
    builder.add_node("inc", inc)
    builder.add_edge(START, "inc")
    builder.add_edge("inc", END)
    return builder.compile(checkpointer=InMemorySaver())


def main() -> None:
    graph = build()
    config = {"configurable": {"thread_id": "demo"}}
    for _ in range(3):
        graph.invoke({"n": 0}, config)

    history = list(graph.get_state_history(config))
    print("history:", len(history))
    old = history[-2]
    fork = graph.update_state(old.config, {"n": 10}, as_node="inc")
    out = graph.invoke(None, fork)
    print("fork result:", out)


if __name__ == "__main__":
    main()
