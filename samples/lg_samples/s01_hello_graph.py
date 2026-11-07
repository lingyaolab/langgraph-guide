"""Chapter 01: the smallest StateGraph."""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    text: str


def upper(state: State) -> dict:
    return {"text": state["text"].upper()}


def build():
    builder = StateGraph(State)
    builder.add_node("upper", upper)
    builder.add_edge(START, "upper")
    builder.add_edge("upper", END)
    return builder.compile()


def main() -> None:
    graph = build()
    print(graph.invoke({"text": "hello langgraph"}))


if __name__ == "__main__":
    main()
