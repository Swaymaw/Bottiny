# %%

import asyncio

from dotenv import find_dotenv, load_dotenv

from src.app.channels.console import Console
from src.app.services.store import list_flows

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
