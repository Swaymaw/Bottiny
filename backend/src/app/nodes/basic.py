from src.app.core.models import OutgoingMessage
from src.app.core.node import BaseNode, NodeResult, register


@register
class StaticReplyNode(BaseNode):
    name = "static_reply"

    async def run(self, ctx, msg):
        return NodeResult(
            message=OutgoingMessage(text=self.config["text"]),
            wait=True,
        )
