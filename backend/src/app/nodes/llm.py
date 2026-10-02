from litellm import acompletion

from src.app.core.models import OutgoingMessage
from src.app.core.node import BaseNode, NodeResult, register
from src.app.utils.prompts import ASSISTANT_PROMPT


@register
class LLMNode(BaseNode):
    name = "llm"

    async def run(self, ctx, msg):
        model = self.config.get("model", "openai/ibm-granite/granite-4.3-3b-GGUF")
        system = self.config.get("system", ASSISTANT_PROMPT.format(user_id=msg.user_id))
        messages = [{"role": "system", "content": system}, *ctx.history]
        resp = await acompletion(model=model, api_base="http://192.168.1.34:8080/v1", messages=messages)
        return NodeResult(
            message=OutgoingMessage(
                text=resp.choices[0].message.content,
                metadata={"model": model},
            )
        )
