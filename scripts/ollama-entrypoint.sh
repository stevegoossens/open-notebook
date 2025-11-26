#!/bin/bash
ollama serve &
sleep 5  # Wait for Ollama server to start

# Pull models if not already present
# Extraction (per‑PDF schema parsing) -> Use Mistral 7B Instruct Q5_K_M
# Aggregation (multi‑PDF comparisons) -> Use Mixtral 8x7B Q5_K_M on the 3080Ti.
#   It handles longer context windows and multi‑document reasoning better.
# Fallback generalist -> Llama 3 Instruct Q5_K_M if you want Meta’s latest tuning, but it’s heavier than Mistral.
# Embeddings -> MXBai-Embed-Large for high-quality text embeddings.
models=("llama3:instruct" "mistral:instruct" "mixtral:8x7b" "mxbai-embed-large")
for model in "${models[@]}"; do
  ollama list | grep -q "$model" || ollama pull "$model"
done

wait -n  # Keep the container running
