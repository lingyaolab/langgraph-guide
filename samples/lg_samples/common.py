"""Shared helpers for the LangGraph 1.2.20 samples."""

from __future__ import annotations

import os

from langchain_core.language_models.fake_chat_models import (
    FakeListChatModel,
    FakeMessagesListChatModel,
)
from langchain_core.messages import AIMessage
from langchain_deepseek import ChatDeepSeek


def has_api_key() -> bool:
    return bool(os.getenv("DEEPSEEK_API_KEY"))


def get_model():
    """Return a real DeepSeek model when a key is present, else a fake one."""
    if has_api_key():
        return ChatDeepSeek(
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            api_key=os.environ["DEEPSEEK_API_KEY"],
            temperature=0,
        )
    return FakeListChatModel(responses=["这是离线假模型的固定回答。"])


def scripted_model(responses: list[AIMessage]) -> FakeMessagesListChatModel:
    """A deterministic model that returns the given AIMessages in order."""
    return FakeMessagesListChatModel(responses=responses)
