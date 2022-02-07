from __future__ import annotations

from contextvars import ContextVar
from datetime import datetime
from uuid import uuid4, UUID
from typing import (
    Any,
    Callable,
    ClassVar,
)
from weakref import WeakSet

from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True)
class BaseMessage:
    id: UUID = field(default_factory=uuid4)
    create_time: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True, kw_only=True)
class Command(BaseMessage):
    handler: ClassVar[Callable[..., Any] | None] = None
    command_sub_classes: ClassVar[WeakSet[type[Command]]] = WeakSet()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.command_sub_classes.add(cls)


@dataclass(frozen=True, kw_only=True)
class Event(BaseMessage):
    handlers: ClassVar[list[Callable[..., Any]]] = []
    event_sub_classes: ClassVar[WeakSet[type[Event]]] = WeakSet()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.event_sub_classes.add(cls)

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
