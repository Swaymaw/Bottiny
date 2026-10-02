# %%

import asyncio

from dotenv import find_dotenv, load_dotenv

from src.app.channels.console import Console
from src.app.services.store import list_flows

# flow = (
#     Flow(start="intro")
#     .add(StaticReplyNode("intro", text="Welcome to Shashank's Dental Clinic\n\nHow can we help you today?"))
#     .add(
#         ButtonsNode(
#             "choose",
#             buttons=[
#                 {"id": "book", "label": "Book Appointment"},
#                 {"id": "cancel", "label": "Cancel Appointment"},
#                 {"id": "update", "label": "Update Appointment"},
#                 {"id": "gen", "label": "General Query"},
#             ],
#         )
#     )
#     .add(StaticReplyNode("book", text="You have booked an appointment"))
#     .add(StaticReplyNode("cancel", text="You have cancelled your appointment"))
#     .add(StaticReplyNode("update", text="You have updated your appointment"))
#     .add(StaticReplyNode("gen", text="Please let us know about your queries."))
#     .add(LLMNode("llm"))
#     .connect("intro", "out", "choose")
#     .connect("choose", "book", "book")
#     .connect("choose", "cancel", "cancel")
#     .connect("choose", "update", "update")
#     .connect("choose", "gen", "gen")
#     .connect("book", "out", "llm")
#     .connect("gen", "out", "llm")
# )

load_dotenv(find_dotenv(), override=True)


async def pick_flow() -> str:
    flows = await list_flows(only_enabled=True)
    if not flows:
        raise SystemExit("No enabled flows. Create one via the API first.")
    for i, f in enumerate(flows, 1):
        print(f"  [{i}] {f.name}")
    return flows[int(input("Which flow? > ")) - 1].name


name = asyncio.run(pick_flow())

Console(name, name="Swayam Singhal").run()
# Telegram(flow).run()
