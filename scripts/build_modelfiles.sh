#!/usr/bin/env bash
# Build all deltai-* Ollama models from modelfiles/.
# Run this once after a fresh clone or when modelfiles change.
# Usage: bash scripts/build_modelfiles.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODELFILES_DIR="${REPO_ROOT}/modelfiles"

if ! command -v ollama &>/dev/null; then
    echo "ERROR: ollama not found in PATH. Install it first: https://ollama.com" >&2
    exit 1
fi

if ! ollama list &>/dev/null; then
    echo "ERROR: Ollama is not running. Start it with: ollama serve" >&2
    exit 1
fi

build_model() {
    local name="$1"
    local file="$2"
    if [ ! -f "${file}" ]; then
        echo "SKIP  ${name} — modelfile not found: ${file}"
        return
    fi
    echo "BUILD ${name} ..."
    if ollama create "${name}" -f "${file}"; then
        echo "OK    ${name}"
    else
        echo "FAIL  ${name}" >&2
    fi
}

build_model "deltai-qwen14b"  "${MODELFILES_DIR}/deltai-qwen14b.modelfile"
build_model "deltai-qwen3b"   "${MODELFILES_DIR}/deltai-qwen3b.modelfile"
build_model "deltai-nemo"     "${MODELFILES_DIR}/deltai-nemo.modelfile"
build_model "deltai-fallback" "${MODELFILES_DIR}/deltai-fallback.modelfile"

echo ""
echo "Done. Registered models:"
ollama list | grep "deltai-" || echo "(none found)"
