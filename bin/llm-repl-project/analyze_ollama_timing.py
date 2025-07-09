#!/usr/bin/env python3
"""
Comprehensive Ollama Model Timing Analysis Script

This script performs statistical analysis of Ollama model performance to derive
accurate timing functions f(input_tokens, output_tokens) = request_duration.

Features:
- Tests multiple token count ranges (10-1000+ tokens)
- Multiple iterations per test point for statistical significance
- Fits polynomial, exponential, and linear models
- Outputs R-style statistical analysis
- Generates timing function coefficients for production use
"""

import asyncio
import aiohttp
import time
import json
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any
import argparse
from pathlib import Path

class OllamaTimingAnalyzer:
    """Comprehensive timing analysis for Ollama models."""
    
    def __init__(self, model_name: str = "tinyllama", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.results: List[Dict[str, Any]] = []
        
    async def single_request_timing(self, prompt: str) -> Tuple[float, int, int]:
        """
        Make a single timed request to Ollama and return (duration, input_tokens, output_tokens).
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,  # Get complete response for accurate timing
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "repeat_penalty": 1.1
            }
        }
        
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")
                    
                    data = await response.json()
                    end_time = time.time()
                    
                    # Extract timing and token information
                    duration = end_time - start_time
                    
                    # Ollama provides token counts in the response
                    input_tokens = data.get('prompt_eval_count', len(prompt.split()) * 1.3)  # Fallback estimate
                    output_tokens = data.get('eval_count', len(data.get('response', '').split()))
                    
                    return duration, int(input_tokens), int(output_tokens)
                    
            except Exception as e:
                print(f"Request failed: {e}")
                return 0.0, 0, 0
    
    def generate_test_prompts(self) -> List[Tuple[str, int]]:
        """Generate prompts of varying lengths for comprehensive testing."""
        
        prompts = []
        
        # Short prompts (10-50 tokens)
        base_short = "What is"
        for i in range(10, 51, 10):
            prompt = f"{base_short} " + "the meaning of " * (i // 4)
            prompts.append((prompt, i))
        
        # Medium prompts (50-200 tokens)
        base_medium = "Explain the concept of machine learning and its applications in"
        for i in range(50, 201, 25):
            additions = " and data science" * (i // 20)
            prompt = f"{base_medium}{additions}. Provide detailed examples."
            prompts.append((prompt, i))
        
        # Long prompts (200-500 tokens)
        base_long = """
        Write a comprehensive analysis of the following topic, including historical context,
        current applications, future implications, and detailed examples with explanations.
        Consider multiple perspectives and provide evidence-based conclusions.
        """
        for i in range(200, 501, 50):
            filler = " Additionally, discuss the societal impact and technological implications." * (i // 30)
            prompt = f"{base_long}{filler}"
            prompts.append((prompt, i))
        
        # Very long prompts (500-1000+ tokens)
        base_very_long = """
        Provide an exhaustive analysis covering: 1) Historical development and evolution,
        2) Current state of technology and implementations, 3) Detailed technical specifications,
        4) Comparative analysis with alternative approaches, 5) Future research directions,
        6) Potential challenges and limitations, 7) Real-world case studies and examples,
        8) Economic and social implications, 9) Ethical considerations and best practices,
        10) Recommendations for implementation and adoption strategies.
        """
        for i in range(500, 1001, 100):
            filler = " Include statistical data, research findings, and expert opinions." * (i // 50)
            prompt = f"{base_very_long}{filler}"
            prompts.append((prompt, i))
        
        return prompts
    
    async def run_timing_analysis(self, iterations_per_prompt: int = 3) -> pd.DataFrame:
        """
        Run comprehensive timing analysis across all prompt lengths.
        """
        print(f"🔬 Starting timing analysis for {self.model_name}")
        print(f"📊 Testing with {iterations_per_prompt} iterations per prompt length")
        
        test_prompts = self.generate_test_prompts()
        
        for prompt, estimated_tokens in test_prompts:
            print(f"\n📝 Testing prompt length ~{estimated_tokens} tokens...")
            
            for iteration in range(iterations_per_prompt):
                print(f"  Iteration {iteration + 1}/{iterations_per_prompt}...", end=" ")
                
                duration, actual_input_tokens, output_tokens = await self.single_request_timing(prompt)
                
                if duration > 0:  # Valid response
                    result = {
                        'estimated_input_tokens': estimated_tokens,
                        'actual_input_tokens': actual_input_tokens,
                        'output_tokens': output_tokens,
                        'total_tokens': actual_input_tokens + output_tokens,
                        'duration_seconds': duration,
                        'tokens_per_second': (actual_input_tokens + output_tokens) / duration if duration > 0 else 0,
                        'iteration': iteration,
                        'prompt_preview': prompt[:50] + "..." if len(prompt) > 50 else prompt
                    }
                    self.results.append(result)
                    print(f"✅ {duration:.2f}s, {actual_input_tokens}+{output_tokens} tokens")
                else:
                    print("❌ Failed")
                
                # Small delay between requests
                await asyncio.sleep(0.5)
        
        df = pd.DataFrame(self.results)
        return df
    
    def fit_timing_functions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Fit various mathematical models to the timing data and find the best fit.
        """
        print("\n🧮 Fitting timing functions...")
        
        # Prepare data
        X_input = df['actual_input_tokens'].values
        X_output = df['output_tokens'].values  
        X_total = df['total_tokens'].values
        y = df['duration_seconds'].values
        
        models = {}
        
        # 1. Linear model: duration = a*input + b*output + c
        def linear_model(X, a, b, c):
            input_tokens, output_tokens = X
            return a * input_tokens + b * output_tokens + c
        
        try:
            popt_linear, pcov_linear = curve_fit(linear_model, (X_input, X_output), y)
            y_pred_linear = linear_model((X_input, X_output), *popt_linear)
            r2_linear = stats.pearsonr(y, y_pred_linear)[0] ** 2
            
            models['linear'] = {
                'function': 'a*input + b*output + c',
                'coefficients': {'a': popt_linear[0], 'b': popt_linear[1], 'c': popt_linear[2]},
                'r_squared': r2_linear,
                'rmse': np.sqrt(np.mean((y - y_pred_linear) ** 2))
            }
            print(f"📈 Linear model: R² = {r2_linear:.4f}")
        except Exception as e:
            print(f"❌ Linear model fitting failed: {e}")
        
        # 2. Polynomial model: duration = a*total² + b*total + c
        def poly_model(total_tokens, a, b, c):
            return a * total_tokens**2 + b * total_tokens + c
        
        try:
            popt_poly, pcov_poly = curve_fit(poly_model, X_total, y)
            y_pred_poly = poly_model(X_total, *popt_poly)
            r2_poly = stats.pearsonr(y, y_pred_poly)[0] ** 2
            
            models['polynomial'] = {
                'function': 'a*total² + b*total + c',
                'coefficients': {'a': popt_poly[0], 'b': popt_poly[1], 'c': popt_poly[2]},
                'r_squared': r2_poly,
                'rmse': np.sqrt(np.mean((y - y_pred_poly) ** 2))
            }
            print(f"📈 Polynomial model: R² = {r2_poly:.4f}")
        except Exception as e:
            print(f"❌ Polynomial model fitting failed: {e}")
        
        # 3. Power law model: duration = a * total^b + c
        def power_model(total_tokens, a, b, c):
            return a * np.power(total_tokens, b) + c
        
        try:
            popt_power, pcov_power = curve_fit(power_model, X_total, y, p0=[0.01, 1.2, 0.5])
            y_pred_power = power_model(X_total, *popt_power)
            r2_power = stats.pearsonr(y, y_pred_power)[0] ** 2
            
            models['power'] = {
                'function': 'a*total^b + c',
                'coefficients': {'a': popt_power[0], 'b': popt_power[1], 'c': popt_power[2]},
                'r_squared': r2_power,
                'rmse': np.sqrt(np.mean((y - y_pred_power) ** 2))
            }
            print(f"📈 Power model: R² = {r2_power:.4f}")
        except Exception as e:
            print(f"❌ Power model fitting failed: {e}")
        
        # Find best model
        if models:
            best_model_name = max(models.keys(), key=lambda k: models[k]['r_squared'])
            models['best_model'] = best_model_name
            print(f"🏆 Best model: {best_model_name} (R² = {models[best_model_name]['r_squared']:.4f})")
        
        return models
    
    def generate_production_code(self, models: Dict[str, Any]) -> str:
        """
        Generate production Python code with the fitted timing functions.
        """
        if 'best_model' not in models:
            return "# No valid models fitted"
        
        best_model = models[models['best_model']]
        coeffs = best_model['coefficients']
        
        code = f'''
class OptimizedTokenRateEstimator:
    """
    Optimized token rate estimator based on statistical analysis of {self.model_name}.
    
    Model: {best_model['function']}
    R-squared: {best_model['r_squared']:.4f}
    RMSE: {best_model['rmse']:.4f} seconds
    """
    
    def __init__(self):
        # Fitted coefficients from statistical analysis
        self.model_type = "{models['best_model']}"
        self.coefficients = {coeffs}
        self.r_squared = {best_model['r_squared']:.4f}
    
    def estimate_duration(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate request duration based on fitted model."""
        if self.model_type == "linear":
            return (self.coefficients['a'] * input_tokens + 
                   self.coefficients['b'] * output_tokens + 
                   self.coefficients['c'])
        elif self.model_type == "polynomial":
            total_tokens = input_tokens + output_tokens
            return (self.coefficients['a'] * total_tokens**2 + 
                   self.coefficients['b'] * total_tokens + 
                   self.coefficients['c'])
        elif self.model_type == "power":
            total_tokens = input_tokens + output_tokens
            return (self.coefficients['a'] * (total_tokens ** self.coefficients['b']) + 
                   self.coefficients['c'])
        else:
            # Fallback
            return 0.5 + (input_tokens + output_tokens) * 0.02
    
    def get_processing_rates(self, input_tokens: int, output_tokens: int) -> dict:
        """Get estimated processing rates for animation purposes."""
        duration = self.estimate_duration(input_tokens, output_tokens)
        
        # Rough estimates for input vs output processing phases
        input_phase_duration = duration * 0.3  # 30% for input processing
        output_phase_duration = duration * 0.7  # 70% for output generation
        
        return {{
            'total_duration': duration,
            'input_tokens_per_second': input_tokens / input_phase_duration if input_phase_duration > 0 else 50,
            'output_tokens_per_second': output_tokens / output_phase_duration if output_phase_duration > 0 else 25,
            'latency_seconds': 0.1  # Minimal latency
        }}
'''
        return code
    
    def save_results(self, df: pd.DataFrame, models: Dict[str, Any], output_dir: str = "timing_analysis"):
        """Save all analysis results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save raw data
        df.to_csv(output_path / f"{self.model_name}_timing_data.csv", index=False)
        
        # Save model analysis
        with open(output_path / f"{self.model_name}_models.json", 'w') as f:
            json.dump(models, f, indent=2)
        
        # Save production code
        production_code = self.generate_production_code(models)
        with open(output_path / f"{self.model_name}_optimized_estimator.py", 'w') as f:
            f.write(production_code)
        
        print(f"\n💾 Results saved to {output_path}/")
        print(f"📊 Raw data: {self.model_name}_timing_data.csv")
        print(f"📈 Models: {self.model_name}_models.json")
        print(f"🚀 Production code: {self.model_name}_optimized_estimator.py")

async def main():
    parser = argparse.ArgumentParser(description="Analyze Ollama model timing performance")
    parser.add_argument("--model", default="tinyllama", help="Ollama model name")
    parser.add_argument("--iterations", type=int, default=3, help="Iterations per test point")
    parser.add_argument("--output", default="timing_analysis", help="Output directory")
    
    args = parser.parse_args()
    
    print(f"🔬 Ollama Timing Analysis for {args.model}")
    print("=" * 50)
    
    analyzer = OllamaTimingAnalyzer(args.model)
    
    # Run analysis
    df = await analyzer.run_timing_analysis(args.iterations)
    
    if df.empty:
        print("❌ No valid timing data collected. Check Ollama server.")
        return
    
    # Fit models
    models = analyzer.fit_timing_functions(df)
    
    # Save results
    analyzer.save_results(df, models, args.output)
    
    # Print summary
    print("\n📊 ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total requests: {len(df)}")
    print(f"Average duration: {df['duration_seconds'].mean():.2f}s")
    print(f"Token range: {df['total_tokens'].min()}-{df['total_tokens'].max()} tokens")
    print(f"Average tokens/sec: {df['tokens_per_second'].mean():.1f}")
    
    if models and 'best_model' in models:
        best = models[models['best_model']]
        print(f"Best model: {models['best_model']} (R² = {best['r_squared']:.4f})")

if __name__ == "__main__":
    asyncio.run(main())