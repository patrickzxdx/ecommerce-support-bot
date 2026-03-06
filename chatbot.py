import os
import anthropic

client = anthropic.Anthropic()

# Keeping the prompt tight — the more specific, the less hallucination
SYSTEM_PROMPT = """You are a support agent for a small online store. Keep answers short and helpful.

What you can help with:
- Order status and tracking
- Returns and refunds (30-day window, no questions asked)
- Shipping times (Standard: 5-7 days, Express: 1-2 days)
- General store questions

Store info:
- Free shipping on orders over $50
- Refunds hit the account in 3-5 business days
- If something's outside your scope, point them to support@example-store.com

Don't over-explain. One or two sentences is usually enough.
"""

# Keep the last N pairs (user + assistant) to avoid bloating the context window.
# 10 pairs is plenty for a support session and stays well under token limits.
MAX_HISTORY_PAIRS = 10


def trim_history(history):
    """Drop oldest messages if history gets too long. Always keeps pairs intact."""
    max_messages = MAX_HISTORY_PAIRS * 2
    if len(history) > max_messages:
        history = history[-max_messages:]
    return history


def ask(history):
    try:
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=history
        )
        return resp.content[0].text

    except anthropic.AuthenticationError:
        return "ERROR: invalid API key. Check your ANTHROPIC_API_KEY."

    except anthropic.RateLimitError:
        return "Slow down! Rate limit hit — wait a few seconds and try again."

    except anthropic.APIStatusError as e:
        # Catches 5xx and other unexpected API errors
        return f"API error ({e.status_code}): {e.message}"

    except anthropic.APIConnectionError:
        return "Couldn't reach the API — check your internet connection."


def chat():
    history = []

    print("\nSupport Bot — type 'exit' to quit\n")

    while True:
        user_msg = input("You: ").strip()

        if not user_msg:
            continue

        if user_msg.lower() in ["exit", "quit", "bye"]:
            print("Bot: Take care!")
            break

        history.append({"role": "user", "content": user_msg})
        history = trim_history(history)

        reply = ask(history)
        print(f"Bot: {reply}\n")

        # Only store the reply in history if the API call actually worked
        if not reply.startswith("ERROR") and not reply.startswith("Couldn't"):
            history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Missing ANTHROPIC_API_KEY — set it before running.")
        exit(1)

    chat()

