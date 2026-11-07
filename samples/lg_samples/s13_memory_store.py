"""Chapter 13: cross-thread preferences in a Store."""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.store.memory import InMemoryStore


class State(TypedDict):
    user_id: str
    action: str
    tone: str
    message: str


def remember(state: State, store) -> dict:
    if state["action"] == "remember":
        store.put(("users", state["user_id"]), "preference", {"tone": "concise"})
        return {"tone": "concise", "message": "记住了"}
    return {}


def recall(state: State, store) -> dict:
    item = store.get(("users", state["user_id"]), "preference")
    tone = item.value["tone"] if item else "default"
    return {"tone": tone, "message": f"当前语气：{tone}"}


def build():
    store = InMemoryStore()
    builder = StateGraph(State)
    builder.add_node("remember", remember)
    builder.add_node("recall", recall)
    builder.add_edge(START, "remember")
    builder.add_edge("remember", "recall")
    builder.add_edge("recall", END)
    return builder.compile(store=store)


def main() -> None:
    graph = build()
    base = {"user_id": "alice", "action": "remember", "tone": "", "message": ""}
    print(graph.invoke(base))
    print(graph.invoke({**base, "action": "recall"}))

    bob = {"user_id": "bob", "action": "recall", "tone": "", "message": ""}
    print(graph.invoke(bob))


if __name__ == "__main__":
    main()
