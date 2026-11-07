"""Chapter 24: a tiny KB service with SSE.

Run: uvicorn lg_samples.s24_kb_service:app --reload
Then: curl -N -X POST localhost:8000/chat -H 'content-type: application/json' \
        -d '{"question":"退款政策是什么？","user_id":"alice","thread_id":"t-1"}'
"""

from __future__ import annotations

import json
from typing import Annotated, TypedDict
from operator import add

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

app = FastAPI()


class State(TypedDict):
    question: str
    citations: Annotated[list[str], add]
    answer: str


def retrieve(state: State) -> dict:
    return {"citations": ["refund.md"]}


def answer(state: State) -> dict:
    return {"answer": "根据 refund.md：7 天无理由退款。"}


def build():
    builder = StateGraph(State)
    builder.add_node("retrieve", retrieve)
    builder.add_node("answer", answer)
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "answer")
    builder.add_edge("answer", END)
    return builder.compile(checkpointer=InMemorySaver())


graph = build()


class ChatBody(BaseModel):
    question: str
    user_id: str = "alice"
    thread_id: str = "t-1"


@app.post("/chat")
async def chat(body: ChatBody):
    config = {"configurable": {"thread_id": body.thread_id, "user_id": body.user_id}}

    async def events():
        state = graph.invoke({"question": body.question, "citations": [], "answer": ""}, config)
        yield f"data: {json.dumps({'type': 'citations', 'data': state['citations']}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'type': 'token', 'text': state['answer']}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")
