# E-Commerce Support Chatbot

I built this as a lightweight CLI chatbot for small e-commerce stores. It uses the Anthropic Claude API to handle the repetitive stuff like order questions, returns, shipping times, so store owners don't have to.

Conversation history is passed on every request, so Claude actually remembers what was said earlier in the session but with history length limit.

---

## Demo

```
Support Bot — type 'exit' to quit

You: hey, i want to return something i bought

Bot: Sure! You have 30 days to return any item, no questions asked.
     Just send it back in the original packaging and the refund will
     hit your account within 3-5 business days. Need the return address?

You: how long does standard shipping take?

Bot: Standard shipping takes 5-7 business days. If you need it faster,
     express shipping gets it there in 1-2 days.
```

## Setup

```bash
git clone https://github.com/patrickzxdx/ecommerce-support-bot
cd ecommerce-support-bot
pip install -r requirements.txt
```

Set your API key:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Then run:

```bash
python chatbot.py
```

You can get a free API key at [console.anthropic.com](https://console.anthropic.com).

## Customizing for a real store

Everything the bot knows lives in the `SYSTEM_PROMPT` inside `chatbot.py`. Change the return policy, shipping times, store email and that's it, the bot adapts automatically.

## Stack

- Python 3.9+
- [anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)

## License

MIT
