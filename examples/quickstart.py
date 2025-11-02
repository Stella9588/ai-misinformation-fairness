"""
Quickstart Example for MDFI Framework

This script demonstrates basic usage of the Multi-Dimensional Fairness Index (MDFI)
calculator and visualization tools.

Run: python examples/quickstart.py
"""

import sys
import os

# Add toolkit to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from toolkit.mdfi_calculator import MDFICalculator
from toolkit.visualization import FairnessVisualizer


def generate_sample_data(n_samples=1000):
    """Generate sample misinformation detection data."""
    np.random.seed(42)
    
    # Simulate detection results
    data = pd.DataFrame({
        # Model predictions and ground truth
        'predicted': np.random.randint(0, 2, n_samples),
        'label': np.random.randint(0, 2, n_samples),
        
        # Demographic information
        'age_group': np.random.choice(['young', 'elderly'], n_samples, p=[0.7, 0.3]),
        
        # Geographic information
        'location': np.random.choice(['urban', 'rural'], n_samples, p=[0.6, 0.4]),
        
        # Content categories
        'content_category': np.random.choice(
            ['health', 'entertainment', 'politics'], 
            n_samples, 
            p=[0.3, 0.5, 0.2]
        ),
        
        # Procedural fairness indicators
        'has_explanation': np.random.choice([True, False], n_samples, p=[0.85, 0.15]),
        'appeal_time_hours': np.random.normal(60, 20, n_samples).clip(0, 200)
    })
    
    return data


def main():
    """Main quickstart demonstration."""
    print("="*70)
    print("MDFI FRAMEWORK - QUICKSTART EXAMPLE")
    print("="*70)
    print()
    
    # Step 1: Generate or load data
    print("Step 1: Loading sample data...")
    data = generate_sample_data(n_samples=1000)
    print(f"✓ Loaded {len(data)} records")
    print(f"  - Demographics: {data['age_group'].nunique()} groups")
    print(f"  - Locations: {data['location'].nunique()} regions")
    print(f"  - Content types: {data['content_category'].nunique()} categories")
    print()
    
    # Step 2: Initialize MDFI Calculator
    print("Step 2: Initializing MDFI Calculator...")
    calculator = MDFICalculator(
        group_weight=0.4,
        content_weight=0.3,
        procedural_weight=0.3
    )
    print("✓ Calculator initialized")
    print()
    
    # Step 3: Calculate MDFI Score
    print("Step 3: Calculating MDFI scores...")
    results = calculator.calculate_mdfi(
        data=data,
        prediction_col='predicted',
        label_col='label',
        demographic_col='age_group',
        geographic_col='location',
        content_col='content_category',
        explanation_col='has_explanation',
        appeal_time_col='appeal_time_hours'
    )
    print("✓ MDFI calculation complete")
    print()
    
    # Step 4: Display Results
    print("="*70)
    print("FAIRNESS ASSESSMENT RESULTS")
    print("="*70)
    print()
    
    print(f"📊 OVERALL MDFI SCORE: {results['overall_score']:.2f}/100")
    print(f"   Interpretation: {results['interpretation']}")
    print()
    
    print("Component Scores:")
    print(f"  • Group Fairness:      {results['group_fairness']*100:.2f}/100")
    print(f"  • Content Fairness:    {results['content_fairness']*100:.2f}/100")
    print(f"  • Procedural Fairness: {results['procedural_fairness']*100:.2f}/100")
    print()
    
    # Step 5: Generate Visualizations
    print("Step 5: Generating visualizations...")
    visualizer = FairnessVisualizer()
    
    # Platform comparison (using sample data)
    platform_scores = {
        'Platform A': results['overall_score'],
        'Platform B': results['overall_score'] - 5,
        'Platform C': results['overall_score'] + 3
    }
    
    visualizer.create_platform_comparison_chart(
        platform_scores,
        'output_platform_comparison.png',
        title='Platform Fairness Comparison'
    )
    print("✓ Created: output_platform_comparison.png")
    
    # Fairness gaps
    gap_metrics = {
        'Demographic Gap': 12.0,
        'Geographic Gap': 8.0,
        'Content Gap': 17.0
    }
    
    visualizer.create_fairness_gaps_chart(
        gap_metrics,
        'output_fairness_gaps.png',
        title='Fairness Disparities'
    )
    print("✓ Created: output_fairness_gaps.png")
    
    # MDFI breakdown
    component_scores = {
        'Group Fairness': results['group_fairness'],
        'Content Fairness': results['content_fairness'],
        'Procedural Fairness': results['procedural_fairness']
    }
    
    weights = {
        'Group Fairness': 0.4,
        'Content Fairness': 0.3,
        'Procedural Fairness': 0.3
    }
    
    visualizer.create_mdfi_breakdown_chart(
        component_scores,
        weights,
        'output_mdfi_breakdown.png',
        title='MDFI Component Analysis'
    )
    print("✓ Created: output_mdfi_breakdown.png")
    print()
    
    # Step 6: Interpretation and Recommendations
    print("="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    print()
    
    if results['overall_score'] >= 70:
        print("✓ ACCEPTABLE FAIRNESS")
        print("  Your system meets the recommended fairness threshold.")
        print("  Continue monitoring for any degradation over time.")
    elif results['overall_score'] >= 50:
        print("⚠ MODERATE CONCERNS")
        print("  Your system shows fairness issues requiring attention:")
        print("  • Review demographic disparities")
        print("  • Improve content category balance")
        print("  • Enhance procedural transparency")
    else:
        print("🚨 URGENT INTERVENTION NEEDED")
        print("  Your system has significant fairness problems:")
        print("  • Implement immediate fairness audits")
        print("  • Adjust detection thresholds for disadvantaged groups")
        print("  • Establish appeal mechanisms")
        print("  • Diversify training data")
    
    print()
    print("="*70)
    print("QUICKSTART COMPLETE!")
    print("="*70)
    print()
    print("Next steps:")
    print("  1. Review the generated visualization files")
    print("  2. See docs/USAGE_GUIDE.md for detailed documentation")
    print("  3. Try examples/platform_comparison.py for multi-platform analysis")
    print()
    print("For questions or issues, visit:")
    print("  https://github.com/yourusername/ai-misinformation-fairness/issues")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nFor help, please check the documentation or open an issue on GitHub.")
        sys.exit(1)
