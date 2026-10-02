# src/app/channels/base.py
from abc import ABC, abstractmethod

from src.app.core.flow import Context, Flow
from src.app.core.models import Button, IncomingMessage, OutgoingMessage
from src.app.core.types import Channels


class Session:
    def __init__(self):
        self.ctx = Context()
        self.pending: list[Button] = []
        self.awaiting: str | None = None


class Channel(ABC):
    channel: Channels

    def __init__(self, flow: Flow):
        self.flow = flow
        self.sessions: dict[str, Session] = {}

    @abstractmethod
    async def render(self, target, out: OutgoingMessage) -> None:
        pass

    def resolve_button(self, raw: str, buttons: list[Button]) -> tuple[str, bool]:
        cleaned_raw = raw.strip().lower()
        for i, b in enumerate(buttons, 1):
            if cleaned_raw in (str(i), b.id.lower(), b.label.lower()):
                return b.id, True
        return raw, False

    async def process(self, user_id: str, name: str, raw: str, target, restart: bool = False):
        if restart:
            self.sessions.pop(user_id, None)

        s = self.sessions.get(user_id)
        if s is None:
            s = self.sessions[user_id] = Session()
            result = await self.flow.handle(s.ctx)
        else:
            correct = False
            if s.awaiting == "button":
                raw, correct = self.resolve_button(raw, s.pending)

            msg = IncomingMessage(
                channel=self.channel,
                user_id=user_id,
                name=name,
                text=raw,
                button_id=raw if correct else None,
            )
            if correct:
                chosen = next((i for i in s.pending if i.id == raw), None)
                if chosen:
                    await self.render(target, OutgoingMessage(text=f"You chose {chosen.label}"))

            result = await self.flow.handle(s.ctx, msg)

        s.pending = []
        for out in result.outputs:
            await self.render(target, out)
            s.pending = out.buttons or s.pending
        s.awaiting = result.awaiting

        if result.awaiting is None:
            self.sessions.pop(user_id, None)

    @abstractmethod
    def run(self) -> None:
        pass
