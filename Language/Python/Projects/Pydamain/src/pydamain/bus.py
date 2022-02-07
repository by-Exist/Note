from typing import (
    Awaitable,
    Callable,
    Concatenate,
    Generic,
    ParamSpec,
    TypeVar,
    Any,
    cast,
)
import asyncio
import inspect

from loguru import logger
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


P = ParamSpec("P")
Message = TypeVar("Message", bound=Command | Event)
Return = TypeVar("Return")


class Handler(Generic[Message, Return]):
    def __init__(
        self,
        func: Callable[Concatenate[Message, P], Return | Awaitable[Return]],
        dependencies: dict[str, Any],
    ):
        self.func = func
        self.func_dependencies = build_dependencies(self.func, dependencies)
        self.func_is_async = asyncio.iscoroutinefunction(self.func)

    async def __call__(self, msg: Message):
        try:
            logger.debug(f"Handling {msg} with handler {self.func.__name__}")
            if self.func_is_async:
                self.func = cast(
                    Callable[Concatenate[Message, P], Awaitable[Return]],
                    self.func,
                )
                return await self.func(msg, **self.func_dependencies)
            else:
                self.func = cast(
                    Callable[Concatenate[Message, P], Return], self.func
                )
                return await asyncio.to_thread(
                    self.func, msg, **self.func_dependencies
                )
        except Exception as e:
            logger.exception(f"Exception handling {msg}")
            raise e

    def __hash__(self):
        return hash(self.func)


class MessageBus:
    def __init__(
        self,
        dependencies: dict[str, Any],
    ):
        self.command_handler_map: dict[type[Command], Handler[Command]] = {}
        for command_sub_class in Command.command_sub_classes:
            if command_sub_class.handler:
                self.command_handler_map[command_sub_class] = Handler(
                    command_sub_class.handler, dependencies
                )
        self.event_handlers_map: dict[type[Event], set[Handler[Event]]] = {}
        for event_sub_class in Event.event_sub_classes:
            if event_sub_class.handlers:
                self.event_handlers_map[event_sub_class] = set(
                    Handler(handler, dependencies)
                    for handler in event_sub_class.handlers
                )

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
            handler = self.command_handler_map[type(command)]
            result = await handler(command)
        return result, event_catcher.events

    async def handle_event(self, event: Event):
        with EventContext() as event_catcher:
            handlers = self.event_handlers_map[type(event)]
            coros = [handler(event) for handler in handlers]
            result = await asyncio.gather(*coros, return_exceptions=True)
        return result, event_catcher.events
