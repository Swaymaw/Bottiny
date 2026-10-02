from abc import abstractmethod
from collections.abc import AsyncGenerator

from pydantic import BaseModel

from src.app.core.models import Context, IncomingMessage, OutgoingMessage


class Ask(BaseModel):
    message: OutgoingMessage | None = None
    expect: str = "text"


class Done(BaseModel):
    port: str = "out"
    message: OutgoingMessage | None = None


NodeGen = AsyncGenerator[Ask | Done, IncomingMessage | None]


class BaseNode:
    name: str = ""

    def __init__(self, id: str, **config):
        self.id = id
        self.config = config

    @abstractmethod
    def run(self, ctx: Context) -> NodeGen:
        raise NotImplementedError


NODE_TYPES: dict[str, type[BaseNode]] = {}


def register(cls: type[BaseNode]) -> type[BaseNode]:
    NODE_TYPES[cls.name] = cls
    return cls
