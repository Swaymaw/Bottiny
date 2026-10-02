from pydantic import BaseModel, Field

from src.app.core.types import Channels


class Button(BaseModel):
    id: str
    label: str


class Context:
    def __init__(self):
        self.history = []
        self.node_id = None
        self.gen = None


class IncomingMessage(BaseModel):
    channel: Channels
    user_id: str
    name: str
    text: str
    button_id: str | None = None


class OutgoingMessage(BaseModel):
    text: str
    buttons: list[Button] = Field(default_factory=list)
    metadata: dict | None = None


class LLMReply(BaseModel):
    text: str
    buttons: list[Button] = Field(default_factory=list)
