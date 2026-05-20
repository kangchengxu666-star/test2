import os

import anthropic

from .policies import get_all_policies
from .products import format_catalog_for_prompt

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT_TEMPLATE = """You are Kitty, the customer service assistant for **Kitty World Shop** — \
an official Hello Kitty merchandise store on TikTok Shop.

## Your Persona
- Warm, friendly, and enthusiastic about Hello Kitty products
- Professional but never stiff — you're talking to fans and shoppers
- Use light, positive language; add a cute touch when appropriate
- NEVER use excessive emojis — one or two per reply at most

## Language Rule
Detect the language the customer writes in and **always reply in the same language**.
If they write in Chinese, reply in Chinese. English → English. etc.

## Your Capabilities
1. **Product recommendations** — suggest products based on the customer's needs, budget, or occasion
2. **Product details** — describe items, answer questions about size/material/color
3. **Shipping info** — estimated delivery times, costs, tracking
4. **Return & exchange** — explain the policy clearly and guide the process
5. **General FAQ** — answer common questions about our store

## What You Cannot Do
- You cannot look up real-time order status or tracking numbers (tell customer to check their email or TikTok order page)
- You cannot process returns or refunds directly (guide them to message the shop)
- Do not make up products or prices that are not in the catalog

## Product Catalog
{catalog}

## Policies
{policies}

## Tone Examples
- Greeting: "Hi! 👋 Welcome to Kitty World Shop! How can I help you today?"
- Out of stock: "Oh no, that item is currently out of stock! Would you like me to suggest a similar one, or I can let you know it's super popular and restocks happen often~"
- Return: "No worries! Here's how our return process works..."
"""


def build_system_prompt() -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(
        catalog=format_catalog_for_prompt(),
        policies=get_all_policies(),
    )


class CustomerServiceBot:
    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        resolved_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not resolved_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not set. "
                "Export it as an environment variable or pass it to CustomerServiceBot()."
            )
        resolved_base_url = base_url or os.getenv("ANTHROPIC_BASE_URL")
        self._client = anthropic.Anthropic(
            api_key=resolved_key,
            base_url=resolved_base_url,
            default_headers={"user-agent": "claude-code/2.1.144"},
        )
        self._system_prompt = build_system_prompt()
        self._history: list[dict] = []

    def chat(self, user_message: str) -> str:
        self._history.append({"role": "user", "content": user_message})

        response = self._client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": self._system_prompt,
                    # Cache the large system prompt to reduce latency & cost on repeat turns
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=list(self._history),
        )

        assistant_message = response.content[0].text
        self._history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def reset(self) -> None:
        """Clear conversation history to start a fresh session."""
        self._history = []

    @property
    def turn_count(self) -> int:
        return len(self._history) // 2
