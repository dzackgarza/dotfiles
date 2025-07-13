#!/usr/bin/env python3
"""
Simple performance validation for Task 12.6 optimizations
"""

import time
import asyncio
from datetime import datetime, timezone

# Test token counting improvements
from src.core.token_counter import CachedTokenCounter

def test_token_counting_performance():
    print("🔢 Testing Token Counting Performance")
    print("-" * 40)
    
    # Create test data
    texts = [f"This is test message {i} with some content." for i in range(100)]
    
    counter = CachedTokenCounter()
    
    # First pass - no cache
    start_time = time.time()
    for text in texts:
        counter.count_tokens(text, include_metadata=False)
    first_pass_time = time.time() - start_time
    
    # Second pass - with cache
    start_time = time.time()
    for text in texts:
        counter.count_tokens(text, include_metadata=False)
    second_pass_time = time.time() - start_time
    
    # Batch processing
    start_time = time.time()
    counter.count_tokens_batch(texts)
    batch_time = time.time() - start_time
    
    stats = counter.get_cache_stats()
    
    print(f"   First pass (no cache): {first_pass_time:.4f}s")
    print(f"   Second pass (cached): {second_pass_time:.4f}s")
    print(f"   Batch processing: {batch_time:.4f}s")
    print(f"   Cache hit rate: {stats['hit_rate']:.1%}")
    print(f"   Speedup (cache): {first_pass_time/second_pass_time:.1f}x")
    print(f"   Speedup (batch): {first_pass_time/batch_time:.1f}x")
    
    return first_pass_time/second_pass_time > 5  # Expect 5x speedup with cache

def test_context_scoring_performance():
    print("\n🎯 Testing Context Scoring Performance")
    print("-" * 40)
    
    from src.core.context_scoring import ContextScorer, ConversationTurn
    
    # Create test turns
    turns = []
    base_time = datetime.now(timezone.utc)
    for i in range(100):
        turn = ConversationTurn(
            id=str(i),
            content=f"Test message {i} about various topics",
            role="user" if i % 2 == 0 else "assistant",
            timestamp=base_time.replace(microsecond=i * 1000),
            tokens=10
        )
        turns.append(turn)
    
    scorer = ContextScorer()
    
    # Test scoring performance
    start_time = time.time()
    scores = scorer.score_context_turns(turns, "test query")
    scoring_time = time.time() - start_time
    
    print(f"   Scored {len(turns)} turns in {scoring_time:.4f}s")
    print(f"   Throughput: {len(turns)/scoring_time:.1f} turns/second")
    print(f"   Average score: {sum(s.combined_score for s in scores)/len(scores):.3f}")
    
    return scoring_time < 0.1  # Should score 100 turns in under 100ms

def test_end_to_end_performance():
    print("\n🚀 Testing End-to-End Performance")
    print("-" * 40)
    
    from src.core.token_counter import ConversationTokenManager
    from src.core.context_scoring import ContextScorer, ConversationTurn
    from src.core.context_formatting import ContextFormattingManager, FormatStyle
    
    # Create test data
    turns = []
    base_time = datetime.now(timezone.utc)
    for i in range(50):
        turn = ConversationTurn(
            id=str(i),
            content=f"Test conversation turn {i} with realistic content length",
            role="user" if i % 2 == 0 else "assistant",
            timestamp=base_time.replace(microsecond=i * 1000),
            tokens=12
        )
        turns.append(turn)
    
    # Initialize components
    token_manager = ConversationTokenManager()
    scorer = ContextScorer()
    formatter = ContextFormattingManager()
    
    # Run complete pipeline
    start_time = time.time()
    
    # 1. Token counting
    messages = [{'role': turn.role, 'content': turn.content} for turn in turns]
    token_result = token_manager.count_conversation_tokens(messages)
    
    # 2. Context scoring and selection
    optimal_turns = scorer.get_optimal_context(turns, "test query", max_tokens=1000)
    
    # 3. Context formatting
    formatted = asyncio.run(formatter.format_context(optimal_turns, FormatStyle.CONVERSATIONAL))
    
    total_time = time.time() - start_time
    
    print(f"   Processed {len(turns)} turns in {total_time:.4f}s")
    print(f"   Selected {len(optimal_turns)} optimal turns")
    print(f"   Formatted output: {len(formatted)} characters")
    print(f"   Throughput: {len(turns)/total_time:.1f} turns/second")
    
    target_met = total_time < 0.5  # 500ms target
    print(f"   Performance target (500ms): {'✅ PASS' if target_met else '❌ FAIL'}")
    
    return target_met

def main():
    print("🔍 TASK 12.6 PERFORMANCE VALIDATION")
    print("=" * 50)
    print("Testing context management optimizations...")
    
    results = []
    
    # Run tests
    results.append(test_token_counting_performance())
    results.append(test_context_scoring_performance()) 
    results.append(test_end_to_end_performance())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n🏆 PERFORMANCE SUMMARY")
    print("=" * 30)
    print(f"   Tests passed: {passed}/{total}")
    
    if passed == total:
        print("   🎉 ALL PERFORMANCE TARGETS MET!")
        print("   ✅ Task 12.6 'Optimize Performance' - COMPLETE")
        print("\n💡 Key optimizations implemented:")
        print("   • Enhanced token counting cache")
        print("   • Parallel context scoring") 
        print("   • Batch processing support")
        print("   • Memory-efficient operations")
    else:
        print("   ⚠️ Some performance targets not met")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)