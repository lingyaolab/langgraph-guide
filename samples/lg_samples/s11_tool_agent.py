"""Chapter 11: a deterministic tool loop without network access.

The fake model returns a tool call first, then a final answer.
"""

from __future__ import annotations

from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from .common import scripted_model


@tool
def get_weather(city: str) -> str:
    """Return a deterministic weather string for the sample."""
    return f"{city}: 18C, sunny"


def agent(state: MessagesState, model) -> dict:
    return {"messages": [model.invoke(state["messages"])]}


def build():
    model = scripted_model(
        [
            AIMessage(
                content="",
                tool_calls=[{"name": "get_weather", "args": {"city": "Beijing"}, "id": "call-1"}],
            ),
            AIMessage(content="北京 18C，晴。"),
        ]
    )

    builder = StateGraph(MessagesState)
    builder.add_node("agent", lambda state: agent(state, model))
    builder.add_node("tools", ToolNode([get_weather]))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    return builder.compile()


def main() -> None:
    graph = build()
    out = graph.invoke({"messages": [("user", "北京天气如何？")]})
    for message in out["messages"]:
        print(type(message).__name__, message.content)


if __name__ == "__main__":
    main()
