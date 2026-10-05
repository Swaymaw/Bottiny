from unittest.mock import AsyncMock, patch

import pytest

from src.app.core.models import IncomingMessage, OutgoingMessage
from src.app.core.node import Ask, Done
from src.app.core.types import Channels
from src.app.nodes.basic import StaticReplyNode
from src.app.nodes.buttons import ButtonsNode
from src.app.nodes.llm import LLMNode


@pytest.mark.asyncio
async def test_static_reply_node(ctx):
    """Test that StaticReplyNode returns the configured text and finishes."""
    node = StaticReplyNode(id="node_1", text="Hello from test!")
    gen = node.run(ctx)

    result = await gen.__anext__()
    assert isinstance(result, Done)
    assert isinstance(result.message, OutgoingMessage)
    assert result.message.text == "Hello from test!"


@pytest.mark.asyncio
async def test_buttons_node(ctx):
    """Test that ButtonsNode asks for a button and finishes when the button is clicked."""
    node = ButtonsNode(id="node_2", text="Choose:", buttons=[{"id": "yes", "label": "Yes"}])
    gen = node.run(ctx)

    # First yield should be Ask
    ask = await gen.__anext__()
    assert isinstance(ask, Ask)
    assert ask.expect == "button"
    assert isinstance(ask.message, OutgoingMessage)
    assert ask.message.text == "Choose:"

    # Simulate user clicking the button
    msg = IncomingMessage(channel=Channels.Telegram, user_id="user_1", name="Tester", text="Yes", button_id="yes")

    done = await gen.asend(msg)
    assert isinstance(done, Done)
    assert done.port == "yes"


@pytest.mark.asyncio
async def test_llm_node(ctx, incoming_message):
    """Test that LLMNode calls the LLM and returns the response."""
    node = LLMNode(id="node_3", system="You are a test bot", loop=False)
    gen = node.run(ctx)

    # First yield is an empty Ask because reply is initially None
    ask = await gen.__anext__()
    assert isinstance(ask, Ask)
    assert ask.message is None

    # Mock litellm completion
    with patch("src.app.nodes.llm.acompletion", new_callable=AsyncMock) as mock_completion:
        mock_completion.return_value.choices[0].message.content = '{"text": "I am a helpful assistant."}'

        # Send a message to trigger the LLM call
        done = await gen.asend(incoming_message)

        assert isinstance(done, Done)
        assert isinstance(done.message, OutgoingMessage)
        assert done.message.text == "I am a helpful assistant."
        mock_completion.assert_awaited_once()
