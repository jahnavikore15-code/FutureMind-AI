import os
from openai import AsyncOpenAI
from pathlib import Path
from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)
load_dotenv()

def qwen_is_configured() -> bool:
    load_dotenv(dotenv_path=_env_path, override=True)
    return bool(os.getenv("QWEN_API_KEY", "").strip())

async def ask_qwen(system_prompt: str, user_prompt: str) -> str:
    api_key = os.getenv("QWEN_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("QWEN_API_KEY is not configured")
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=os.getenv(
            "QWEN_BASE_URL",
            "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
        )
    )
    response = await client.chat.completions.create(
        model=os.getenv("QWEN_MODEL", "qwen-plus"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content or ""
