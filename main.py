import asyncio
import os
from dotenv import load_dotenv

# cognee 1.1.0 references starlette.status.HTTP_422_UNPROCESSABLE_CONTENT which
# was never added to starlette — patch it before importing cognee.
import starlette.status as _status
if not hasattr(_status, "HTTP_422_UNPROCESSABLE_CONTENT"):
    _status.HTTP_422_UNPROCESSABLE_CONTENT = 422

import cognee

load_dotenv()


async def main():
    api_base_url = os.environ["COGNEE_API_BASE_URL"]
    api_key = os.environ["COGNEE_API_KEY"]

    await cognee.serve(url=api_base_url, api_key=api_key)

    # Store knowledge
    await cognee.remember(
        "User prefers dark mode and concise answers.",
        datasets=["default_dataset"],
    )

    # Retrieve relevant context
    results = await cognee.recall(
        "What are the user preferences?",
        datasets=["default_dataset"],
    )
    for item in results:
        print(item.get("text") or item.get("search_result") or item)


if __name__ == "__main__":
    asyncio.run(main())
