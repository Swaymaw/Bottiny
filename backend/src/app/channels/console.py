# src/app/channels/console.py
import asyncio

from src.app.channels.base import Channel
from src.app.core.types import Channels


class Console(Channel):
    channel = Channels.Console

    def __init__(self, flow_name, name: str = "Console User"):
        super().__init__(flow_name)
        self.user_id = "console"
        self.name = name

    async def render(self, target, out):
        print(f"assistant> {out.text}")
        for i, b in enumerate(out.buttons, 1):
            print(f"  [{i}] {b.label}")
        if out.buttons:
            print(f"  press <1-{len(out.buttons)}> + enter")

    def run(self):
        asyncio.run(self._loop())

    async def _loop(self):
        await self.process(self.user_id, self.name, "", None)

        while self.user_id in self.sessions:
            raw = input("you> ")
            await self.process(self.user_id, self.name, raw, None)

        print("-- flow finished --")
