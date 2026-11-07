"""Chapter 03: conditional routing with an explicit path map."""

from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    route: str
    answer: str


def classify(state: State) -> dict:
    route = "billing" if "退款" in state["question"] else "general"
    return {"route": route}


def billing(state: State) -> dict:
    return {"answer": "进入退款流程"}


def general(state: State) -> dict:
    return {"answer": "进入通用回答"}


def pick(state: State) -> Literal["billing", "general"]:
    return state["route"]  # type: ignore[return-value]


def build():
    builder = StateGraph(State)
    builder.add_node("classify", classify)
    builder.add_node("billing", billing)
    builder.add_node("general", general)
    builder.add_edge(START, "classify")
    builder.add_conditional_edges(
        "classify",
        pick,
        {"billing": "billing", "general": "general"},
    )
    builder.add_edge("billing", END)
    builder.add_edge("general", END)
    return builder.compile()


def main() -> None:
    graph = build()
    print(graph.invoke({"question": "我要退款", "route": "", "answer": ""}))
    print(graph.invoke({"question": "你们几点上班", "route": "", "answer": ""}))


if __name__ == "__main__":
    main()
