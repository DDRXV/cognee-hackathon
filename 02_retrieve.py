"""
Stage 2: Retrieval (Local Mode)
Agentic multi-step reasoning over the ingested knowledge graph.
Uses AGENTIC_COMPLETION (reasoning loop) with fallback to GRAPH_COMPLETION.
"""
import asyncio
from utils import setup
import cognee
from cognee.api.v1.search import SearchType


DATASETS = ["sdr_knowledge", "icp_profiles", "prospect_data"]

QUERIES = [
    (
        "ICP MATCH RANKING",
        "Which prospect companies best match our Ideal Customer Profile for SkillAgents AI? "
        "Rank them from highest to lowest fit and explain the reasoning for each.",
    ),
    (
        "OUTREACH ANGLE — BuildFast SaaS",
        "What is the best personalized outreach angle for BuildFast SaaS based on their recent "
        "activity, technology stack, and our SkillAgents AI value proposition?",
    ),
    (
        "OBJECTION PREP — GlobalBank Corp",
        "What objections might GlobalBank Corp raise when evaluating SkillAgents AI, "
        "and how should we respond to each objection specifically?",
    ),
]


def extract_text(result) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        return (
            result.get("text")
            or result.get("search_result")
            or str(result.get("raw", {}).get("value", result))
        )
    return str(result)


async def run_query(label: str, query: str):
    print(f"[{label}]")
    print(f"Query: {query}\n")

    results = await cognee.search(
        query_text=query,
        query_type=SearchType.GRAPH_COMPLETION,
    )

    if results:
        for item in results:
            text = extract_text(item)
            if text:
                print(text)
    else:
        print("(no results)")

    print("\n" + "─" * 70 + "\n")


async def main():
    await setup()
    print("\n=== STAGE 2: RETRIEVAL ===\n")
    for label, query in QUERIES:
        await run_query(label, query)


if __name__ == "__main__":
    asyncio.run(main())
