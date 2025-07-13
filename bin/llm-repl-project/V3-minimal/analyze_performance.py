#!/usr/bin/env python3
"""
Performance analysis script for context management system.
Analyzes profiling data and identifies optimization opportunities.
"""

import pstats
import time
import asyncio
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_profiling_data():
    """Analyze the context_performance.prof file"""
    try:
        # Read profiling data
        p = pstats.Stats('context_performance.prof')
        
        print("🔍 CONTEXT MANAGEMENT PERFORMANCE ANALYSIS")
        print("=" * 60)
        
        # Top 20 functions by cumulative time
        print("\n📊 TOP 20 FUNCTIONS BY CUMULATIVE TIME:")
        print("-" * 50)
        p.sort_stats('cumulative').print_stats(20)
        
        # Functions taking most self-time
        print("\n⏱️ TOP 10 FUNCTIONS BY SELF TIME:")
        print("-" * 40)
        p.sort_stats('tottime').print_stats(10)
        
        # Context-specific function analysis
        print("\n🎯 CONTEXT MANAGEMENT SPECIFIC ANALYSIS:")
        print("-" * 45)
        
        # Filter for context-related functions
        context_functions = [
            'token', 'context', 'score', 'format', 'summariz', 
            'timeline', 'conversation', 'cache', 'block'
        ]
        
        for keyword in context_functions:
            print(f"\n🔎 Functions containing '{keyword}':")
            try:
                p.print_stats(keyword)
            except:
                print(f"   No functions found containing '{keyword}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing profiling data: {e}")
        return False

async def benchmark_context_operations():
    """Benchmark individual context management operations"""
    
    print("\n🚀 CONTEXT OPERATIONS BENCHMARK")
    print("=" * 40)
    
    # Import context management components
    try:
        from src.core.context_scoring import ContextScorer
        from src.core.token_counting import ConversationTokenManager
        from src.core.context_formatting import ContextFormatter, FormatStyle
        from src.core.context_summarization import ContextSummarizer
        
        # Create test data
        sample_turns = [
            {
                "id": f"turn_{i}",
                "role": "user" if i % 2 == 0 else "assistant", 
                "content": f"Sample message {i} with some content to test performance " * 10,
                "timestamp": time.time() - (100 - i) * 60
            }
            for i in range(100)  # 100 turns for stress testing
        ]
        
        print(f"📝 Created {len(sample_turns)} test conversation turns")
        
        # Benchmark token counting
        start_time = time.time()
        token_manager = ConversationTokenManager()
        token_result = await token_manager.count_conversation_tokens(sample_turns)
        token_time = time.time() - start_time
        
        print(f"⏱️ Token counting: {token_time:.4f}s for {len(sample_turns)} turns")
        print(f"   Result: {token_result.token_count} tokens")
        
        # Benchmark context scoring
        start_time = time.time()
        scorer = ContextScorer()
        scores = await scorer.score_context_turns(sample_turns, query="test query")
        scoring_time = time.time() - start_time
        
        print(f"⏱️ Context scoring: {scoring_time:.4f}s for {len(sample_turns)} turns")
        print(f"   Average score: {sum(scores) / len(scores):.3f}")
        
        # Benchmark context formatting
        start_time = time.time()
        formatter = ContextFormatter()
        formatted = await formatter.format_conversation_turns(
            sample_turns[:20], FormatStyle.CONVERSATIONAL
        )
        formatting_time = time.time() - start_time
        
        print(f"⏱️ Context formatting: {formatting_time:.4f}s for 20 turns")
        print(f"   Output length: {len(formatted)} chars")
        
        # Benchmark summarization
        start_time = time.time()
        summarizer = ContextSummarizer()
        summary = await summarizer.summarize_turns(sample_turns[:50])
        summary_time = time.time() - start_time
        
        print(f"⏱️ Summarization: {summary_time:.4f}s for 50 turns")
        print(f"   Compression ratio: {summary.metadata.compression_ratio:.2f}x")
        
        # Overall performance assessment
        total_time = token_time + scoring_time + formatting_time + summary_time
        print(f"\n📊 PERFORMANCE SUMMARY:")
        print(f"   Total test time: {total_time:.4f}s")
        print(f"   Turns per second: {len(sample_turns) / total_time:.1f}")
        
        # Performance targets
        target_response_time = 0.5  # 500ms target
        if total_time < target_response_time:
            print(f"✅ Performance target met ({target_response_time}s)")
        else:
            print(f"⚠️ Performance target missed by {total_time - target_response_time:.3f}s")
            
        return {
            'token_time': token_time,
            'scoring_time': scoring_time, 
            'formatting_time': formatting_time,
            'summary_time': summary_time,
            'total_time': total_time,
            'meets_target': total_time < target_response_time
        }
        
    except Exception as e:
        print(f"❌ Error during benchmarking: {e}")
        return None

def identify_optimization_opportunities(benchmark_results):
    """Identify specific optimization opportunities"""
    
    print("\n🔧 OPTIMIZATION OPPORTUNITIES")
    print("=" * 35)
    
    if not benchmark_results:
        print("❌ No benchmark data available")
        return
    
    # Analyze timing breakdowns
    operations = [
        ('Token Counting', benchmark_results['token_time']),
        ('Context Scoring', benchmark_results['scoring_time']),
        ('Context Formatting', benchmark_results['formatting_time']),
        ('Summarization', benchmark_results['summary_time'])
    ]
    
    # Sort by time consumption
    operations.sort(key=lambda x: x[1], reverse=True)
    
    print("\n📈 OPERATIONS BY TIME CONSUMPTION:")
    for i, (operation, time_taken) in enumerate(operations, 1):
        percentage = (time_taken / benchmark_results['total_time']) * 100
        print(f"   {i}. {operation}: {time_taken:.4f}s ({percentage:.1f}%)")
    
    # Optimization recommendations
    print("\n💡 OPTIMIZATION RECOMMENDATIONS:")
    
    slowest_op, slowest_time = operations[0]
    if slowest_time > 0.1:  # More than 100ms
        print(f"   🎯 Priority 1: Optimize {slowest_op}")
        
        if slowest_op == "Token Counting":
            print("      - Implement LRU cache for repeated content")
            print("      - Use faster tokenizer libraries")
            print("      - Batch token counting operations")
            
        elif slowest_op == "Context Scoring":
            print("      - Implement parallel processing for scoring")
            print("      - Cache similarity computations")
            print("      - Use approximate scoring for large contexts")
            
        elif slowest_op == "Summarization":
            print("      - Move to background processing")
            print("      - Implement incremental summarization")
            print("      - Cache summary results")
            
        elif slowest_op == "Context Formatting":
            print("      - Pre-compile format templates")
            print("      - Stream formatting for large contexts")
            print("      - Cache formatted outputs")
    
    # Memory optimization
    print("\n💾 MEMORY OPTIMIZATION:")
    print("      - Implement memory pooling for large operations")
    print("      - Use streaming for large context processing") 
    print("      - Clear intermediate results promptly")
    
    # Concurrency optimization
    print("\n⚡ CONCURRENCY OPTIMIZATION:")
    print("      - Parallelize independent scoring operations")
    print("      - Use async/await for I/O operations")
    print("      - Implement background summarization tasks")

async def main():
    """Main performance analysis function"""
    
    print("🔍 STARTING CONTEXT MANAGEMENT PERFORMANCE ANALYSIS")
    print("=" * 65)
    
    # Analyze profiling data
    profiling_success = analyze_profiling_data()
    
    # Run benchmarks
    benchmark_results = await benchmark_context_operations()
    
    # Identify optimizations
    identify_optimization_opportunities(benchmark_results)
    
    print("\n✅ PERFORMANCE ANALYSIS COMPLETE")
    
    if benchmark_results and benchmark_results['meets_target']:
        print("🎉 System meets performance targets!")
    else:
        print("⚠️ Performance optimization needed")

if __name__ == "__main__":
    asyncio.run(main())