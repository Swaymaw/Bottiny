# %%
import asyncio

from src.app.channels.console import render, resolve_button
from src.app.core.flow import Context, Flow
from src.app.core.models import Button, IncomingMessage
from src.app.core.types import Channels
from src.app.nodes.basic import StaticReplyNode
from src.app.nodes.buttons import ButtonsNode
from src.app.nodes.llm import LLMNode

flow = (
    Flow(start="menu")
    .add(
        ButtonsNode(
            "menu",
            text="What do you want to do?",
            buttons=[
                {"id": "chat", "label": "Chat with AI"},
                {"id": "book", "label": "Book appointment"},
            ],
        )
    )
    .add(LLMNode("llm"))
    .add(
        ButtonsNode(
            "book",
            text="Confirm booking?",
            buttons=[
                {"id": "yes", "label": "Yes"},
                {"id": "no", "label": "No"},
            ],
        )
    )
    .add(StaticReplyNode("booked", text="Booked!"))  # trivial node returning a message
    .add(StaticReplyNode("cancelled", text="Cancelled."))
    .connect("menu", "chat", "llm")
    .connect("menu", "book", "book")
    .connect("book", "yes", "booked")
    .connect("book", "no", "cancelled")
)


async def main():
    ctx = Context()
    pending: list[Button] = []
    while True:
        raw = input("you> ")
        msg = IncomingMessage(
            channel=Channels.Console,
            user_id="Swayam Singhal",
            text=raw,
            button_id=resolve_button(raw, pending),
        )
        outputs = await flow.handle(ctx, msg)
        pending = []
        for out in outputs:
            render(out)
            pending = out.buttons or pending


asyncio.run(main())
