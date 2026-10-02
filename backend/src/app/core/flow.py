from src.app.core.models import Context, IncomingMessage, OutgoingMessage
from src.app.core.node import BaseNode


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

    async def handle(self, ctx: Context, msg: IncomingMessage) -> list[OutgoingMessage]:
        outputs: list[OutgoingMessage] = []
        ctx.history.append({"role": "user", "content": msg.text})

        node_id = ctx.cursor or self.start
        ctx.resuming = ctx.cursor is not None
        ctx.cursor = None

        while True:
            result = await self.nodes[node_id].run(ctx, msg)
            ctx.resuming = False

            if result.message:
                outputs.append(result.message)
                ctx.history.append({"role": "assistant", "content": result.message.text})

            if result.wait:
                ctx.cursor = node_id
                return outputs

            nxt = self.edges.get((node_id, result.port))
            if nxt is None:
                return outputs
            node_id = nxt
