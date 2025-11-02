# MDFI Framework Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Detailed Usage](#detailed-usage)
4. [API Reference](#api-reference)
5. [Examples](#examples)

## Installation

```bash
git clone https://github.com/yourusername/ai-misinformation-fairness.git
cd ai-misinformation-fairness
pip install -r requirements.txt
```

## Quick Start

Run the quickstart example:

```bash
python examples/quickstart.py
```

This will:
- Generate sample data
- Calculate MDFI scores
- Create visualizations
- Provide recommendations

## Detailed Usage

### 1. Prepare Your Data

Your dataset should be a pandas DataFrame with:
- Prediction column (0/1)
- Label column (0/1) 
- Demographic information (optional)
- Geographic information (optional)
- Content categories (optional)
- Procedural metrics (optional)

### 2. Calculate MDFI

```python
from toolkit.mdfi_calculator import MDFICalculator
import pandas as pd

# Load data
data = pd.read_csv('your_data.csv')

# Initialize calculator
calculator = MDFICalculator()

# Calculate
results = calculator.calculate_mdfi(
    data=data,
    prediction_col='predicted',
    label_col='label',
    demographic_col='age_group',
    geographic_col='location',
    content_col='category'
)

print(f"MDFI Score: {results['overall_score']:.2f}/100")
```

### 3. Visualize Results

```python
from toolkit.visualization import FairnessVisualizer

visualizer = FairnessVisualizer()

# Create charts
visualizer.create_platform_comparison_chart(
    platform_scores,
    'output.png'
)
```

## For More Details

See full API reference in [API_REFERENCE.md](API_REFERENCE.md)
