#!/usr/bin/env bash
# Build all deltai-* Ollama models from modelfiles/.
#
# Run this once after a fresh clone (or whenever modelfiles change). The
# inference fallback chain (deltai-qwen14b → deltai-nemo → deltai-fallback)
# silently degrades when nemo or fallback are missing, so building all four
# avoids 4-minute hangs the first time the chain is exercised.
#
# Usage:
#   bash scripts/build_modelfiles.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODELS_DIR="$REPO_ROOT/modelfiles"

if ! command -v ollama >/dev/null 2>&1; then
    echo "ollama not found in PATH. Install Ollama first: https://ollama.ai" >&2
    exit 1
fi

if ! curl -fsS http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    echo "Ollama isn't responding on 127.0.0.1:11434. Start it with 'ollama serve' first." >&2
    exit 1
fi

build() {
    local name="$1"
    local file="$MODELS_DIR/$name.modelfile"
    if [[ ! -f "$file" ]]; then
        echo "skip: $file missing"
        return
    fi
    echo ">> ollama create $name -f $file"
    ollama create "$name" -f "$file"
}

build deltai-qwen14b
build deltai-qwen3b
build deltai-nemo
build deltai-fallback

echo
echo "Done. Verify with: ollama list | grep deltai-"
