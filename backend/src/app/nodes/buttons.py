from src.app.core.models import Button, OutgoingMessage
from src.app.core.node import BaseNode, NodeResult, register


@register
class ButtonsNode(BaseNode):
    name = "buttons"

    async def run(self, ctx, msg):
        buttons = [Button(**b) for b in self.config["buttons"]]

        if ctx.resuming:
            if msg.button_id in {b.id for b in buttons}:
                return NodeResult(port=msg.button_id)  # route by button
            return NodeResult(  # invalid -> re-ask
                message=OutgoingMessage(text="Please pick one of the options.", buttons=buttons),
                wait=True,
            )

        return NodeResult(
            message=OutgoingMessage(text=self.config["text"], buttons=buttons),
            wait=True,
        )
