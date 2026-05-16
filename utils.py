import starlette.status as _status
if not hasattr(_status, "HTTP_422_UNPROCESSABLE_CONTENT"):
    _status.HTTP_422_UNPROCESSABLE_CONTENT = 422

# Load env vars BEFORE importing cognee so LLM_API_KEY is visible at startup
import os
from dotenv import load_dotenv
load_dotenv()

import cognee  # noqa: E402 — must be after load_dotenv()


async def setup():
    openai_key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    if not openai_key:
        raise EnvironmentError(
            "LLM_API_KEY not set in .env — required for local entity extraction"
        )
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    print(f"  Config: Redis={redis_url}  LLM key=...{openai_key[-6:]}")
