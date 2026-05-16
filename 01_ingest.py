"""
Stage 1: Ingest (Local Mode)
Mixed ingestion: unstructured text (SDR playbook, ICP profiles) + structured dlt resource (prospects).
Vector store: local Redis. LLM: OpenAI (for entity extraction + embeddings).
"""
import asyncio
import os
import sys
from pathlib import Path
from utils import setup
import cognee

DATA_DIR = Path(__file__).parent / "data"


async def main():
    await setup()

    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if not openai_key:
        print("[ERROR] OPENAI_API_KEY not set — add it to .env and retry.")
        sys.exit(1)

    print("\n=== STAGE 1: INGEST (LOCAL) ===\n")

    # --- Unstructured text datasets ---
    for dataset_name, filename in [
        ("sdr_knowledge", "sdr_playbook.txt"),
        ("icp_profiles", "icp_profiles.txt"),
    ]:
        text = (DATA_DIR / filename).read_text()
        await cognee.add(text, dataset_name=dataset_name)
        print(f"[text] {dataset_name}: {filename} ({len(text):,} chars)")

    # --- Structured dlt resource ---
    sys.path.insert(0, str(DATA_DIR))
    from prospects_dlt import get_prospects

    await cognee.add(
        get_prospects(),
        dataset_name="prospect_data",
        primary_key="id",
        write_disposition="replace",
    )
    print(f"[dlt]  prospect_data: 5 companies with nested signals / tech_stack / contacts")

    # --- Build knowledge graph ---
    print("\n[~] Building knowledge graph (cognify)... this may take 60–120s")
    await cognee.cognify(datasets=["sdr_knowledge", "icp_profiles", "prospect_data"])
    print("[✓] Knowledge graph built.\n")
    print("All datasets ingested into local Cognee + Redis. Ready for retrieval.")


if __name__ == "__main__":
    asyncio.run(main())
