#!/bin/bash
# Download advanced Ollama models for better performance
# Requires more RAM/VRAM - see .ai/ollama-setup.md for requirements

echo "🚀 Downloading advanced Ollama models..."
echo "⚠️  These models require significant RAM/VRAM:"
echo "   - 13B models: 16GB RAM minimum"
echo "   - 33B models: 24GB RAM minimum" 
echo "   - 70B models: 48GB RAM minimum"
echo ""

read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Check available RAM
total_ram=$(free -g | awk '/^Mem:/{print $2}')
echo "💾 Detected ${total_ram}GB total RAM"

if [ "$total_ram" -lt 16 ]; then
    echo "⚠️  Warning: Less than 16GB RAM detected. Large models may not run well."
fi

# Download based on available RAM
if [ "$total_ram" -ge 48 ]; then
    echo "📦 Downloading 70B models (excellent performance)..."
    ollama pull llama3.1:70b-instruct-q4_K_M
    echo "✅ Llama 3.1 70B downloaded"
fi

if [ "$total_ram" -ge 32 ]; then
    echo "📦 Downloading Mixtral 8x7B (excellent multilingual)..."
    ollama pull mixtral:8x7b-instruct-q4_K_M
    echo "✅ Mixtral 8x7B downloaded"
fi

if [ "$total_ram" -ge 24 ]; then
    echo "📦 Downloading 33B code model..."
    ollama pull deepseek-coder:33b-instruct-q4_K_M
    echo "✅ DeepSeek Coder 33B downloaded"
fi

if [ "$total_ram" -ge 16 ]; then
    echo "📦 Downloading 13B reasoning model..."
    ollama pull nous-hermes2:13b-q4_K_M
    echo "✅ Nous Hermes 13B downloaded"
else
    echo "ℹ️  Skipping large models due to RAM limitations"
    echo "   Consider upgrading to 16GB+ RAM for better performance"
fi

echo ""
echo "✅ Advanced models download complete!"
echo ""
echo "📊 Updated model hierarchy:"
if [ "$total_ram" -ge 48 ]; then
    echo "🥇 Reasoning: llama3.1:70b-instruct-q4_K_M (best)"
fi
if [ "$total_ram" -ge 32 ]; then
    echo "🥇 Multilingual: mixtral:8x7b-instruct-q4_K_M"
fi
if [ "$total_ram" -ge 24 ]; then
    echo "🥇 Code: deepseek-coder:33b-instruct-q4_K_M (best)"
fi
if [ "$total_ram" -ge 16 ]; then
    echo "🥇 General: nous-hermes2:13b-q4_K_M (better)"
fi
echo ""
echo "💡 Update your model routing config to use these advanced models"
echo "📚 See .ai/ollama-setup.md for integration instructions"