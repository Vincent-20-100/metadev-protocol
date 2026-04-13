#!/usr/bin/env bash
# Regenerate all README diagrams from their .mmd sources.
#
# Usage: bash scripts/render-diagrams.sh
# Requires: node + npx (no global install needed)

set -euo pipefail

DIAGRAMS_DIR="docs/diagrams"
CONFIG="$DIAGRAMS_DIR/mermaid-config.json"
PUPPETEER="$DIAGRAMS_DIR/puppeteer-config.json"

cd "$(dirname "$0")/.."

if [[ ! -d "$DIAGRAMS_DIR" ]]; then
  echo "error: $DIAGRAMS_DIR not found" >&2
  exit 1
fi

shopt -s nullglob
for src in "$DIAGRAMS_DIR"/*.mmd; do
  out="${src%.mmd}.svg"
  # Use per-diagram config if present (e.g. 03-rails.config.json), else global.
  per_diagram="${src%.mmd}.config.json"
  cfg="$CONFIG"
  if [[ -f "$per_diagram" ]]; then
    cfg="$per_diagram"
  fi
  echo "→ $src → $out (config: $cfg)"
  npx -y -p @mermaid-js/mermaid-cli mmdc \
    -i "$src" \
    -o "$out" \
    -c "$cfg" \
    -p "$PUPPETEER" \
    -b transparent
done

echo "normalizing viewBox aspect ratios to 2.1..."
python - <<'PY'
import re, pathlib
target_ratio = 2.1
for p in sorted(pathlib.Path("docs/diagrams").glob("*.svg")):
    s = p.read_text(encoding="utf-8")
    m = re.search(r'<svg[^>]*viewBox="([^"]+)"', s)
    if not m:
        continue
    parts = [float(x) for x in m.group(1).replace(",", " ").split()]
    x, y, w, h = parts
    ratio = w / h
    if abs(ratio - target_ratio) < 0.05:
        print(f"  {p.name}: {w:.0f}x{h:.0f} ratio {ratio:.2f} ok")
        continue
    if ratio > target_ratio:
        new_h = w / target_ratio
        new_y = y - (new_h - h) / 2
        new_vb = f"{x} {new_y} {w} {new_h}"
    else:
        new_w = h * target_ratio
        new_x = x - (new_w - w) / 2
        new_vb = f"{new_x} {y} {new_w} {h}"
    s = re.sub(r'(<svg[^>]*viewBox=")[^"]+(")', r'\g<1>' + new_vb + r'\g<2>', s, count=1)
    s = re.sub(r'(<svg[^>]*?)\s+width="[^"]*"', r'\1', s, count=1)
    s = re.sub(r'(<svg[^>]*?)\s+height="[^"]*"', r'\1', s, count=1)
    p.write_text(s, encoding="utf-8")
    print(f"  {p.name}: {w:.0f}x{h:.0f} ratio {ratio:.2f} -> normalized")
PY

echo "done."
