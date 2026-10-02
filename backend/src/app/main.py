# %%

from dotenv import find_dotenv, load_dotenv

from src.app.channels.telegram import Telegram
from src.app.core.flow import Flow
from src.app.nodes.basic import StaticReplyNode
from src.app.nodes.buttons import ButtonsNode
from src.app.nodes.llm import LLMNode

flow = (
    Flow(start="intro")
    .add(StaticReplyNode("intro", text="Welcome to Shashank's Dental Clinic\n\nHow can we help you today?"))
    .add(
        ButtonsNode(
            "choose",
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

load_dotenv(find_dotenv())

# Console(flow, name="Swayam Singhal").run()
Telegram(flow).run()
