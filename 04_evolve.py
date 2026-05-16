"""
Stage 4: Self-Evolution
Simulates two deal outcomes flowing in, demonstrating the two-layer memory architecture:

  Redis  → real-time signal cache (fast write, ephemeral buffer)
  Cognee → persistent knowledge graph (permanent, queryable across sessions)

Outcomes hit Redis first (like a CRM event stream), then get crystallised into
Cognee's graph so every future SDR can benefit from the learned patterns.
"""
import asyncio
import os
import json
import redis as redis_lib
from datetime import datetime
from utils import setup
import cognee
from cognee.api.v1.search import SearchType


QUERY = (
    "What is the best personalized outreach angle for BuildFast SaaS based on "
    "their recent activity, technology stack, and our SkillAgents AI value proposition?"
)

DEAL_OUTCOMES = [
    {
        "id": "deal-001",
        "company": "BuildFast SaaS",
        "result": "CLOSED WON",
        "arr": 120000,
        "contact": "Ben Alvarez (CTO)",
        "what_worked": (
            "ROI quantification tied to CTO's own LinkedIn post about Cursor AI adoption gap. "
            "Email opened: 'Your 400 engineers average 4 months to full productivity — $240K per hire in ramp cost. "
            "SkillAgents cuts that to 6 weeks.' Reply in 4 hours. 14-day pilot, 88% completion, converted to annual."
        ),
        "lesson": (
            "ICP B CTOs respond to ROI math anchored to their public statements. "
            "Lead with their words back to them. Pitch cost of inaction, not features. "
            "Close time: 18 days."
        ),
    },
    {
        "id": "deal-002",
        "company": "GlobalBank Corp",
        "result": "STALLED",
        "arr": 0,
        "contact": "Sarah Mitchell (CHRO)",
        "what_worked": "N/A — deal paused before demo.",
        "lesson": (
            "Enterprise Financial Services (ICP A) requires SOC2 Type II report, "
            "EU data residency options, and GDPR compliance brief BEFORE the first call. "
            "Send compliance collateral in the intro email — do not wait for them to ask. "
            "Legal blocks any deal that isn't pre-cleared on security."
        ),
    },
]

OUTCOMES_TEXT = """
DEAL OUTCOME LOG — SkillAgents AI Field Intelligence
=====================================================

DEAL #1 — BuildFast SaaS — CLOSED WON — $120,000 ARR
Contact: Ben Alvarez (CTO) and Keisha Thompson (Head of People)
What worked: Opened with ROI quantification — "Your 400 engineers average 4 months to full
productivity. At $180K loaded cost, that's $240K per hire in ramp cost. SkillAgents cuts
that to 6 weeks." Ben Alvarez responded within 4 hours. The Cursor AI training gap framing
was the hook — he had publicly posted that 60% of engineers hadn't opened Cursor AI.
Lesson learned: ICP B (Scaling Tech Company) CTOs respond best to ROI math tied to their
own public statements. Lead with their words back to them. Quantify the cost of the status quo.
Do not pitch features — pitch the cost of inaction.
Trial: 14-day pilot with 50 engineers. 88% completion rate. Converted to annual contract.
Close time: 18 days from first outreach to signed contract.

DEAL #2 — GlobalBank Corp — STALLED — Deal paused
Contact: Sarah Mitchell (CHRO), Derek Okafor (VP L&D)
What blocked: Sarah Mitchell raised SOC2 Type II compliance and EU data residency requirements
on the second call. We did not have the security documentation ready. Deal sent to legal review.
Lesson learned: Enterprise Financial Services (ICP A) requires compliance collateral BEFORE
the first call — not after. Send SOC2 Type II report, data residency options, and GDPR
compliance overview in the intro email. Do not wait for them to ask. Their legal team will
block any deal that doesn't arrive pre-cleared on security.
Action: Prepare a 2-page compliance brief. Lead the next FinServ outreach with it.
"""


def extract_text(result) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, list):
        return "\n".join(str(x) for x in result)
    if isinstance(result, dict):
        val = result.get("text") or result.get("search_result")
        if isinstance(val, list):
            return "\n".join(str(x) for x in val)
        if val:
            return str(val)
        return str(result.get("raw", {}).get("value", result))
    return str(result)


async def run_query() -> str:
    try:
        results = await cognee.search(
            query_text=QUERY,
            query_type=SearchType.GRAPH_COMPLETION,
        )
    except Exception:
        results = []
    texts = [extract_text(r) for r in results]
    texts = [t for t in texts if t and t.strip()]
    return "\n".join(texts) if texts else "(no results)"


async def main():
    await setup()

    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    r = redis_lib.from_url(redis_url)

    print("\n" + "=" * 70)
    print("  STAGE 4: SELF-EVOLUTION — Two-Layer Memory Architecture")
    print("  Redis  → real-time signal cache  (fast, ephemeral buffer)")
    print("  Cognee → persistent knowledge graph  (permanent, traversable)")
    print("=" * 70 + "\n")

    # Show Redis signal cache before
    signal_keys_before = len(r.keys("skillagents:signal:*"))
    print(f"  Redis signal cache BEFORE: {signal_keys_before} deal outcomes cached\n")

    print("─" * 70)
    print("  BEFORE EVOLUTION — BuildFast SaaS outreach recommendation:")
    print("─" * 70)
    before_answer = await run_query()
    print(before_answer)

    # Step 1: outcomes hit Redis first (real-time signal buffer)
    print("\n" + "─" * 70)
    print("  STEP 1: Deal outcomes arrive → cached in Redis (real-time buffer)")
    print("─" * 70)
    for outcome in DEAL_OUTCOMES:
        key = f"skillagents:signal:{outcome['id']}"
        r.hset(key, mapping={
            "company": outcome["company"],
            "result": outcome["result"],
            "arr": outcome["arr"],
            "lesson": outcome["lesson"],
            "cached_at": datetime.utcnow().isoformat(),
        })
        r.expire(key, 86400)  # 24h TTL — signals are ephemeral
        status = "WON $120K" if outcome["result"] == "CLOSED WON" else "STALLED"
        print(f"  [Redis HSET] {key}")
        print(f"               {outcome['company']} — {status}")

    signal_keys_after = len(r.keys("skillagents:signal:*"))
    print(f"\n  Redis signal cache AFTER: {signal_keys_after} deal outcomes cached  (+{signal_keys_after - signal_keys_before} new)\n")

    # Step 2: outcomes get crystallised into Cognee's knowledge graph
    print("─" * 70)
    print("  STEP 2: Outcomes crystallised → Cognee knowledge graph (permanent)")
    print("─" * 70)
    print("  [~] Extracting entities and updating graph...")
    await cognee.add(OUTCOMES_TEXT, dataset_name="deal_outcomes")
    await cognee.cognify(datasets=["deal_outcomes"])
    print("  [✓] BuildFast win pattern + GlobalBank compliance lesson now in graph.\n")

    print("─" * 70)
    print("  AFTER EVOLUTION — BuildFast SaaS outreach recommendation:")
    print("─" * 70)
    after_answer = await run_query()
    print(after_answer)

    print("\n" + "=" * 70)
    print("  SELF-EVOLUTION COMPLETE")
    print(f"  Redis: {signal_keys_after} signals cached  (real-time, 24h TTL)")
    print("  Cognee: win patterns + objection lessons now in the knowledge graph")
    print("  Every future SDR query can now surface these learnings.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
