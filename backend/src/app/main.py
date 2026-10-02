# %%
import asyncio

from src.app.channels.console import ask_input, render, resolve_button
from src.app.core.flow import Context, Flow
from src.app.core.models import Button, IncomingMessage
from src.app.core.types import Channels
from src.app.nodes.basic import StaticReplyNode
from src.app.nodes.buttons import ButtonsNode
from src.app.nodes.llm import LLMNode

flow = (
    Flow(start="intro")
    .add(StaticReplyNode("intro", text="Welcome to Shashank's Dental Clinic\n\nHow can we help you today?"))
    .add(
        ButtonsNode(
            "choose",
            text="What do you want to do?",
            buttons=[
                {"id": "book", "label": "Book Appointment"},
                {"id": "cancel", "label": "Cancel Appointment"},
                {"id": "update", "label": "Update Appointment"},
                {"id": "gen", "label": "General Query"},
            ],
        )
    )
    .add(StaticReplyNode("book", text="You have booked an appointment"))
    .add(StaticReplyNode("cancel", text="You have cancelled your appointment"))
    .add(StaticReplyNode("update", text="You have updated your appointment"))
    .add(StaticReplyNode("gen", text="Please let us know about your queries."))
    .add(LLMNode("llm"))
    .connect("intro", "out", "choose")
    .connect("choose", "book", "book")
    .connect("choose", "cancel", "cancel")
    .connect("choose", "update", "update")
    .connect("choose", "gen", "gen")
    .connect("book", "out", "llm")
    .connect("gen", "out", "llm")
)


async def main():
    ctx = Context()
    result = await flow.handle(ctx)  # flow speaks first, no user input
    pending: list[Button] = []

    while True:
        for out in result.outputs:
            render(out)
            pending = out.buttons or pending

        if result.awaiting is None:  # flow finished
            print("-- flow finished --")
            break

        raw = ask_input()
        msg = IncomingMessage(
            channel=Channels.Console,
            user_id="Swayam Singhal",
            text=raw,
            button_id=resolve_button(raw, pending) if result.awaiting == "button" else None,
        )
        result = await flow.handle(ctx, msg)
        pending = []  # buttons are only valid for the next reply


asyncio.run(main())
