import os
import asyncio
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from prompts import SYSTEM_MESSAGE, USER_MESSAGES

load_dotenv()

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def main() -> None:
    message = await client.messages.create(
        max_tokens=1024,
        system=TEXT_INFERENCE_SYSTEM_MESSAGE,
        messages=TEXT_INFERENCE_PROMPT,
        model="claude-3-opus-20240229",
    )
    print(message.content)

asyncio.run(main())