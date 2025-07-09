#!/usr/bin/env python3
"""
Quick timing test to get immediate baseline data for TinyLlama.
"""

import asyncio
import aiohttp
import time
import json
import sys

async def test_timing(prompt: str, model: str = "tinyllama"):
    """Quick timing test for a single prompt."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7}
    }
    
    print(f"Testing prompt ({len(prompt.split())} words): {prompt[:50]}...")
    
    start_time = time.time()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    print(f"Error: {response.status}")
                    return None
                
                data = await response.json()
                end_time = time.time()
                
                duration = end_time - start_time
                input_tokens = data.get('prompt_eval_count', len(prompt.split()) * 1.3)
                output_tokens = data.get('eval_count', len(data.get('response', '').split()))
                
                print(f"  ✅ {duration:.2f}s | ↑{int(input_tokens)} ↓{int(output_tokens)} tokens")
                print(f"  Response: {data.get('response', '')[:100]}...")
                
                return {
                    'duration': duration,
                    'input_tokens': int(input_tokens),
                    'output_tokens': int(output_tokens),
                    'total_tokens': int(input_tokens + output_tokens),
                    'tokens_per_second': (input_tokens + output_tokens) / duration
                }
    
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return None

async def main():
    """Run quick baseline tests."""
    print("🔬 Quick TinyLlama Timing Test")
    print("=" * 40)
    
    test_prompts = [
        "Hello",
        "What is 2+2?",
        "Explain machine learning in simple terms",
        "Write a short poem about programming",
        "Describe the process of photosynthesis in detail with examples and applications"
    ]
    
    results = []
    
    for prompt in test_prompts:
        result = await test_timing(prompt)
        if result:
            results.append(result)
        print()
    
    if results:
        print("📊 SUMMARY")
        print("-" * 40)
        avg_duration = sum(r['duration'] for r in results) / len(results)
        avg_tokens_per_sec = sum(r['tokens_per_second'] for r in results) / len(results)
        
        print(f"Average duration: {avg_duration:.2f}s")
        print(f"Average tokens/sec: {avg_tokens_per_sec:.1f}")
        
        # Simple linear estimates
        durations = [r['duration'] for r in results]
        total_tokens = [r['total_tokens'] for r in results]
        
        if len(results) >= 2:
            # Simple correlation
            import numpy as np
            correlation = np.corrcoef(total_tokens, durations)[0, 1]
            print(f"Token-duration correlation: {correlation:.3f}")
            
            # Simple linear fit: duration = a*tokens + b
            slope = np.cov(total_tokens, durations)[0, 1] / np.var(total_tokens)
            intercept = avg_duration - slope * np.mean(total_tokens)
            
            print(f"Simple linear model: duration = {slope:.4f}*tokens + {intercept:.2f}")
            print(f"Estimated base latency: {intercept:.2f}s")
            print(f"Estimated processing rate: {1/slope:.1f} tokens/sec")

if __name__ == "__main__":
    asyncio.run(main())