# Dev Scripts

Development utilities for the LLM REPL project.

## groq-code-review.py

AI-powered code review tool using Groq's API with automatic model selection based on July 2025 capabilities.

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure you have `GROQ_API_KEY` in your `~/.env` file:
   ```
   GROQ_API_KEY=your-api-key-here
   ```

### Usage

Basic code review:
```bash
./groq-code-review.py path/to/file.py
```

List available models:
```bash
./groq-code-review.py --list-models any-file
```

Use specific model:
```bash
./groq-code-review.py --model llama-3.3-70b-versatile path/to/file.py
```

Save review to file:
```bash
./groq-code-review.py -o review.md path/to/file.py
```

### Model Selection

The script prioritizes models in this order (July 2025):
1. `llama-3.3-70b-versatile` - Latest Llama with strong code capabilities
2. `mixtral-8x7b-32768` - Excellent for code with large context windows
3. `llama3-70b-8192` - Strong general-purpose model
4. `gemma2-9b-it` - Good for detailed analysis
5. `llama3-8b-8192` - Efficient fallback model

The script automatically selects the best available model based on current API availability.

## Groq API Model Information (July 2025)

### Context Window Limits

| Model | Context Window | Notes |
|-------|----------------|-------|
| **llama-3.3-70b-versatile** | 131,072 tokens | Latest, recommended for code review |
| **llama-3.1-70b-versatile** | 131,072 tokens | Excellent performance |
| **llama-3.1-8b-instant** | 131,072 tokens | Fast responses, smaller model |
| **mixtral-8x7b-32768** | 32,768 tokens | Being deprecated March 2025 |
| **llama3-70b-8192** | 8,192 tokens | Legacy model |
| **llama3-8b-8192** | 8,192 tokens | Legacy model |
| **gemma2-9b-it** | 8,192 tokens | Good for analysis |

### Rate Limits

Groq offers different tiers with varying rate limits:

#### Free Tier
- **Rate limits**: Applied at organization level, per model
- **Types of limits**: 
  - RPM (Requests Per Minute)
  - TPM (Tokens Per Minute)
  - TPD (Tokens Per Day)
- **Important**: You hit whichever limit comes first

#### Developer Tier
- **10x more capacity** than free tier
- **Batch API access** with 25% discount
- **Self-serve upgrade** available

#### Enterprise Tier
- Custom limits
- Dedicated instances available

### Best Practices for Context Usage

1. **Large Files (>100KB)**:
   - Use models with 131K context (llama-3.3-70b-versatile)
   - Can send entire files up to ~50K lines of code

2. **Medium Files (10-100KB)**:
   - Any model works well
   - Mixtral-8x7b offers good balance with 32K context

3. **Small Files (<10KB)**:
   - All models handle these easily
   - Consider using faster models like llama-3.1-8b-instant

### Rate Limit Optimization

To maximize usage within rate limits:

1. **Batch Processing**:
   - Use the Developer Tier Batch API for 25% discount
   - Process multiple files in sequence

2. **Token Estimation**:
   - Code files: ~1.5 tokens per character
   - The script shows token usage in responses

3. **Request Spacing**:
   - Free tier: Space requests by at least 1-2 seconds
   - Monitor HTTP headers for remaining quota

4. **Model Selection**:
   - Smaller models (8B) use fewer tokens
   - Larger models (70B) provide better analysis

### Checking Your Limits

To see your current rate limits:
1. Log into [console.groq.com](https://console.groq.com)
2. Navigate to Dashboard → Limits
3. View per-model limits and current usage

### Error Handling

The script handles common API errors:
- Rate limit exceeded: Automatic retry with backoff
- Model unavailable: Falls back to alternative models
- Network errors: Clear error messages

### Advanced Usage

For production use, consider:
- Implementing request queuing
- Caching reviews for identical files
- Using batch API for multiple files
- Monitoring token usage via response headers