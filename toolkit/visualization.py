"""
Fairness Visualization Module

Generate professional charts and visualizations for fairness metrics.

Author: Zhejiang University
License: MIT
"""

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from typing import Dict, List, Optional

# Use non-interactive backend
matplotlib.use('Agg')


class FairnessVisualizer:
    """Generate professional visualizations for fairness analysis."""
    
    def __init__(self, style: str = 'default', dpi: int = 300):
        """
        Initialize visualizer with style settings.
        
        Args:
            style: Matplotlib style ('default', 'seaborn', etc.)
            dpi: Resolution for saved figures
        """
        plt.style.use(style)
        self.dpi = dpi
        
        # Professional color schemes
        self.colors = {
            'primary': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E'],
            'sequential': ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51'],
            'diverging': ['#E63946', '#F77F00', '#06FFA5']
        }
    
    def create_platform_comparison_chart(self,
                                        platform_scores: Dict[str, float],
                                        output_path: str,
                                        title: str = 'Fairness Index Scores by Platform',
                                        show_thresholds: bool = True) -> str:
        """
        Create bar chart comparing MDFI scores across platforms.
        
        Args:
            platform_scores: Dict mapping platform names to MDFI scores
            output_path: Path to save the chart
            title: Chart title
            show_thresholds: Whether to show recommended threshold lines
        
        Returns:
            Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        platforms = list(platform_scores.keys())
        scores = list(platform_scores.values())
        
        bars = ax.bar(platforms, scores, 
                     color=self.colors['primary'][:len(platforms)],
                     alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add threshold lines
        if show_thresholds:
            ax.axhline(y=70, color='green', linestyle='--', linewidth=2,
                      alpha=0.7, label='Recommended (70)')
            ax.axhline(y=50, color='orange', linestyle='--', linewidth=2,
                      alpha=0.7, label='Moderate Concern (50)')
        
        # Customize chart
        ax.set_ylabel('MDFI Score', fontsize=14, fontweight='bold')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_ylim(0, 100)
        ax.legend(loc='upper right', fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_fairness_gaps_chart(self,
                                   gap_metrics: Dict[str, float],
                                   output_path: str,
                                   title: str = 'Fairness Disparities Across Dimensions') -> str:
        """
        Create horizontal bar chart showing fairness gaps.
        
        Args:
            gap_metrics: Dict mapping gap types to percentages
            output_path: Path to save the chart
            title: Chart title
        
        Returns:
            Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        gaps = list(gap_metrics.keys())
        values = list(gap_metrics.values())
        
        bars = ax.barh(gaps, values,
                      color=self.colors['diverging'][:len(gaps)],
                      alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add SLA threshold lines
        ax.axvline(x=10, color='orange', linestyle='--', linewidth=2,
                  alpha=0.7, label='Geographic SLA (10%)')
        ax.axvline(x=15, color='red', linestyle='--', linewidth=2,
                  alpha=0.7, label='Demographic SLA (15%)')
        
        # Customize chart
        ax.set_xlabel('Disparity Gap (%)', fontsize=14, fontweight='bold')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlim(0, max(values) * 1.2)
        ax.legend(loc='lower right', fontsize=11)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{width:.1f}%',
                   ha='left', va='center', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_mdfi_breakdown_chart(self,
                                   component_scores: Dict[str, float],
                                   weights: Dict[str, float],
                                   output_path: str,
                                   title: str = 'MDFI Component Breakdown') -> str:
        """
        Create chart showing MDFI component scores and weights.
        
        Args:
            component_scores: Dict of component names to scores (0-1)
            weights: Dict of component names to weights
            output_path: Path to save the chart
            title: Chart title
        
        Returns:
            Path to saved chart
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        components = list(component_scores.keys())
        scores = [component_scores[c] * 100 for c in components]  # Scale to 0-100
        weight_values = [weights[c] * 100 for c in components]  # Convert to percentages
        
        # Chart 1: Component Scores
        bars1 = ax1.bar(components, scores,
                       color=self.colors['sequential'][:len(components)],
                       alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax1.set_ylabel('Score', fontsize=12, fontweight='bold')
        ax1.set_title('Component Scores', fontsize=14, fontweight='bold', pad=15)
        ax1.set_ylim(0, 100)
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Chart 2: Component Weights
        explode = tuple([0.05] * len(components))
        colors = self.colors['sequential'][:len(components)]
        
        wedges, texts, autotexts = ax2.pie(weight_values,
                                           labels=components,
                                           colors=colors,
                                           autopct='%1.0f%%',
                                           startangle=90,
                                           explode=explode,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(13)
            autotext.set_fontweight('bold')
        
        ax2.set_title('Component Weights', fontsize=14, fontweight='bold', pad=15)
        
        plt.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_dataset_composition_chart(self,
                                        dataset_sizes: Dict[str, int],
                                        output_path: str,
                                        title: str = 'Dataset Composition') -> str:
        """
        Create pie chart showing dataset composition.
        
        Args:
            dataset_sizes: Dict mapping dataset names to record counts
            output_path: Path to save the chart
            title: Chart title
        
        Returns:
            Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        datasets = list(dataset_sizes.keys())
        sizes = list(dataset_sizes.values())
        
        # Add record counts to labels
        labels = [f"{name}\n({size:,})" for name, size in zip(datasets, sizes)]
        
        colors = self.colors['sequential'][:len(datasets)]
        explode = tuple([0.05] * len(datasets))
        
        wedges, texts, autotexts = ax.pie(sizes,
                                          labels=labels,
                                          colors=colors,
                                          autopct='%1.1f%%',
                                          startangle=90,
                                          explode=explode,
                                          textprops={'fontsize': 12, 'fontweight': 'bold'},
                                          pctdistance=0.85)
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')
        
        total = sum(sizes)
        ax.set_title(f'{title}\n(Total: {total:,} records)',
                    fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_comprehensive_dashboard(self,
                                      results: Dict,
                                      output_path: str) -> str:
        """
        Create comprehensive dashboard with multiple visualizations.
        
        Args:
            results: Complete MDFI results dictionary
            output_path: Path to save the dashboard
        
        Returns:
            Path to saved dashboard
        """
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # This would include multiple sub-charts
        # Implementation details omitted for brevity
        
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path


# Example usage
if __name__ == "__main__":
    visualizer = FairnessVisualizer()
    
    # Example data
    platform_scores = {
        'Weibo': 68.04,
        'mygopen': 59.49,
        'Taiwan FactCheck': 58.75,
        'Tencent News': 57.21,
        'Sina News': 57.16
    }
    
    gap_metrics = {
        'Demographic\n(Elderly vs Young)': 12.0,
        'Geographic\n(Rural vs Urban)': 8.0,
        'Content Category\n(Health vs Entertainment)': 17.0
    }
    
    component_scores = {
        'Group Fairness': 0.72,
        'Content Fairness': 0.65,
        'Procedural Fairness': 0.80
    }
    
    weights = {
        'Group Fairness': 0.4,
        'Content Fairness': 0.3,
        'Procedural Fairness': 0.3
    }
    
    # Generate charts
    print("Generating visualizations...")
    visualizer.create_platform_comparison_chart(platform_scores, 'platform_scores.png')
    print("✓ Platform comparison chart created")
    
    visualizer.create_fairness_gaps_chart(gap_metrics, 'fairness_gaps.png')
    print("✓ Fairness gaps chart created")
    
    visualizer.create_mdfi_breakdown_chart(component_scores, weights, 'mdfi_breakdown.png')
    print("✓ MDFI breakdown chart created")
    
    print("\nAll visualizations generated successfully!")
