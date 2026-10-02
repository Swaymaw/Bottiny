from src.app.core.models import Button, OutgoingMessage
from src.app.core.node import Ask, BaseNode, Done, NodeGen, register


@register
class ButtonsNode(BaseNode):
    name = "buttons"

    async def run(self, ctx) -> NodeGen:
        buttons = [Button(**b) for b in self.config["buttons"]]
        ids = {b.id for b in buttons}
        text = self.config.get("text", "Please pick one of the options.")

        msg = yield Ask(message=OutgoingMessage(text=text, buttons=buttons), expect="button")

        if msg is None:
            raise ValueError("msg cannot be empty after ask")

        while msg.button_id not in ids:
            msg = yield Ask(message=OutgoingMessage(text=text, buttons=buttons), expect="button")
            if msg is None:
                raise ValueError("msg cannot be empty after ask")

        yield Done(port=msg.button_id)
