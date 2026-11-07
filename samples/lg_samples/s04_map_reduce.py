"""Chapter 04: Send fan-out plus a reducer for map-reduce."""

from __future__ import annotations

from operator import add
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send


class State(TypedDict):
    docs: list[dict]
    summaries: Annotated[list[str], add]
    report: str


def fan_out(state: State):
    return [Send("summarize", {"doc": doc, "index": i}) for i, doc in enumerate(state["docs"])]


def summarize(payload: dict) -> dict:
    return {"summaries": [f'{payload["index"]}:{payload["doc"]["text"][:10]}']}


def merge(state: State) -> dict:
    return {"report": "\n".join(sorted(state["summaries"]))}


def build():
    builder = StateGraph(State)
    builder.add_node("summarize", summarize)
    builder.add_node("merge", merge)
    builder.add_conditional_edges(START, fan_out, ["summarize"])
    builder.add_edge("summarize", "merge")
    builder.add_edge("merge", END)
    return builder.compile()


def main() -> None:
    graph = build()
    docs = [{"id": "a", "text": "alpha document"}, {"id": "b", "text": "beta document"}]
    print(graph.invoke({"docs": docs, "summaries": [], "report": ""}))


if __name__ == "__main__":
    main()
