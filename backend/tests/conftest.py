import pytest

from src.app.core.models import Context, IncomingMessage
from src.app.core.types import Channels


@pytest.fixture
def ctx():
    return Context()


@pytest.fixture
def incoming_message():
    return IncomingMessage(channel=Channels.Telegram, user_id="123", name="Test User", text="Hello")
