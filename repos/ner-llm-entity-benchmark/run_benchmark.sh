#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "=================================================="
echo "🚀 Activating Virtual Environment & Running NER System"
echo "=================================================="

# Check and activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "❌ Error: Virtual environment activation script not found. Please run ./configure.sh first."
    exit 1
fi

echo "📊 Running full benchmark sweep — 15 models (including MiniMax & gpt-oss) on ALL data..."
python src/main.py --data-file data/kleptotrace.json \
  --models \
    gemma4:31b-cloud \
    minimax-m3:cloud \
    gemma4:31b-mlx \
    "sonct988/gemma4-26b-a4b-it-q4km-256k:latest" \
    gpt-oss:20b \
    gemma4:latest \
    gemma:latest \
    qwen3:8b \
    qwen2.5:14b \
    mistral-nemo:latest \
    nuextract:latest \
    llama3.1:8b \
    llama3.2:latest \
    nemotron-mini:4b \
    deepseek-r1:1.5b \
  --batch-size 3

echo "🧪 Running the prompt ablation study sweep on ALL data..."
python src/main.py --ablation --data-file data/kleptotrace.json --models gemma4:latest --batch-size 3

echo "📈 Simulating production batch flow..."
python src/simulate_production.py

echo "=================================================="
echo "🎉 System Execution Complete!"
echo "Metrics and results are saved in the results/ directory."
echo "=================================================="
