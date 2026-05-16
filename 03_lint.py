"""
Stage 3: Lint / Knowledge Audit
Structured audit of what Cognee learned — like Andrej Karpathy's LLM.txt wiki.
7 sections: product, ICPs, prospects, competitive, best targets, winning signals, graph edges (dlt).
"""
import asyncio
from utils import setup
import cognee
from cognee.api.v1.search import SearchType


DATASETS = ["sdr_knowledge", "icp_profiles", "prospect_data"]

AUDIT_SECTIONS = [
    (
        "PRODUCT KNOWLEDGE",
        "What product does SkillAgents AI sell, how does it work, and who is it built for?",
    ),
    (
        "ICP DEFINITIONS",
        "What are the Ideal Customer Profiles (ICPs) defined in the knowledge base? "
        "List each with key firmographic and behavioral criteria.",
    ),
    (
        "PROSPECT LANDSCAPE",
        "List all prospect companies with their employee count, industry, ICP fit score, "
        "technology stack, and whether they are qualified targets.",
    ),
    (
        "COMPETITIVE CONTEXT",
        "Who are SkillAgents AI's main competitors and how does SkillAgents AI position "
        "against each of them?",
    ),
    (
        "BEST FIT TARGETS",
        "Which prospect companies are the highest priority targets and why? "
        "Which should be deprioritized and why?",
    ),
    (
        "WINNING SIGNALS",
        "What are the key buying signals and deal patterns that indicate a company is "
        "ready to buy SkillAgents AI?",
    ),
    (
        "GRAPH EDGES — dlt Structure",
        "Which companies share the same LMS vendor? What AI tools are being adopted "
        "across the highest-fit prospects, and what training gaps do they share?",
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


async def run_section(section: str, query: str):
    print(f"[{section}]")
    print(f"Q: {query}\n")

    results = await cognee.search(
        query_text=query,
        query_type=SearchType.GRAPH_COMPLETION,
    )

    if results:
        for item in results:
            text = extract_text(item)
            if text:
                print(f"A: {text}")
    else:
        print("A: (no results)")

    print("\n" + "─" * 70 + "\n")


async def main():
    await setup()

    print("\n" + "=" * 70)
    print("  COGNEE KNOWLEDGE AUDIT — SkillAgents AI GTM Brain")
    print("  What the knowledge graph learned from ingested sales data")
    print("  Vector store: Redis (local)  |  Structured data: dlt")
    print("=" * 70 + "\n")

    for section, query in AUDIT_SECTIONS:
        await run_section(section, query)

    print("=" * 70)
    print("  END OF KNOWLEDGE AUDIT")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
