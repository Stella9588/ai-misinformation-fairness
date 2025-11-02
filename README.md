# AI Misinformation Detection Fairness Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Ensuring Fairness in AI-based Misinformation Detection: Toward a Governance Toolkit for Sustainable Digital Information Systems**

A comprehensive framework and toolkit for measuring and improving fairness in AI-driven misinformation detection systems, with empirical validation on Chinese and Vietnamese platforms.

## 📋 Overview

This repository contains the complete implementation of the **Multi-Dimensional Fairness Index (MDFI)** framework, developed as part of a Master's thesis at Zhejiang University. The framework addresses systematic fairness failures in misinformation detection systems that disproportionately impact:

- 👴 **Elderly users** (12% higher false positive rate)
- 🏘️ **Rural populations** (8% lower detection protection)  
- 🏥 **Health content** (17% accuracy gap vs. entertainment)

## 🎯 Key Features

- **Multi-Dimensional Fairness Index (MDFI)**: Composite metric combining group fairness (40%), content fairness (30%), and procedural fairness (30%)
- **Platform Benchmarking**: Comparative analysis across Weibo, Tencent News, Zalo, VnExpress, and more
- **Governance Toolkit**: Audit frameworks, SLA thresholds, transparency templates
- **Visualization Suite**: Professional charts for fairness metrics
- **Cross-National Analysis**: China-Vietnam comparative framework

## 📊 Key Results

| Platform | MDFI Score | Coverage |
|----------|------------|----------|
| Weibo | 68.04/100 | 38.07% |
| mygopen | 59.49/100 | 11.35% |
| Taiwan FactCheck | 58.75/100 | 9.03% |
| **Overall** | **60.13/100** | **100%** |

**Recommended Threshold:** 70/100 (based on EU, OECD, Chinese regulatory frameworks)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-misinformation-fairness.git
cd ai-misinformation-fairness

# Install dependencies
pip install -r requirements.txt

# Run quick example
python examples/quickstart.py
```

## 📁 Repository Structure

```
ai-misinformation-fairness/
├── paper/                          # Research paper and supplementary materials
│   ├── AI_Misinformation_Fairness_FINAL.pdf
│   └── figures/                    # All charts and visualizations
├── data/                           # Datasets and samples
│   ├── sample_mcfend.csv          # Sample MCFEND data
│   ├── platform_metadata.json     # Platform information
│   └── DATA_README.md             # Data documentation
├── toolkit/                        # Core MDFI implementation
│   ├── mdfi_calculator.py         # MDFI score computation
│   ├── fairness_audit.py          # Audit framework
│   ├── data_preprocessing.py      # Data cleaning utilities
│   └── visualization.py           # Chart generation
├── docs/                           # Documentation
│   ├── USAGE_GUIDE.md             # Detailed usage instructions
│   ├── METHODOLOGY.md             # Technical methodology
│   └── API_REFERENCE.md           # API documentation
├── examples/                       # Example scripts
│   ├── quickstart.py              # Basic usage example
│   ├── platform_comparison.py     # Multi-platform analysis
│   └── generate_report.py         # Generate audit report
├── requirements.txt                # Python dependencies
├── LICENSE                         # MIT License
└── README.md                       # This file
```

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from source

```bash
git clone https://github.com/yourusername/ai-misinformation-fairness.git
cd ai-misinformation-fairness
pip install -r requirements.txt
```

### Install as package (optional)

```bash
pip install -e .
```

## 📖 Usage Examples

### 1. Calculate MDFI Score

```python
from toolkit.mdfi_calculator import MDFICalculator
import pandas as pd

# Load your data
data = pd.read_csv('data/sample_mcfend.csv')

# Initialize calculator
calculator = MDFICalculator()

# Calculate scores
results = calculator.calculate_mdfi(
    data=data,
    demographic_col='user_age_group',
    geographic_col='user_location',
    content_col='content_category',
    label_col='is_fake'
)

print(f"Overall MDFI Score: {results['overall_score']:.2f}/100")
print(f"Group Fairness: {results['group_fairness']:.2f}")
print(f"Content Fairness: {results['content_fairness']:.2f}")
print(f"Procedural Fairness: {results['procedural_fairness']:.2f}")
```

### 2. Run Fairness Audit

```python
from toolkit.fairness_audit import FairnessAuditor

auditor = FairnessAuditor()
audit_report = auditor.generate_audit(
    data=data,
    output_path='audit_report.pdf'
)

print(f"Audit complete! Report saved to {audit_report}")
```

### 3. Visualize Results

```python
from toolkit.visualization import FairnessVisualizer

visualizer = FairnessVisualizer()

# Generate all charts
visualizer.create_platform_comparison_chart(results, 'platform_scores.png')
visualizer.create_fairness_gaps_chart(results, 'fairness_gaps.png')
visualizer.create_mdfi_breakdown_chart(results, 'mdfi_breakdown.png')
```

## 📊 Datasets

### MCFEND (Multi-platform Chinese Fake News Dataset)

- **Total Records:** 23,974
- **Clean Labeled Data:** 14,473
  - False News: 13,039 (90.1%)
  - Authentic News: 1,434 (9.9%)
- **Platforms:** 10 major Chinese fact-checking sources
- **Time Period:** 2019-2024

### Additional Datasets

- **WELFake:** ~233,659 records
- **Social Context:** ~480,749 records
- **Total Combined:** 738,382 records

**Note:** Full datasets are not included in this repository due to size. Sample data is provided. Contact authors for access to complete datasets.

## 🔧 API Reference

### MDFICalculator

Main class for calculating Multi-Dimensional Fairness Index scores.

**Methods:**
- `calculate_mdfi(data, **kwargs)`: Compute complete MDFI score
- `calculate_group_fairness(data, demographic_col, label_col)`: Group fairness component
- `calculate_content_fairness(data, content_col, label_col)`: Content fairness component
- `calculate_procedural_fairness(data)`: Procedural fairness component

See [API_REFERENCE.md](docs/API_REFERENCE.md) for complete documentation.

## 📈 Governance Toolkit

The toolkit includes practical templates for platform operators and regulators:

### Audit Framework
- Standardized audit forms
- Demographic fairness assessment protocols
- Content category analysis procedures
- Temporal fairness tracking

### SLA Thresholds
| Metric | Minimum Threshold |
|--------|------------------|
| Demographic FPR Disparity | ≤ 15% |
| Geographic Detection Gap | ≤ 10% |
| Content Category Accuracy Range | ≤ 20% |
| Explanation Availability Rate | ≥ 90% |
| Appeal Resolution Time | ≤ 72 hours |
| Overall MDFI Score | ≥ 70/100 |

### Transparency Reporting
- Quarterly fairness report templates
- Incident documentation guidelines
- Improvement initiative tracking

### Appeal Mechanisms
- User appeal submission procedures
- Human review protocols
- Resolution communication templates

## 🌏 Cross-National Comparison

The framework includes comparative analysis between Chinese and Vietnamese platforms:

### Chinese Platforms
- **Regulatory Approach:** Platform responsibility with state oversight
- **Key Platforms:** Weibo, WeChat, Tencent News
- **Fairness Priority:** Demographic equity (elderly, rural populations)

### Vietnamese Platforms
- **Regulatory Approach:** Self-regulation with government guidelines
- **Key Platforms:** Zalo, VnExpress, Zing News
- **Fairness Priority:** Social harmony and ethnic/religious balance

See [paper/](paper/) for detailed comparative analysis.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute
- Report bugs and issues
- Suggest new features or improvements
- Improve documentation
- Add support for new platforms
- Share your fairness audit results

## 📄 Citation

If you use this framework in your research, please cite:

```bibtex
@mastersthesis{misinformation_fairness_2024,
  author = {Your Name},
  title = {Ensuring Fairness in AI-based Misinformation Detection: 
           Toward a Governance Toolkit for Sustainable Digital Information Systems},
  school = {Zhejiang University},
  year = {2024},
  type = {Master's thesis}
}
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Author Name** - Zhejiang University, School of Public Administration
- **Supervisor:** Prof. Wuchao

## 🙏 Acknowledgments

- Zhejiang University School of Public Administration
- MCFEND dataset contributors
- Chinese and Vietnamese platform research participants
- Open source community

## 📧 Contact

- **Email:** your.email@example.com
- **Issues:** [GitHub Issues](https://github.com/yourusername/ai-misinformation-fairness/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/ai-misinformation-fairness/discussions)

## 🔗 Related Resources

- [Research Paper (Full Text)](paper/AI_Misinformation_Fairness_FINAL.pdf)
- [Usage Guide](docs/USAGE_GUIDE.md)
- [Methodology Documentation](docs/METHODOLOGY.md)
- [Example Scripts](examples/)

---

**⚠️ Disclaimer:** This framework is provided for research and educational purposes. Users should ensure compliance with local regulations and platform terms of service when conducting fairness audits.
