#!/bin/bash
# Download essential Ollama models for LLM REPL
# Based on performance benchmarks in .ai/ollama-setup.md

echo "🚀 Downloading essential Ollama models for LLM REPL..."
echo "This will download ~20GB of models optimized for our use cases"
echo ""

# Core models (essential)
echo "📦 Downloading core models..."
echo "1/6 Mistral 7B (primary speed model)..."
ollama pull mistral:7b-instruct-q4_K_M

echo "2/6 Llama 3.1 8B (tool use and formatting)..."
ollama pull llama3.1:8b-instruct-q4_K_M

echo "3/6 TinyLlama (lightweight fallback)..."
ollama pull tinyllama:1.1b-chat-q4_K_M

# Specialized models
echo "📦 Downloading specialized models..."
echo "4/6 Nous Hermes (instruction processing)..."
ollama pull nous-hermes2-mistral:7b-q4_K_M

echo "5/6 CodeLlama (code generation)..."
ollama pull codellama:7b-instruct-q4_K_M

echo "6/6 Phi 3.5 (mathematics and reasoning)..."
ollama pull phi3.5:3.8b-mini-instruct-q4_K_M

echo ""
echo "✅ Essential models downloaded!"
echo ""
echo "📊 Model usage summary:"
echo "- mistral:7b-instruct-q4_K_M     → Default speed model (most tasks)"
echo "- llama3.1:8b-instruct-q4_K_M   → Tool use, shell commands, formatting"
echo "- nous-hermes2-mistral:7b-q4_K_M → Instruction routing and rewriting"
echo "- codellama:7b-instruct-q4_K_M   → Code generation and debugging"
echo "- phi3.5:3.8b-mini-instruct-q4_K_M → Mathematical reasoning"
echo "- tinyllama:1.1b-chat-q4_K_M     → Lightweight fallback"
echo ""
echo "🔧 Optional: Run 'bash download-advanced-models.sh' for better performance models"
echo "📚 See .ai/ollama-setup.md for complete configuration details"