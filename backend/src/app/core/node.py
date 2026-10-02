from abc import abstractmethod

from pydantic import BaseModel

from src.app.core.models import Context, IncomingMessage, OutgoingMessage


class NodeResult(BaseModel):
    message: OutgoingMessage | None = None
    port: str = "out"
    wait: bool = False


class BaseNode:
    name = ""

    def __init__(self, id: str, **config):
        self.id = id
        self.config = config

    @abstractmethod
    async def run(self, ctx: Context, msg: IncomingMessage) -> NodeResult:
        raise NotImplementedError


NODE_TYPES: dict[str, type[BaseNode]] = {}


def register(cls: type[BaseNode]) -> type[BaseNode]:
    NODE_TYPES[cls.name] = cls
    return cls
