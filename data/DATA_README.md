# Dataset Documentation

This directory contains sample data and metadata for the MDFI framework.

## 📊 Available Datasets

### 1. MCFEND (Multi-platform Chinese Fake News Dataset)

**Description:** Comprehensive Chinese misinformation dataset compiled from 10 major fact-checking platforms.

**Statistics:**
- **Total Records:** 23,974
- **Clean Labeled Data:** 14,473
  - False News (谣言): 13,039 (90.1%)
  - Authentic News (事实): 1,434 (9.9%)
- **Time Period:** January 2019 - August 2024
- **Languages:** Chinese (Simplified)

**Platform Distribution:**
| Platform | Records | Percentage |
|----------|---------|------------|
| Weibo (微博) | 9,128 | 38.07% |
| mygopen | 2,722 | 11.35% |
| Taiwan FactCheck Center | 2,166 | 9.03% |
| Tencent News (腾讯新闻较真平台) | 1,013 | 4.23% |
| Sina News (新浪) | 976 | 4.07% |
| Others | 9,969 | 41.65% |

**Data Fields:**
- `id`: Unique record identifier
- `title`: News headline/title
- `content`: Full article text (if available)
- `label`: Ground truth label (0=authentic, 1=fake)
- `platform`: Source platform
- `category`: Content category (health, politics, entertainment, etc.)
- `publish_date`: Original publication date
- `verified_date`: Fact-checking verification date
- `source_url`: Original article URL

### 2. WELFake Dataset

**Description:** Large-scale Western fake news dataset for cross-validation.

**Statistics:**
- **Records:** ~233,659
- **Languages:** English
- **Sources:** Multiple Western fact-checking organizations

### 3. Social Context Dataset

**Description:** Extended dataset with social media propagation patterns.

**Statistics:**
- **Records:** ~480,749
- **Features:** Social network metrics, propagation patterns, user behavior

### 4. Vietnamese Datasets (vfnd, ReINTEL)

**Description:** Vietnamese misinformation detection datasets for cross-national comparison.

**Platforms:** Zalo, VnExpress, Zing News

## 📁 Files in This Directory

### `sample_mcfend.csv`
Representative sample of 1,000 records from MCFEND dataset for testing and demonstration purposes.

**Columns:**
- `record_id`: Unique identifier
- `title`: News title
- `content_category`: health|politics|entertainment|economics|social
- `is_fake`: Binary label (1=fake, 0=authentic)
- `platform`: Source platform
- `user_age_group`: young|elderly (inferred or provided)
- `user_location`: urban|rural
- `has_explanation`: Boolean indicating if flagging explanation provided
- `appeal_time_hours`: Time to resolve appeal (if applicable)
- `predicted_label`: Model prediction
- `confidence_score`: Model confidence (0-1)

### `platform_metadata.json`
Metadata about platforms included in the study.

```json
{
  "weibo": {
    "name": "Weibo",
    "country": "China",
    "type": "social_media",
    "users": "500M",
    "url": "https://weibo.com"
  },
  ...
}
```

## 🔒 Data Access and Privacy

### Full Dataset Access

Due to file size and privacy considerations, the complete MCFEND dataset is not included in this repository. To access the full dataset:

1. **Academic/Research Use:**
   - Contact: [your.email@university.edu]
   - Provide: Research proposal and intended use
   - Sign: Data usage agreement

2. **Commercial Use:**
   - Contact: [licensing@institution.edu]
   - License fees may apply

### Data Privacy

All datasets have been:
- ✅ Anonymized (personal identifiers removed)
- ✅ Aggregated (where required by privacy regulations)
- ✅ Reviewed for compliance with GDPR, CCPA, and Chinese data protection laws
- ✅ Approved by institutional review board (IRB)

### Ethical Considerations

This research follows ethical guidelines for misinformation research:
- No amplification of false information
- Respect for user privacy
- Transparency about data sources
- Responsible disclosure of findings

## 📖 Data Usage Guidelines

### Citation

If you use these datasets in your research, please cite:

```bibtex
@mastersthesis{misinformation_fairness_2024,
  author = {Your Name},
  title = {Ensuring Fairness in AI-based Misinformation Detection},
  school = {Zhejiang University},
  year = {2024}
}
```

### Preprocessing

The sample data has been preprocessed as follows:

1. **Text Normalization:**
   - Lowercased
   - Special characters removed
   - Chinese text segmented using jieba

2. **Label Verification:**
   - Manual verification of 500 random samples
   - Inter-annotator agreement: κ = 0.87

3. **Quality Filters:**
   - Removed duplicates
   - Filtered out records with missing labels
   - Excluded spam and low-quality content

### Loading Data

```python
import pandas as pd

# Load sample data
data = pd.read_csv('data/sample_mcfend.csv')

# Basic statistics
print(f"Total records: {len(data)}")
print(f"Fake news: {(data['is_fake'] == 1).sum()}")
print(f"Authentic news: {(data['is_fake'] == 0).sum()}")
```

## 🔄 Data Updates

This dataset is periodically updated with new records:

- **Current Version:** v1.0 (2024-11)
- **Last Update:** November 2024
- **Next Planned Update:** Q1 2025

## 📞 Contact

For questions about the datasets:

- **General Inquiries:** your.email@university.edu
- **Technical Issues:** GitHub Issues
- **Data Access Requests:** data-requests@institution.edu

## 📄 License

The sample data in this repository is provided under the **CC BY-NC 4.0** license:
- ✅ Attribution required
- ✅ Non-commercial use allowed
- ✅ Adaptations allowed
- ❌ Commercial use prohibited without permission

For commercial licensing, contact: licensing@institution.edu
