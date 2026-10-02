from litellm import acompletion
from pydantic import ValidationError

from src.app.core.models import LLMReply, OutgoingMessage
from src.app.core.node import Ask, BaseNode, Done, register
from src.app.utils.prompts import ASSISTANT_PROMPT, FORMAT_HINT


@register
class LLMNode(BaseNode):
    name = "llm"

    @staticmethod
    def _parse(raw: str) -> OutgoingMessage:
        try:
            r = LLMReply.model_validate_json(raw)
            return OutgoingMessage(text=r.text, buttons=r.buttons)
        except ValidationError:
            return OutgoingMessage(text=raw)

    async def run(self, ctx):
        reply = None

        while True:
            expect = "button" if reply and reply.buttons else "text"
            msg = yield Ask(message=reply, expect=expect)

            if expect == "button":
                chosen = next((b for b in reply.buttons if b.id == msg.button_id), None)
                if chosen is None:
                    continue
                ctx.history[-1]["content"] = chosen.label

            system = self.config.get("system", ASSISTANT_PROMPT.format(user_id=msg.user_id)) + FORMAT_HINT

            resp = await acompletion(
                model=self.config.get("model", "openai/ibm-granite/granite-4.3-3b-GGUF"),
                api_base=self.config.get("api_base", "http://192.168.1.34:8080/v1"),
                messages=[{"role": "system", "content": system}, *ctx.history],
                response_format=LLMReply,
            )
            reply = self._parse(resp.choices[0].message.content)
            if not self.config.get("loop", True):
                break
        yield Done(message=reply)
