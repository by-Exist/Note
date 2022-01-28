from typing import (
    Awaitable,
    Callable,
    Concatenate,
    Coroutine,
    Generic,
    Mapping,
    MutableMapping,
    ParamSpec,
    Protocol,
    Sequence,
    TypeGuard,
    TypeVar,
    Any,
    TypedDict,
    cast,
    overload,
)
import asyncio
import inspect

from pydamain import Command, Event
from pydamain.message import EventContext


def build_dependencies(
    func: Callable[..., Any],
    dependencies: dict[str, Any],
):
    params = inspect.signature(func).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return deps


M = TypeVar("M", bound=Command | Event)
P = ParamSpec("P")
R = TypeVar("R")


class Handler(Generic[M, P, R]):
    def __init__(
        self,
        func: Callable[Concatenate[M, P], R | Awaitable[R]],
        dependencies: dict[str, Any],
    ):
        self.func = func
        self.injected_dependencies = dependencies
        self.func_is_async = asyncio.iscoroutinefunction(self.func)
        self.ready = False

    def start_up(self):
        if self.ready:
            return
        self.func_dependencies = build_dependencies(
            self.func, self.injected_dependencies
        )
        del self.injected_dependencies
        self.ready = True

    async def __call__(self, msg: M):
        if not self.ready:
            raise RuntimeError(
                "Handler는 MessageBus의 start_up이 수행될 때 까지 호출할 수 없습니다."
            )
        if self.func_is_async:
            self.func = cast(
                Callable[Concatenate[M, P], Awaitable[R]], self.func
            )
            return await self.func(msg, **self.func_dependencies)
        else:
            self.func = cast(Callable[Concatenate[M, P], R], self.func)
            return await asyncio.to_thread(
                self.func, msg, **self.func_dependencies
            )

    def __hash__(self):
        return hash(self.func)


class TC1(Command):
    ...


class TC2(Command):
    ...


def test1(c: TC1, x: int) -> str:
    ...


async def test2(c: Command, x: int) -> float:
    ...


async def _():
    message_bus = MessageBus({}, {}, {})
    result = await message_bus.handle(TC1())


class MessageBus:
    def __init__(
        self,
        dependencies: dict[str, Any],
        command_type_func_mapping: dict[type[Command], Callable[..., Any]],
        event_type_funcs_mapping: dict[
            type[Event], Sequence[Callable[..., Any]]
        ],
    ):
        self.dependencies = dependencies
        self.command_type_handler_mapping = {
            name: Handler(value, dependencies)
            for name, value in command_type_func_mapping.items()
        }
        self.event_type_handlers_mapping = {
            name: set(Handler(value, dependencies) for value in values)
            for name, values in event_type_funcs_mapping.items()
        }

    async def handle(self, m: Command | Event):
        if isinstance(m, Command):
            result, events = await asyncio.create_task(self.handle_command(m))
        else:
            result, events = await asyncio.create_task(self.handle_event(m))
        for event in events:
            asyncio.create_task(self.handle(event))
        return result

    async def handle_command(self, command: Command):
        with EventContext() as event_catcher:
            handler = self.command_type_handler_mapping[type(command)]
            result = await handler(command)
        return result, event_catcher.events

    async def handle_event(self, event: Event):
        with EventContext() as event_catcher:
            handlers = self.event_type_handlers_mapping[type(event)]
            coros = [handler(event) for handler in handlers]
            result = await asyncio.gather(*coros)
        return result, event_catcher.events
