from pydantic import BaseModel, Field

from src.app.core.types import Channels


class Button(BaseModel):
    id: str
    label: str


class Context:
    def __init__(self):
        self.history: list[dict] = []
        self.cursor: str | None = None
        self.resuming: bool = False


class IncomingMessage(BaseModel):
    channel: Channels
    user_id: str
    text: str
    button_id: str | None = None


class OutgoingMessage(BaseModel):
    text: str
    buttons: list[Button] = Field(default_factory=list)
    metadata: dict | None = None
