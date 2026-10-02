from pydantic import BaseModel

from src.app.core.models import Context, IncomingMessage, OutgoingMessage
from src.app.core.node import Ask, BaseNode


class FlowResult(BaseModel):
    outputs: list[OutgoingMessage]
    awaiting: str | None


class Flow:
    def __init__(self, start: str):
        self.start = start
        self.nodes: dict[str, BaseNode] = {}
        self.edges: dict[tuple[str, str], str] = {}

    def add(self, node: BaseNode):
        self.nodes[node.id] = node
        return self

    def connect(self, src: str, port: str, dst: str):
        self.edges[(src, port)] = dst
        return self

    def _enter(self, ctx, node_id):
        ctx.node_id = node_id
        ctx.gen = self.nodes[node_id].run(ctx)

    async def handle(self, ctx: Context, msg: IncomingMessage | None = None) -> FlowResult:
        outputs: list[OutgoingMessage] = []

        if ctx.gen is None:
            self._enter(ctx, self.start)
        else:
            if msg is None:
                raise ValueError("message cannot be none after yield")
            ctx.history.append({"role": "user", "content": msg.text})

        while True:
            event = await ctx.gen.asend(msg)
            msg = None

            if event.message:
                outputs.append(event.message)
                ctx.history.append({"role": "assistant", "content": event.message.text})

            if isinstance(event, Ask):
                return FlowResult(outputs=outputs, awaiting=event.expect)

            nxt = self.edges.get((ctx.node_id, event.port))
            if nxt is None:
                ctx.gen = ctx.node_id = None
                return FlowResult(outputs=outputs, awaiting=None)
            self._enter(ctx, nxt)
