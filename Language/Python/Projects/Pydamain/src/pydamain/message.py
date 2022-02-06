from __future__ import annotations

from contextvars import ContextVar
from datetime import datetime
from uuid import uuid4, UUID
from typing import Any, Callable, ClassVar
from weakref import WeakSet

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

    handler: ClassVar[Callable[..., Any]] | None = None
    command_sub_classes: ClassVar[WeakSet[type[Command]]] = WeakSet()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.command_sub_classes.add(cls)


events_context_var: ContextVar[list[Event]] = ContextVar("events_context_var")


class Event(BaseMessage):

    handlers: ClassVar[list[Callable[..., Any]]] = []
    event_sub_classes: ClassVar[WeakSet[type[Event]]] = WeakSet()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.event_sub_classes.add(cls)

    def issue(self):
        event_list = events_context_var.get()
        event_list.append(self)


class EventContext:
    def __init__(self):
        self.events: list[Event] = []

    def __enter__(self):
        self.token = events_context_var.set(list())
        return self

    def __exit__(self, *args: tuple[Any]):
        self.events.extend(events_context_var.get())
        events_context_var.reset(self.token)
