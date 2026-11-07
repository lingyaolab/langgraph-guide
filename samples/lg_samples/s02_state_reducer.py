"""Chapter 02: reducers change how partial updates merge."""

from __future__ import annotations

from operator import add
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    total: Annotated[int, add]
    logs: Annotated[list[str], add]


def add_one(state: State) -> dict:
    return {"total": 1, "logs": ["add_one"]}


def add_two(state: State) -> dict:
    return {"total": 2, "logs": ["add_two"]}


def build():
    builder = StateGraph(State)
    builder.add_node("add_one", add_one)
    builder.add_node("add_two", add_two)
    builder.add_edge(START, "add_one")
    builder.add_edge("add_one", "add_two")
    builder.add_edge("add_two", END)
    return builder.compile()


def main() -> None:
    graph = build()
    print(graph.invoke({"total": 0, "logs": []}))


if __name__ == "__main__":
    main()
