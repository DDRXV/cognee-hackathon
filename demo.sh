#!/bin/bash
# Hackathon demo runner — Self-Evolving GTM Brain
# Run from the cognee-hackathon directory: ./demo.sh

set -e
cd "$(dirname "$0")"
ulimit -n 4096 2>/dev/null || true  # prevent "too many open files" from LanceDB subprocesses

# Helper: count cached deal signals in Redis (our real-time buffer)
redis_signals() {
    python -c "
import os; from dotenv import load_dotenv; load_dotenv()
import redis; r = redis.from_url(os.environ.get('REDIS_URL','redis://localhost:6379'))
print(len(r.keys('skillagents:signal:*')))
" 2>/dev/null || echo "?"
}

clear
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║      SELF-EVOLVING GTM BRAIN — SkillAgents AI                      ║"
echo "║      Redis + Cognee Knowledge Graph  |  Hackathon Demo              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "  Architecture:"
echo "    Cognee  →  persistent knowledge graph  (entities, relationships, facts)"
echo "    Redis   →  real-time signal cache      (deal outcomes buffered before graph update)"
echo "    dlt     →  structured ingestion        (FK edges: company → signals/tech/contacts)"
echo ""

echo "──────────────────────────────────────────────────────────────────────"
echo "  PREREQS"
echo "──────────────────────────────────────────────────────────────────────"
if docker ps 2>/dev/null | grep -q redis; then
    echo "  [✓] Redis container: RUNNING"
else
    echo "  [!] Redis not running — start with:"
    echo "      docker run -d --name redis-cognee -p 6379:6379 redis:latest"
fi
SIGNALS=$(redis_signals)
echo "  [~] Redis signal cache: ${SIGNALS} deal outcomes cached"
echo ""

read -p "  Press Enter to run Stage 1: INGEST ▶  "
clear
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  STAGE 1: INGEST                                                    ║"
echo "║  Loading SDR playbook + ICP profiles + 5 prospects into Cognee      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
python 01_ingest.py
echo ""
echo "  Cognee knowledge graph built. Redis signal cache: $(redis_signals) outcomes."

read -p "
  Press Enter to run Stage 2: RETRIEVE ▶  "
clear
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  STAGE 2: RETRIEVE                                                  ║"
echo "║  Agentic reasoning across the knowledge graph                       ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
python 02_retrieve.py

read -p "
  Press Enter to run Stage 3: KNOWLEDGE AUDIT ▶  "
clear
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  STAGE 3: KNOWLEDGE AUDIT                                           ║"
echo "║  What did Cognee actually learn? (Karpathy-style LLM.txt wiki)      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
python 03_lint.py

read -p "
  Press Enter to run Stage 4: SELF-EVOLVE  ◀ THE WOW MOMENT ▶  "
clear
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║  STAGE 4: SELF-EVOLUTION                                            ║"
echo "║  Two deals close. Redis buffers signals. Cognee learns. Graph grows. ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
python 04_evolve.py

echo ""
echo "──────────────────────────────────────────────────────────────────────"
echo "  DEMO COMPLETE"
echo "──────────────────────────────────────────────────────────────────────"
echo ""
echo "  View the knowledge graph:"
echo "    Cognee UI  →  http://localhost:3000"
echo ""
echo "  Redis signal cache: $(redis_signals) deal outcomes cached (24h TTL)"
echo "  Cognee: win patterns + compliance lessons permanent in knowledge graph"
echo ""
