#!/bin/bash
ollama serve &
sleep 5  # Wait for Ollama server to start

# Pull models if not already present
ollama list | grep -q llama2 || ollama pull llama2
ollama list | grep -q mistral || ollama pull mistral
ollama list | grep -q 'llama2:13b' || ollama pull llama2:13b

wait -n  # Keep the container running
