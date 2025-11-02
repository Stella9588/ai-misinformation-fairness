"""
Multi-Dimensional Fairness Index (MDFI) Calculator

This module provides the core implementation for calculating fairness metrics
in AI-based misinformation detection systems.

Author: Zhejiang University
License: MIT
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


class MDFICalculator:
    """
    Calculate Multi-Dimensional Fairness Index (MDFI) scores.
    
    The MDFI combines three dimensions:
    - Group Fairness (40%): Demographic and geographic equity
    - Content Fairness (30%): Accuracy consistency across content types
    - Procedural Fairness (30%): Transparency and appeal mechanisms
    """
    
    def __init__(self, 
                 group_weight: float = 0.4,
                 content_weight: float = 0.3,
                 procedural_weight: float = 0.3):
        """
        Initialize MDFI Calculator with component weights.
        
        Args:
            group_weight: Weight for group fairness component (default: 0.4)
            content_weight: Weight for content fairness component (default: 0.3)
            procedural_weight: Weight for procedural fairness component (default: 0.3)
        """
        assert abs(group_weight + content_weight + procedural_weight - 1.0) < 0.001, \
            "Weights must sum to 1.0"
        
        self.group_weight = group_weight
        self.content_weight = content_weight
        self.procedural_weight = procedural_weight
    
    def calculate_mdfi(self,
                      data: pd.DataFrame,
                      prediction_col: str = 'predicted',
                      label_col: str = 'label',
                      demographic_col: Optional[str] = None,
                      geographic_col: Optional[str] = None,
                      content_col: Optional[str] = None,
                      explanation_col: Optional[str] = None,
                      appeal_time_col: Optional[str] = None) -> Dict:
        """
        Calculate complete MDFI score and component scores.
        
        Args:
            data: DataFrame containing detection results and metadata
            prediction_col: Column name for model predictions (0/1)
            label_col: Column name for ground truth labels (0/1)
            demographic_col: Column name for demographic groups (e.g., 'age_group')
            geographic_col: Column name for geographic regions (e.g., 'location')
            content_col: Column name for content categories (e.g., 'topic')
            explanation_col: Column name indicating explanation availability (boolean)
            appeal_time_col: Column name for appeal resolution time (hours)
        
        Returns:
            Dictionary containing MDFI score and component scores
        """
        results = {}
        
        # Calculate Group Fairness
        if demographic_col or geographic_col:
            gf_score = self.calculate_group_fairness(
                data, prediction_col, label_col, 
                demographic_col, geographic_col
            )
            results['group_fairness'] = gf_score
        else:
            results['group_fairness'] = None
            print("Warning: No demographic/geographic columns provided for group fairness")
        
        # Calculate Content Fairness
        if content_col:
            cf_score = self.calculate_content_fairness(
                data, prediction_col, label_col, content_col
            )
            results['content_fairness'] = cf_score
        else:
            results['content_fairness'] = None
            print("Warning: No content category column provided for content fairness")
        
        # Calculate Procedural Fairness
        if explanation_col or appeal_time_col:
            pf_score = self.calculate_procedural_fairness(
                data, explanation_col, appeal_time_col
            )
            results['procedural_fairness'] = pf_score
        else:
            results['procedural_fairness'] = None
            print("Warning: No procedural columns provided for procedural fairness")
        
        # Calculate Overall MDFI Score
        scores = [
            results['group_fairness'] if results['group_fairness'] is not None else 0.0,
            results['content_fairness'] if results['content_fairness'] is not None else 0.0,
            results['procedural_fairness'] if results['procedural_fairness'] is not None else 0.0
        ]
        
        # Scale to 0-100
        overall_score = (
            scores[0] * self.group_weight + 
            scores[1] * self.content_weight + 
            scores[2] * self.procedural_weight
        ) * 100
        
        results['overall_score'] = overall_score
        results['interpretation'] = self._interpret_score(overall_score)
        
        return results
    
    def calculate_group_fairness(self,
                                 data: pd.DataFrame,
                                 prediction_col: str,
                                 label_col: str,
                                 demographic_col: Optional[str] = None,
                                 geographic_col: Optional[str] = None) -> float:
        """
        Calculate group fairness score based on FPR and TPR disparities.
        
        Group Fairness = 1 - max(FPR_disparity, TPR_disparity)
        
        Args:
            data: DataFrame with predictions and labels
            prediction_col: Column name for predictions
            label_col: Column name for true labels
            demographic_col: Column for demographic groups
            geographic_col: Column for geographic regions
        
        Returns:
            Group fairness score (0-1, higher is better)
        """
        disparities = []
        
        # Calculate demographic disparity if provided
        if demographic_col and demographic_col in data.columns:
            demo_disparity = self._calculate_group_disparity(
                data, prediction_col, label_col, demographic_col
            )
            disparities.append(demo_disparity)
        
        # Calculate geographic disparity if provided
        if geographic_col and geographic_col in data.columns:
            geo_disparity = self._calculate_group_disparity(
                data, prediction_col, label_col, geographic_col
            )
            disparities.append(geo_disparity)
        
        if not disparities:
            return 0.0
        
        # Take maximum disparity (worst case)
        max_disparity = max(disparities)
        
        # Convert to fairness score (1 = perfect fairness)
        group_fairness = 1.0 - max_disparity
        
        return max(0.0, group_fairness)
    
    def _calculate_group_disparity(self,
                                   data: pd.DataFrame,
                                   prediction_col: str,
                                   label_col: str,
                                   group_col: str) -> float:
        """Calculate FPR/TPR disparity between groups."""
        groups = data[group_col].unique()
        
        if len(groups) < 2:
            return 0.0
        
        fpr_scores = []
        tpr_scores = []
        
        for group in groups:
            group_data = data[data[group_col] == group]
            
            if len(group_data) < 10:  # Skip small groups
                continue
            
            y_true = group_data[label_col]
            y_pred = group_data[prediction_col]
            
            # Calculate False Positive Rate
            tn = ((y_true == 0) & (y_pred == 0)).sum()
            fp = ((y_true == 0) & (y_pred == 1)).sum()
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            
            # Calculate True Positive Rate
            tp = ((y_true == 1) & (y_pred == 1)).sum()
            fn = ((y_true == 1) & (y_pred == 0)).sum()
            tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            fpr_scores.append(fpr)
            tpr_scores.append(tpr)
        
        # Calculate max disparity
        fpr_disparity = max(fpr_scores) - min(fpr_scores) if fpr_scores else 0
        tpr_disparity = max(tpr_scores) - min(tpr_scores) if tpr_scores else 0
        
        return max(fpr_disparity, tpr_disparity)
    
    def calculate_content_fairness(self,
                                   data: pd.DataFrame,
                                   prediction_col: str,
                                   label_col: str,
                                   content_col: str) -> float:
        """
        Calculate content fairness based on accuracy consistency across categories.
        
        Content Fairness = 1 - (max_accuracy - min_accuracy) / max_accuracy
        
        Args:
            data: DataFrame with predictions and labels
            prediction_col: Column name for predictions
            label_col: Column name for true labels
            content_col: Column name for content categories
        
        Returns:
            Content fairness score (0-1, higher is better)
        """
        categories = data[content_col].unique()
        
        if len(categories) < 2:
            return 1.0  # Perfect fairness if only one category
        
        accuracies = []
        
        for category in categories:
            cat_data = data[data[content_col] == category]
            
            if len(cat_data) < 10:  # Skip small categories
                continue
            
            y_true = cat_data[label_col]
            y_pred = cat_data[prediction_col]
            
            accuracy = accuracy_score(y_true, y_pred)
            accuracies.append(accuracy)
        
        if not accuracies:
            return 0.0
        
        max_acc = max(accuracies)
        min_acc = min(accuracies)
        
        # Avoid division by zero
        if max_acc == 0:
            return 0.0
        
        content_fairness = 1.0 - ((max_acc - min_acc) / max_acc)
        
        return max(0.0, content_fairness)
    
    def calculate_procedural_fairness(self,
                                     data: pd.DataFrame,
                                     explanation_col: Optional[str] = None,
                                     appeal_time_col: Optional[str] = None) -> float:
        """
        Calculate procedural fairness based on transparency and appeal mechanisms.
        
        Procedural Fairness = 0.5 * explanation_rate + 0.5 * appeal_score
        
        Args:
            data: DataFrame with procedural information
            explanation_col: Boolean column indicating explanation availability
            appeal_time_col: Column with appeal resolution time in hours
        
        Returns:
            Procedural fairness score (0-1, higher is better)
        """
        scores = []
        
        # Explanation availability rate
        if explanation_col and explanation_col in data.columns:
            explanation_rate = data[explanation_col].mean()
            scores.append(explanation_rate)
        
        # Appeal resolution time score
        if appeal_time_col and appeal_time_col in data.columns:
            # Target: 72 hours (3 days)
            # Score = 1 if <= 72h, decreases linearly to 0 at 168h (1 week)
            avg_appeal_time = data[appeal_time_col].mean()
            
            if avg_appeal_time <= 72:
                appeal_score = 1.0
            elif avg_appeal_time >= 168:
                appeal_score = 0.0
            else:
                appeal_score = 1.0 - ((avg_appeal_time - 72) / (168 - 72))
            
            scores.append(appeal_score)
        
        if not scores:
            return 0.0
        
        return np.mean(scores)
    
    def _interpret_score(self, score: float) -> str:
        """Provide interpretation of MDFI score."""
        if score >= 70:
            return "Acceptable fairness (meets threshold)"
        elif score >= 50:
            return "Moderate concerns (requires attention)"
        else:
            return "Urgent intervention needed"
    
    def generate_detailed_report(self,
                                data: pd.DataFrame,
                                **kwargs) -> Dict:
        """
        Generate comprehensive fairness report with detailed metrics.
        
        Returns:
            Dictionary with detailed fairness analysis
        """
        results = self.calculate_mdfi(data, **kwargs)
        
        # Add detailed breakdowns
        results['detailed_metrics'] = {
            'total_records': len(data),
            'baseline_accuracy': accuracy_score(
                data[kwargs.get('label_col', 'label')],
                data[kwargs.get('prediction_col', 'predicted')]
            ),
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        return results


# Example usage
if __name__ == "__main__":
    # Create sample data for demonstration
    np.random.seed(42)
    n_samples = 1000
    
    sample_data = pd.DataFrame({
        'predicted': np.random.randint(0, 2, n_samples),
        'label': np.random.randint(0, 2, n_samples),
        'age_group': np.random.choice(['young', 'elderly'], n_samples),
        'location': np.random.choice(['urban', 'rural'], n_samples),
        'content_category': np.random.choice(['health', 'entertainment', 'politics'], n_samples),
        'has_explanation': np.random.choice([True, False], n_samples, p=[0.85, 0.15]),
        'appeal_time_hours': np.random.normal(60, 20, n_samples)
    })
    
    # Calculate MDFI
    calculator = MDFICalculator()
    results = calculator.calculate_mdfi(
        data=sample_data,
        demographic_col='age_group',
        geographic_col='location',
        content_col='content_category',
        explanation_col='has_explanation',
        appeal_time_col='appeal_time_hours'
    )
    
    print("="*60)
    print("MDFI CALCULATION RESULTS")
    print("="*60)
    print(f"Overall MDFI Score: {results['overall_score']:.2f}/100")
    print(f"Interpretation: {results['interpretation']}")
    print(f"\nComponent Scores:")
    print(f"  Group Fairness: {results['group_fairness']:.4f}")
    print(f"  Content Fairness: {results['content_fairness']:.4f}")
    print(f"  Procedural Fairness: {results['procedural_fairness']:.4f}")
    print("="*60)
