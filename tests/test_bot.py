from unittest.mock import MagicMock, patch

import pytest

from src.cs_bot.bot import CustomerServiceBot, build_system_prompt


def test_build_system_prompt_contains_required_sections():
    prompt = build_system_prompt()
    assert "Hello Kitty" in prompt
    assert "Kitty World Shop" in prompt
    assert "Shipping" in prompt
    assert "Return" in prompt


def test_build_system_prompt_contains_catalog():
    prompt = build_system_prompt()
    assert "Plush Toys" in prompt
    assert "$" in prompt


def test_bot_raises_without_api_key():
    with patch.dict("os.environ", {}, clear=True):
        # Remove key if present
        import os

        os.environ.pop("ANTHROPIC_API_KEY", None)
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
            CustomerServiceBot()


def _make_mock_bot() -> CustomerServiceBot:
    """Create a bot with a mocked Anthropic client."""
    with patch("src.cs_bot.bot.anthropic.Anthropic") as mock_anthropic:
        bot = CustomerServiceBot(api_key="test-key-123")
    bot._client = mock_anthropic.return_value
    return bot


def test_bot_chat_sends_user_message():
    bot = _make_mock_bot()

    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Hello! How can I help?")]
    bot._client.messages.create.return_value = mock_response

    reply = bot.chat("Hi there")

    assert reply == "Hello! How can I help?"
    assert bot.turn_count == 1


def test_bot_history_grows_with_turns():
    bot = _make_mock_bot()

    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Response")]
    bot._client.messages.create.return_value = mock_response

    bot.chat("Message 1")
    bot.chat("Message 2")

    assert bot.turn_count == 2
    # history has user+assistant pairs
    assert len(bot._history) == 4


def test_bot_reset_clears_history():
    bot = _make_mock_bot()

    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Response")]
    bot._client.messages.create.return_value = mock_response

    bot.chat("Hello")
    assert bot.turn_count == 1

    bot.reset()
    assert bot.turn_count == 0
    assert bot._history == []


def test_bot_passes_full_history_to_api():
    bot = _make_mock_bot()

    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Resp")]
    bot._client.messages.create.return_value = mock_response

    bot.chat("First message")
    bot.chat("Second message")

    call_args = bot._client.messages.create.call_args
    messages_sent = call_args.kwargs["messages"]
    # Should include all history: user1, assistant1, user2
    assert len(messages_sent) == 3
    assert messages_sent[0]["role"] == "user"
    assert messages_sent[1]["role"] == "assistant"
    assert messages_sent[2]["role"] == "user"
