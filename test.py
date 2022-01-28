from __future__ import annotations

from contextvars import ContextVar
from datetime import datetime, date, timedelta
from dataclasses import dataclass, field, asdict
from uuid import uuid4, UUID
import json

from typing import (
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Generic,
    TypeVar,
    ParamSpec,
)


C = TypeVar("C")
P = ParamSpec("P")


class MessageEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, UUID):
            return o.hex
        return super().default(o)


@dataclass(frozen=True)
class BaseMessage:
    id: UUID = field(default_factory=uuid4)
    create_time: datetime = field(default_factory=datetime.now)

    handlers: ClassVar[Callable[..., Any | Awaitable[Any]]]

    def to_json(self):
        return json.dumps(asdict(self), cls=MessageEncoder)

    @classmethod
    def from_json(cls, raw: str):
        return cls(**json.loads(raw))


m = BaseMessage()
print(m)
j = m.to_json()
print(j)
m2 = BaseMessage.from_json(j)
print(m2)
