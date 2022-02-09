from __future__ import annotations

from contextvars import ContextVar
from datetime import datetime
from uuid import uuid4, UUID
from typing import Any

from pydantic import BaseModel, Field


class BaseMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    create_time: datetime = Field(default_factory=datetime.now)

    class Config:
        frozen = True


class Command(BaseMessage):
    ...


class Event(BaseMessage):
    def issue(self):
        event_list = _events_context_var.get()
        event_list.append(self)


_events_context_var: ContextVar[list[Event]] = ContextVar(
    "_events_context_var"
)


class EventContext:
    def __init__(self):
        self.events: list[Event] = []

    def __enter__(self):
        self.token = _events_context_var.set(list())
        return self

    def __exit__(self, *args: tuple[Any]):
        self.events.extend(_events_context_var.get())
        _events_context_var.reset(self.token)
