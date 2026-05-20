"""CLI entry point for Kitty World Shop customer service bot."""

import sys

from dotenv import load_dotenv

from src.cs_bot.bot import CustomerServiceBot

load_dotenv()

BANNER = """
╔══════════════════════════════════════════════════════╗
║      🎀  Kitty World Shop — Customer Service  🎀     ║
║  Type your question below. Type 'quit' to exit.      ║
║  Type 'reset' to start a new conversation.           ║
╚══════════════════════════════════════════════════════╝
"""


def run_cli() -> None:
    print(BANNER)

    try:
        bot = CustomerServiceBot()
    except ValueError as exc:
        print(f"[Error] {exc}")
        sys.exit(1)

    # Opening greeting
    greeting = bot.chat("Hello! Please greet me as a new customer.")
    print(f"Kitty: {greeting}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Have a great day~ 🎀")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print(
                "Kitty: Thank you for visiting Kitty World Shop! Have a great day~ 🎀"
            )
            break

        if user_input.lower() == "reset":
            bot.reset()
            print("--- New conversation started ---\n")
            greeting = bot.chat("Hello! Please greet me as a new customer.")
            print(f"Kitty: {greeting}\n")
            continue

        response = bot.chat(user_input)
        print(f"\nKitty: {response}\n")


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()
