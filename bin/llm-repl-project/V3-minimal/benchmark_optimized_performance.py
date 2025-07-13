#!/usr/bin/env python3
"""
Comprehensive Performance Benchmark for Optimized Context Management

Validates Task 12.6 performance improvements:
- Enhanced token counting with caching
- Parallel context scoring  
- Background summarization processing
- Overall system responsiveness
"""

import asyncio
import time
import statistics
import logging
from typing import List, Dict, Any
from datetime import datetime, timezone

# Import optimized context management components
from src.core.token_counter import CachedTokenCounter, ConversationTokenManager
from src.core.context_scoring import ContextScorer, ConversationTurn
from src.core.context_formatting import ContextFormattingManager, FormatStyle
from src.core.summarization import SummarizationService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceBenchmark:
    """Comprehensive performance testing suite"""
    
    def __init__(self):
        self.results = {}
        
        # Initialize optimized components
        self.token_counter = CachedTokenCounter()
        self.token_manager = ConversationTokenManager(self.token_counter)
        self.context_scorer = ContextScorer()
        self.context_formatter = ContextFormattingManager()
        self.summarization_service = SummarizationService()
        
        # Create test data with varying sizes
        self.test_datasets = {
            'small': self._create_test_conversations(20),
            'medium': self._create_test_conversations(100), 
            'large': self._create_test_conversations(500),
            'xlarge': self._create_test_conversations(1000)
        }
        
    def _create_test_conversations(self, num_turns: int) -> List[ConversationTurn]:
        """Create test conversation turns"""
        turns = []
        base_time = datetime.now(timezone.utc)
        
        for i in range(num_turns):
            # Alternate between user and assistant
            role = "user" if i % 2 == 0 else "assistant"
            
            # Vary content length for realistic testing
            if i % 10 == 0:  # Every 10th turn is longer
                content = f"This is a longer test message {i} with more content to test performance. " * 5
            else:
                content = f"Test message {i} with standard length content."
            
            turn = ConversationTurn(
                id=str(i),
                content=content,
                role=role,
                timestamp=base_time.replace(microsecond=i * 1000),
                tokens=len(content.split()) * 1.3  # Rough token estimate
            )
            turns.append(turn)
            
        return turns
    
    async def benchmark_token_counting(self) -> Dict[str, Any]:
        """Benchmark optimized token counting performance"""
        print("\n🔢 BENCHMARKING TOKEN COUNTING PERFORMANCE")
        print("=" * 55)
        
        results = {}
        
        for dataset_name, turns in self.test_datasets.items():
            print(f"\n📊 Testing {dataset_name} dataset ({len(turns)} turns)")
            
            # Extract text content
            texts = [turn.content for turn in turns]
            
            # Test single token counting
            start_time = time.time()
            single_results = []
            for text in texts:
                result = self.token_counter.count_tokens(text, include_metadata=False)
                single_results.append(result)
            single_time = time.time() - start_time
            
            # Test batch token counting
            start_time = time.time()
            batch_results = self.token_counter.count_tokens_batch(texts)
            batch_time = time.time() - start_time
            
            # Test conversation token counting
            messages = [{'role': turn.role, 'content': turn.content} for turn in turns]
            start_time = time.time()
            conversation_result = self.token_manager.count_conversation_tokens(messages)
            conversation_time = time.time() - start_time
            
            # Get cache statistics
            cache_stats = self.token_counter.get_cache_stats()
            
            results[dataset_name] = {
                'turn_count': len(turns),
                'single_counting_time': single_time,
                'batch_counting_time': batch_time,
                'conversation_counting_time': conversation_time,
                'speedup_batch_vs_single': single_time / batch_time if batch_time > 0 else 0,
                'cache_hit_rate': cache_stats['hit_rate'],
                'total_tokens': conversation_result['total_tokens'],
                'tokens_per_second': len(turns) / single_time if single_time > 0 else 0
            }
            
            print(f"   Single counting: {single_time:.4f}s")
            print(f"   Batch counting: {batch_time:.4f}s ({single_time/batch_time:.1f}x speedup)")
            print(f"   Cache hit rate: {cache_stats['hit_rate']:.1%}")
            print(f"   Tokens/second: {len(turns)/single_time:.1f}")
        
        return results
    
    async def benchmark_context_scoring(self) -> Dict[str, Any]:
        """Benchmark parallel context scoring performance"""
        print("\n🎯 BENCHMARKING CONTEXT SCORING PERFORMANCE")
        print("=" * 55)
        
        results = {}
        test_query = "Help me implement user authentication with JWT tokens"
        
        for dataset_name, turns in self.test_datasets.items():
            print(f"\n📊 Testing {dataset_name} dataset ({len(turns)} turns)")
            
            # Test scoring performance
            start_time = time.time()
            scores = self.context_scorer.score_context_turns(turns, test_query)
            scoring_time = time.time() - start_time
            
            # Test optimal context selection
            start_time = time.time()
            optimal_turns = self.context_scorer.get_optimal_context(
                turns, test_query, max_tokens=2000
            )
            selection_time = time.time() - start_time
            
            results[dataset_name] = {
                'turn_count': len(turns),
                'scoring_time': scoring_time,
                'selection_time': selection_time,
                'selected_turns': len(optimal_turns),
                'turns_per_second': len(turns) / scoring_time if scoring_time > 0 else 0,
                'average_score': statistics.mean([s.combined_score for s in scores])
            }
            
            print(f"   Scoring time: {scoring_time:.4f}s")
            print(f"   Selection time: {selection_time:.4f}s")
            print(f"   Turns/second: {len(turns)/scoring_time:.1f}")
            print(f"   Selected {len(optimal_turns)}/{len(turns)} turns")
        
        return results
    
    async def benchmark_context_formatting(self) -> Dict[str, Any]:
        """Benchmark context formatting performance"""
        print("\n📝 BENCHMARKING CONTEXT FORMATTING PERFORMANCE")
        print("=" * 55)
        
        results = {}
        
        for dataset_name, turns in self.test_datasets.items():
            print(f"\n📊 Testing {dataset_name} dataset ({len(turns)} turns)")
            
            format_results = {}
            
            # Test each format style
            for style in FormatStyle:
                start_time = time.time()
                formatted = await self.context_formatter.format_context(
                    turns, style
                )
                format_time = time.time() - start_time
                
                format_results[style.name.lower()] = {
                    'time': format_time,
                    'output_length': len(formatted),
                    'turns_per_second': len(turns) / format_time if format_time > 0 else 0
                }
                
                print(f"   {style.name}: {format_time:.4f}s ({len(formatted)} chars)")
            
            results[dataset_name] = {
                'turn_count': len(turns),
                'format_results': format_results
            }
        
        return results
    
    async def benchmark_summarization(self) -> Dict[str, Any]:
        """Benchmark summarization performance"""
        print("\n📚 BENCHMARKING SUMMARIZATION PERFORMANCE")
        print("=" * 50)
        
        results = {}
        
        # Test only medium and large datasets for summarization
        test_datasets = {k: v for k, v in self.test_datasets.items() 
                        if k in ['medium', 'large']}
        
        for dataset_name, turns in test_datasets.items():
            print(f"\n📊 Testing {dataset_name} dataset ({len(turns)} turns)")
            
            # Test synchronous summarization
            start_time = time.time()
            summary = await self.summarization_service.generate_summary(turns)
            sync_time = time.time() - start_time
            
            # Test background summarization queue
            start_time = time.time()
            background_complete = asyncio.Event()
            
            def callback(result):
                background_complete.set()
            
            self.summarization_service.queue_background_summarization(turns, callback)
            
            # Wait for background completion
            await asyncio.wait_for(background_complete.wait(), timeout=30.0)
            background_time = time.time() - start_time
            
            results[dataset_name] = {
                'turn_count': len(turns),
                'sync_time': sync_time,
                'background_time': background_time,
                'compression_ratio': summary.metadata.compression_ratio,
                'summary_length': len(summary.content),
                'turns_per_second': len(turns) / sync_time if sync_time > 0 else 0
            }
            
            print(f"   Sync summarization: {sync_time:.4f}s")
            print(f"   Background queue: {background_time:.4f}s")
            print(f"   Compression ratio: {summary.metadata.compression_ratio:.1f}x")
            print(f"   Turns/second: {len(turns)/sync_time:.1f}")
        
        return results
    
    async def benchmark_end_to_end_performance(self) -> Dict[str, Any]:
        """Benchmark complete context management pipeline"""
        print("\n🚀 BENCHMARKING END-TO-END PERFORMANCE")
        print("=" * 50)
        
        results = {}
        test_query = "Explain the authentication implementation"
        
        for dataset_name, turns in self.test_datasets.items():
            print(f"\n📊 Testing {dataset_name} dataset ({len(turns)} turns)")
            
            # Simulate complete context management workflow
            start_time = time.time()
            
            # 1. Token counting
            messages = [{'role': turn.role, 'content': turn.content} for turn in turns]
            token_result = self.token_manager.count_conversation_tokens(messages)
            
            # 2. Context scoring and optimization  
            optimal_turns = self.context_scorer.get_optimal_context(
                turns, test_query, max_tokens=3000
            )
            
            # 3. Context formatting
            formatted_context = await self.context_formatter.format_context(
                optimal_turns, FormatStyle.CONVERSATIONAL
            )
            
            # 4. Check if summarization needed
            should_summarize, trigger = self.summarization_service.should_summarize(
                turns, token_result['total_tokens']
            )
            
            total_time = time.time() - start_time
            
            results[dataset_name] = {
                'turn_count': len(turns),
                'total_time': total_time,
                'original_tokens': token_result['total_tokens'],
                'selected_turns': len(optimal_turns),
                'formatted_length': len(formatted_context),
                'should_summarize': should_summarize,
                'trigger': trigger.name if trigger else None,
                'throughput': len(turns) / total_time if total_time > 0 else 0,
                'meets_target': total_time < 0.5  # 500ms target
            }
            
            print(f"   Total time: {total_time:.4f}s")
            print(f"   Selected {len(optimal_turns)}/{len(turns)} turns")
            print(f"   Throughput: {len(turns)/total_time:.1f} turns/second")
            print(f"   Target met: {'✅' if total_time < 0.5 else '❌'}")
        
        return results
    
    def generate_performance_report(self, all_results: Dict[str, Any]):
        """Generate comprehensive performance report"""
        print("\n" + "=" * 70)
        print("🎉 PERFORMANCE OPTIMIZATION REPORT - TASK 12.6")
        print("=" * 70)
        
        # Token counting improvements
        print("\n📈 TOKEN COUNTING OPTIMIZATIONS:")
        for dataset, results in all_results['token_counting'].items():
            hit_rate = results['cache_hit_rate']
            speedup = results['speedup_batch_vs_single']
            print(f"   {dataset}: {hit_rate:.1%} cache hit rate, {speedup:.1f}x batch speedup")
        
        # Context scoring improvements  
        print("\n⚡ CONTEXT SCORING OPTIMIZATIONS:")
        for dataset, results in all_results['context_scoring'].items():
            tps = results['turns_per_second']
            print(f"   {dataset}: {tps:.1f} turns/second")
        
        # End-to-end performance
        print("\n🎯 END-TO-END PERFORMANCE:")
        targets_met = 0
        total_tests = 0
        
        for dataset, results in all_results['end_to_end'].items():
            total_time = results['total_time']
            meets_target = results['meets_target']
            throughput = results['throughput']
            
            if meets_target:
                targets_met += 1
            total_tests += 1
            
            status = "✅ PASS" if meets_target else "❌ FAIL"
            print(f"   {dataset}: {total_time:.4f}s ({throughput:.1f} turns/sec) {status}")
        
        # Overall assessment
        print(f"\n🏆 OVERALL ASSESSMENT:")
        print(f"   Performance targets met: {targets_met}/{total_tests}")
        
        if targets_met == total_tests:
            print("   🎉 ALL PERFORMANCE TARGETS ACHIEVED!")
            print("   ✅ Task 12.6 'Optimize Performance' - COMPLETE")
        else:
            print("   ⚠️ Some performance targets not met")
            print("   📝 Additional optimization may be needed")
        
        # Optimization summary
        print(f"\n💡 KEY OPTIMIZATIONS IMPLEMENTED:")
        print("   ✅ Enhanced token counting cache (2000 entries)")
        print("   ✅ Batch token processing with pre-hashing")
        print("   ✅ Parallel context scoring (4 threads)")
        print("   ✅ Background summarization processing")
        print("   ✅ Memory-efficient caching strategies")
        print("   ✅ Early returns for empty content")
        
        return targets_met == total_tests

async def main():
    """Run comprehensive performance benchmark"""
    
    print("🔍 STARTING TASK 12.6 PERFORMANCE VALIDATION")
    print("=" * 60)
    print("Testing optimized context management system...")
    
    benchmark = PerformanceBenchmark()
    
    try:
        # Run all benchmarks
        results = {}
        
        results['token_counting'] = await benchmark.benchmark_token_counting()
        results['context_scoring'] = await benchmark.benchmark_context_scoring()
        results['context_formatting'] = await benchmark.benchmark_context_formatting()
        results['summarization'] = await benchmark.benchmark_summarization()
        results['end_to_end'] = await benchmark.benchmark_end_to_end_performance()
        
        # Generate final report
        success = benchmark.generate_performance_report(results)
        
        return success
        
    finally:
        # Clean up background processing
        benchmark.summarization_service.shutdown()

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)