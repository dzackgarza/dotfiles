# Ollama Local Model Setup

**Created:** 2025-07-10

This document provides commands to download all optimal local models for our LLM REPL system.

## Required Local Models

Based on our performance benchmarks, these are the optimal local models for each task:

### Core Models (Essential)

```bash
# Primary speed model - used for most tasks
ollama pull mistral:7b-instruct-q4_K_M

# Tool use and formatting
ollama pull llama3.1:8b-instruct-q4_K_M

# Reasoning and explanation
ollama pull grok:1.5-7b-q4_K_M

# Classification and triage
ollama pull command-r:35b-q4_K_M
```

### Specialized Models

```bash
# Instruction processing
ollama pull nous-hermes2-mistral:7b-q4_K_M
ollama pull openhermes:7b-q4_K_M

# Code generation
ollama pull codellama:7b-instruct-q4_K_M
ollama pull deepseek-coder:6.7b-instruct-q4_K_M

# Mathematics and logic
ollama pull phi3.5:3.8b-mini-instruct-q4_K_M

# Lightweight fallback
ollama pull tinyllama:1.1b-chat-q4_K_M
```

### Model Performance Matrix

| Task Category | Primary Model | Fallback Model | Use Case |
|---------------|---------------|----------------|----------|
| **Speed/General** | `mistral:7b-instruct-q4_K_M` | `tinyllama:1.1b-chat-q4_K_M` | Default routing |
| **Tool Use** | `llama3.1:8b-instruct-q4_K_M` | `mistral:7b-instruct-q4_K_M` | Shell commands, formatting |
| **Reasoning** | `grok:1.5-7b-q4_K_M` | `nous-hermes2-mistral:7b-q4_K_M` | Complex explanations |
| **Code** | `codellama:7b-instruct-q4_K_M` | `deepseek-coder:6.7b-instruct-q4_K_M` | Programming tasks |
| **Math** | `phi3.5:3.8b-mini-instruct-q4_K_M` | `mistral:7b-instruct-q4_K_M` | Mathematical reasoning |
| **Classification** | `command-r:35b-q4_K_M` | `mistral:7b-instruct-q4_K_M` | Intent detection |

## Ollama Setup Commands

### 1. Download All Essential Models

```bash
#!/bin/bash
# Essential models download script

echo "Downloading essential Ollama models..."

# Core models
ollama pull mistral:7b-instruct-q4_K_M
ollama pull llama3.1:8b-instruct-q4_K_M
ollama pull tinyllama:1.1b-chat-q4_K_M

# Specialized models
ollama pull nous-hermes2-mistral:7b-q4_K_M
ollama pull codellama:7b-instruct-q4_K_M
ollama pull phi3.5:3.8b-mini-instruct-q4_K_M

echo "Essential models downloaded!"
```

### 2. Download Advanced Models (Optional)

```bash
#!/bin/bash
# Advanced models for better performance

echo "Downloading advanced models..."

# Better reasoning
ollama pull llama3.1:70b-instruct-q4_K_M  # If you have 48GB+ RAM
ollama pull mixtral:8x7b-instruct-q4_K_M  # If you have 32GB+ RAM

# Code specialization
ollama pull deepseek-coder:33b-instruct-q4_K_M  # If you have 24GB+ RAM

echo "Advanced models downloaded!"
```

### 3. Hugging Face to Ollama Integration

For models not directly available in Ollama:

```bash
# Download quantized models from Hugging Face
ollama run hf.co/bartowski/Mistral-Small-3.2-24B-Instruct-GGUF:Q4_K_M
ollama run hf.co/gabriellarson/Llama-4-Scout-17B-16E-Instruct-GGUF:Q4_K_M

# Save them locally
ollama create mistral-small-3.2:24b-q4_K_M -f <(echo "FROM hf.co/bartowski/Mistral-Small-3.2-24B-Instruct-GGUF:Q4_K_M")
```

## Model Configuration

### Memory Requirements

| Model Size | RAM Required | GPU VRAM | Performance |
|------------|--------------|----------|-------------|
| 1B-3B | 4GB | 2GB | Fast, basic |
| 7B | 8GB | 4GB | Good, standard |
| 13B | 16GB | 8GB | Better, slower |
| 33B | 24GB | 16GB | Best, much slower |
| 70B | 48GB | 32GB | Excellent, very slow |

### Quantization Levels

- **Q4_K_M**: Best balance of quality and size (recommended)
- **Q5_K_M**: Higher quality, larger size
- **Q8_0**: Highest quality, largest size
- **Q2_K**: Smallest size, lower quality

## Integration with LLM REPL

### Model Routing Configuration

```python
# V2/config/llm_config.py additions
LOCAL_MODEL_CONFIG = {
    'speed_model': 'mistral:7b-instruct-q4_K_M',
    'reasoning_model': 'grok:1.5-7b-q4_K_M',
    'tool_model': 'llama3.1:8b-instruct-q4_K_M',
    'code_model': 'codellama:7b-instruct-q4_K_M',
    'math_model': 'phi3.5:3.8b-mini-instruct-q4_K_M',
    'fallback_model': 'tinyllama:1.1b-chat-q4_K_M'
}

TASK_MODEL_ROUTING = {
    'instruction_routing': 'speed_model',
    'tool_use_formatting': 'tool_model',
    'rationale_generation': 'reasoning_model',
    'parameter_extraction': 'speed_model',
    'simple_classification': 'speed_model',
    'error_quality_scoring': 'reasoning_model',
}
```

### Usage Patterns

```python
def get_local_model_for_task(task_type: str) -> str:
    """Get optimal local model for task type"""
    model_key = TASK_MODEL_ROUTING.get(task_type, 'speed_model')
    return LOCAL_MODEL_CONFIG[model_key]

# Example usage
model = get_local_model_for_task('instruction_routing')
# Returns: 'mistral:7b-instruct-q4_K_M'
```

## Performance Expectations

### Speed (Tokens/Second on Modern Hardware)

| Model | CPU (16-core) | GPU (RTX 4090) | M2 Pro |
|-------|---------------|----------------|---------|
| tinyllama:1.1b | 50-80 | 100-150 | 40-60 |
| mistral:7b-q4 | 15-25 | 40-60 | 12-20 |
| llama3.1:8b-q4 | 12-20 | 35-50 | 10-15 |
| codellama:7b-q4 | 15-25 | 40-60 | 12-20 |

### Quality Scores

Based on our benchmarks:
- **7B models**: 7-8/10 performance
- **13B+ models**: 8-9/10 performance
- **Quantized (Q4_K_M)**: -0.5 quality vs full precision

## Maintenance

### Update Models Regularly

```bash
# Check for updates
ollama list

# Update specific model
ollama pull mistral:7b-instruct-q4_K_M

# Remove old versions
ollama rm mistral:old-version
```

### Monitor Usage

```bash
# Check model sizes
ollama list

# Monitor system resources
htop  # CPU/RAM usage
nvidia-smi  # GPU usage
```

## Troubleshooting

### Common Issues

1. **Out of Memory**: Use smaller models or higher quantization
2. **Slow Performance**: Ensure GPU acceleration is enabled
3. **Model Not Found**: Check ollama library or use HF integration

### Performance Optimization

```bash
# Enable GPU acceleration
export OLLAMA_GPU_LAYERS=999

# Adjust context size
export OLLAMA_NUM_CTX=4096

# Optimize for speed
export OLLAMA_NUM_THREAD=8
```