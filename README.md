# 🏨 Gezinomi Customer Segmentation Analysis
## Statistical Analysis of Tourist Booking Behaviors

> **"Veri sadece sayı değildir. Doğru analizle, stratejiye dönüşen bir sezgidir."**

---

## 📊 Project Overview

This project analyzes **59,164 hotel booking records** from Gezinomi to understand tourist behavior patterns through comprehensive statistical analysis. The study reveals distinct booking behavior segments and their economic implications using rigorous statistical methodology.

### 🎯 Key Objectives
- Segment customers based on `SaleCheckInDayDiff` patterns
- Apply comprehensive statistical testing pipeline
- Analyze price variance across behavioral segments
- Generate data-driven strategic recommendations

---

## 🔍 Dataset Structure

**Dataset:** `miuul_gezinomi.csv` - 59,164 booking records  
**Key Variables:**
- `SaleDate`: Reservation date (dd.mm.yyyy format)
- `CheckInDate`: Hotel check-in date (dd.mm.yyyy format)
- `Price`: Booking price (comma-separated decimals)
- `SaleCityName`: Destination city
- `ConceptName`: Hotel concept/type
- `Seasons`: Seasonal classification (High/Low)
- `SaleCheckInDayDiff`: Days between booking and check-in (target variable)

---

## 🎭 Customer Segmentation Results

### Tourist Type Distribution
Based on `SaleCheckInDayDiff` analysis with custom segmentation function:

```python
def segment_tourist(diff):
    if diff <= 5:
        return "son dakikacı"           # Last-minute bookers
    elif diff <= 30:
        return "kısa vadeli planlayıcı" # Short-term planners
    elif diff <= 150:
        return "orta vadeli planlayıcı" # Medium-term planners
    elif diff <= 250:
        return "uzun vadeli stratejist"  # Long-term strategists
    else:
        return "çok uzun vadeli stratejist" # Ultra long-term strategists
```

| 🏷️ Segment | 📊 Percentage | 🎯 Booking Window | 💡 Key Insight |
|------------|---------------|-------------------|-----------------|
| **Son Dakikacı** | 39.1% | 0-5 days | Dominant spontaneous behavior |
| **Kısa Vadeli Planlayıcı** | 33.9% | 6-30 days | Flexible planning approach |
| **Orta Vadeli Planlayıcı** | 21.4% | 31-150 days | Balanced planning behavior |
| **Uzun Vadeli Stratejist** | 5.3% | 151-250 days | Strategic advance planning |
| **Çok Uzun Vadeli Stratejist** | 0.3% | 250+ days | Ultra-conservative planning |

---

## 🔬 Statistical Analysis Pipeline

### 1. Data Preprocessing & Transformation
```python
# Column header assignment and data cleaning
df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)

# Price conversion (comma to decimal)
df["Price"] = df["Price"].str.replace(",", ".").astype(float)

# Date parsing and feature engineering
df['SaleDate'] = pd.to_datetime(df['SaleDate'], format='%d.%m.%Y')
df['CheckInDate'] = pd.to_datetime(df['CheckInDate'], format='%d.%m.%Y')
df["SaleCheckInDayDiff"] = pd.to_numeric(df["SaleCheckInDayDiff"], errors="coerce")
```

### 2. Normality Testing - Kolmogorov-Smirnov Test
```python
from scipy.stats import kstest, norm

for group in df["TouristType"].unique():
    data = df[df["TouristType"] == group]["Price"]
    stat, p = kstest(data, "norm", args=(data.mean(), data.std()))
    print(f"{group}: p-değeri = {p:.4f}")
```
**Result:** All segments showed p < 0.05 → **Non-normal distribution confirmed**

### 3. Visual Normality Assessment
- **Histograms with KDE** for each segment
- **Q-Q plots** against theoretical normal distribution
- **Key Finding:** Son dakikacı, kısa vadeli, orta vadeli segments closest to normality

### 4. Variance Homogeneity - Levene Test
```python
from scipy.stats import levene

groups = [df[df["TouristType"] == g]["Price"] for g in df["TouristType"].unique()]
stat, p = levene(*groups)
print(f"Levene Testi: p-değeri = {p:.4f}")
```
**Result:** p < 0.05 → **Variance heterogeneity confirmed**

### 5. Price Variance Analysis
| Segment | Price Variance |
|---------|----------------|
| Orta vadeli planlayıcı | 2,992.35 |
| Son dakikacı | 2,857.44 |
| Kısa vadeli planlayıcı | 2,415.03 |
| Uzun vadeli stratejist | 1,073.17 |
| Çok uzun vadeli stratejist | 753.81 |

**Key Insight:** Higher planning lead time correlates with lower price variance

### 6. Non-Parametric Group Comparison - Kruskal-Wallis Test
```python
from scipy.stats import kruskal

stat, p = kruskal(*groups)
print(f"Kruskal-Wallis: p-değeri = {p:.4f}")
```
**Result:** p < 0.0001 → **Significant price differences between segments**

### 7. Post-Hoc Analysis - Dunn Test with Bonferroni Correction
```python
import scikit_posthocs as sp

dunn_results = sp.posthoc_dunn(groups, p_adjust="bonferroni")
```

**Critical Finding:** Only **orta vadeli planlayıcı** vs **uzun vadeli stratejist** showed no significant difference (p = 1.000)

---

## 📈 Key Analytical Insights

### Behavioral Patterns
- **60%+ bookings** are same-day reservations (SaleCheckInDayDiff = 0)
- **Seasonal dynamics:** High season shows wider behavioral range vs. Low season concentration
- **City preferences:** Antalya dominant across all segments, but Aydın/Muğla preferred by medium-term planners

### Economic Insights
- **Price sensitivity decreases** with longer planning horizons
- **Variance analysis** reveals distinct risk profiles per segment
- **"Herşey Dahil" concept** dominant across all segments, but last-minute bookers more open to alternatives

### Statistical Validation
- **Non-parametric approach** justified due to normality violations
- **Bonferroni correction** ensures robust multiple comparison results
- **Effect sizes** demonstrate practical significance beyond statistical significance

---

## 🎯 Strategic Recommendations

### 🔥 High Season Strategy (Haziran-Ağustos)
- **Early campaign initiation** for long-term segments
- **Premium packages** and loyalty programs emphasis
- **Value-based pricing** over flexibility

### ❄️ Low Season Strategy (Kasım-Mart)
- **Last-minute flash campaigns** targeting spontaneous bookers
- **Mobile notification systems** for immediate conversions
- **Flexible pricing structures** and limited-time offers

### 📊 Segment-Specific Approaches

| Segment | Strategy | Channel Focus | Pricing Approach |
|---------|----------|---------------|------------------|
| **Son Dakikacı** | Sınırlı süreli fırsatlar | Push notifications | Dynamic/Flash pricing |
| **Kısa Vadeli** | Sosyal medya kampanyaları | Social platforms | Flexible pricing |
| **Orta Vadeli** | Geniş ürün yelpazesi | Display advertising | Standard pricing |
| **Uzun Vadeli** | Sadakat programları | Email nurturing | Early bird discounts |

---

## 🛠️ Technical Implementation

### Dependencies
```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kstest, levene, kruskal
import scikit_posthocs as sp
import scipy.stats as stats
```

### Core Analysis Functions
- **Data preprocessing pipeline** with robust type conversions
- **Custom segmentation logic** based on booking lead time
- **Comprehensive statistical testing** workflow
- **Advanced visualization suite** (histograms, Q-Q plots, boxplots, heatmaps)

### Visualization Highlights
- **Pie charts** for segment distribution
- **Seasonal analysis plots** with grid styling
- **Variance comparison** bar charts
- **Dunn test heatmap** with p-value annotations
- **Multi-dimensional boxplots** (segment × season × price)

---

## 📊 Results & Business Impact

### Statistical Validation
- **Robust methodology** with proper assumption testing
- **Non-parametric approach** for non-normal data
- **Multiple comparison correction** for reliable results
- **Visual validation** through comprehensive plotting

### Business Intelligence
- **Clear segmentation boundaries** based on booking behavior
- **Price variance insights** for risk management
- **Seasonal strategy differentiation** supported by data
- **Channel optimization** opportunities identified

### Strategic Value
- **39.1% market** requires immediate-response capabilities
- **73% combined** (son dakikacı + kısa vadeli) need agile marketing
- **Variance analysis** informs pricing strategy risk assessment
- **Geographic insights** enable regional campaign optimization

---

## 🚀 Future Enhancement Opportunities

### Advanced Analytics
- **Time series analysis** for monthly booking pattern forecasting
- **Machine learning models** for booking probability prediction
- **Customer lifetime value** analysis by segment
- **Real-time segmentation** system development

### Business Applications
- **Dynamic pricing engine** based on segment behavior
- **Automated campaign triggers** for different tourist types
- **Inventory optimization** aligned with booking patterns
- **Revenue management** strategies per segment

---

## 👩‍💼 Author

**Aslı Torun**  
Data Scientist & Strategic Insights Specialist

*"Rezervasyon davranışlarını iş stratejilerine dönüştürmek - her veri noktasıyla birlikte."*

---

## 📄 Project Files

- `gezinomi_analysis.py` - Complete analysis pipeline
- `miuul_gezinomi.csv` - Source dataset (59,164 records)
- Statistical test outputs and visualization exports
- Strategic recommendation framework

---

## 🙏 Acknowledgments

- **Gezinomi** for comprehensive booking dataset
- **Miuul** for data science methodology guidance
- **Statistical analysis community** for robust testing approaches

---

*This analysis demonstrates how booking patterns transform into business strategies through rigorous statistical methodology.*
