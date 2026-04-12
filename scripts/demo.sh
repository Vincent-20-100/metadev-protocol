#!/usr/bin/env bash
# demo.sh — End-to-end demo of metadev-protocol
# Usage: bash scripts/demo.sh
# Records well with: vhs scripts/demo.tape

set -euo pipefail

DEMO_DIR=$(mktemp -d)
PROJECT_NAME="my-ai-project"
trap "rm -rf $DEMO_DIR" EXIT

echo ""
echo "══════════════════════════════════════════════════════"
echo "  metadev-protocol — AI-assisted Python project template"
echo "══════════════════════════════════════════════════════"
echo ""
sleep 1

# Step 1: Generate
echo "▸ Step 1: Generate a project"
echo "  copier copy gh:Vincent-20-100/metadev-protocol $DEMO_DIR/$PROJECT_NAME"
echo ""
copier copy . "$DEMO_DIR/$PROJECT_NAME" \
  --trust --vcs-ref=HEAD --defaults \
  -d "project_name=$PROJECT_NAME" \
  -d "meta_visibility=public" \
  -d "execution_mode=safe" \
  2>/dev/null
echo "  Done."
echo ""
sleep 1

# Step 2: Show structure
echo "▸ Step 2: Project structure"
echo ""
cd "$DEMO_DIR/$PROJECT_NAME"
find . -maxdepth 3 -not -path './.git/*' -not -path './.venv/*' -not -name '.gitkeep' | sort | head -40
echo "  ..."
echo ""
sleep 2

# Step 3: Show CLAUDE.md highlights
echo "▸ Step 3: CLAUDE.md — the AI session contract"
echo ""
head -20 CLAUDE.md
echo "  ..."
echo ""
sleep 2

# Step 4: Show .meta/ taxonomy
echo "▸ Step 4: .meta/ — persistent project memory"
echo ""
echo "  PILOT.md        → project dashboard (AI reads first)"
echo "  SESSION-CONTEXT  → living context (rewritten each session)"
echo "  GUIDELINES       → recommended practices"
echo "  active/          → validated specs and plans"
echo "  archive/         → implemented artifacts"
echo "  decisions/       → ADRs"
echo "  drafts/          → WIP (gitignored)"
echo ""
sleep 2

# Step 5: Show pre-commit hooks
echo "▸ Step 5: Pre-commit hooks (safety from day 1)"
echo ""
grep "id:" .pre-commit-config.yaml | sed 's/^.*id: /  ✓ /'
echo ""
sleep 2

# Step 6: Show skills
echo "▸ Step 6: Available skills"
echo ""
for skill in .claude/skills/*/; do
  name=$(basename "$skill")
  echo "  /$(printf '%-16s' "$name") → $(head -3 "$skill/SKILL.md" | grep 'description:' | sed 's/.*description: //')"
done
echo ""
sleep 2

# Step 7: Secret scan demo
echo "▸ Step 7: Public safety audit"
echo ""
echo "  40+ regex patterns for AWS keys, GitHub tokens, private keys..."
echo "  Runs at every commit via pre-commit hook."
echo ""
echo "  Testing a fake secret..."
# Generate a fake token at runtime to trigger the scanner
python -c "print('key = \"ghp_' + 'a' * 36 + '\"')" > /tmp/test-secret.py
python scripts/audit_public_safety.py --mode=quick /tmp/test-secret.py 2>&1 || true
rm -f /tmp/test-secret.py
echo ""
sleep 2

# Step 8: Execution modes
echo "▸ Step 8: Execution modes"
echo ""
echo "  safe      → Claude asks before touching repo structure"
echo "  full-auto → everything allowed except hard safety net"
echo ""
echo "  Configured per project at generation time."
echo "  Switch anytime: copier update --data execution_mode=full-auto"
echo ""
sleep 1

echo "══════════════════════════════════════════════════════"
echo "  Ready to build. Your AI has context from day one."
echo "  https://github.com/Vincent-20-100/metadev-protocol"
echo "══════════════════════════════════════════════════════"
echo ""
