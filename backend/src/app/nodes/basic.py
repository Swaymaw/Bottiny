from src.app.core.models import OutgoingMessage
from src.app.core.node import BaseNode, Done, register


@register
class StaticReplyNode(BaseNode):
    name = "static"

    async def run(self, ctx):
        yield Done(message=OutgoingMessage(text=self.config["text"]))
