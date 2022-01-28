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
        command_type_func_mapping: dict[type[Command], Callable[..., Any]],
        event_type_funcs_mapping: dict[type[Event], list[Callable[..., Any]]],
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
            events = await asyncio.create_task(self.handle_command(m))
        else:
            events = await asyncio.create_task(self.handle_event(m))
        for event in events:
            asyncio.create_task(self.handle(event))

    async def handle_command(self, command: Command):
        with EventContext() as event_catcher:
            handler = self.command_type_handler_mapping[type(command)]
            await handler(command)
        return event_catcher.events

    async def handle_event(self, event: Event):
        with EventContext() as event_catcher:
            handlers = self.event_type_handlers_mapping[type(event)]
            coros = [handler(event) for handler in handlers]
            await asyncio.gather(*coros, return_exceptions=True)
        return event_catcher.events
