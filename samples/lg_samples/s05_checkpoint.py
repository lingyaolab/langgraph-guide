"""Chapter 05: multi-turn state with a checkpointer."""

from __future__ import annotations

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph


def echo(state: MessagesState) -> dict:
    last = state["messages"][-1]
    return {"messages": [("ai", f"你说了：{last.content}")]}


def build():
    builder = StateGraph(MessagesState)
    builder.add_node("echo", echo)
    builder.add_edge(START, "echo")
    builder.add_edge("echo", END)
    return builder.compile(checkpointer=InMemorySaver())


def main() -> None:
    graph = build()
    config = {"configurable": {"thread_id": "user-1"}}
    graph.invoke({"messages": [("user", "我叫 Alice")]}, config)
    out = graph.invoke({"messages": [("user", "我叫什么？")]}, config)
    print(out["messages"][-1].content)
    print("messages:", len(out["messages"]))


if __name__ == "__main__":
    main()
