from __future__ import annotations
from cgitb import handler

from contextvars import ContextVar
from datetime import datetime
from uuid import uuid4, UUID
from typing import Any

from pydantic import BaseModel, Field, Extra


class BaseMessage(BaseModel):

    id: UUID = Field(default_factory=uuid4)
    create_time: datetime = Field(default_factory=datetime.now)

    class Config:
        # Class
        frozen = True
        # Initialization
        extra = Extra.ignore
        allow_population_by_field_name = True


class Command(BaseMessage):
    ...


events_context_var: ContextVar[list[Event]] = ContextVar("events_context_var")


class Event(BaseMessage):
    def issue(self):
        event_list = events_context_var.get()
        event_list.append(self)


class EventContext:

    __slots__ = "events", "token"

    def __init__(self):
        self.events: list[Event] = []

    def __enter__(self):
        self.token = events_context_var.set(list())
        return self

    def __exit__(self, *args: tuple[Any]):
        self.events.extend(events_context_var.get())
        events_context_var.reset(self.token)
