# 🏨 Gezinomi Müşteri Segmentasyon Analizi
## Tatilci Rezervasyon Davranışlarının İstatistiksel Analizi

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)](https://pandas.pydata.org/)
[![İstatistiksel Analiz](https://img.shields.io/badge/İstatistiksel%20Analiz-İleri%20Düzey-orange.svg)]()
[![Scipy](https://img.shields.io/badge/Scipy-Stats-red.svg)]()

> **"Veri sadece sayı değildir. Doğru analizle, stratejiye dönüşen bir sezgidir."**

---

## 📊 Proje Genel Bakış

Bu proje, Gezinomi'nin **59.164 otel rezervasyon kaydını** analiz ederek tatilci davranış kalıplarını kapsamlı istatistiksel metodoloji ile anlamayı hedeflemektedir. Çalışma, farklı rezervasyon davranış segmentlerini ve bunların ekonomik etkilerini ortaya koymaktadır.

### 🎯 Temel Amaçlar
- `SaleCheckInDayDiff` kalıplarına dayalı müşteri segmentasyonu
- Kapsamlı istatistiksel test pipeline'ı uygulama
- Davranışsal segmentler arasında fiyat varyansı analizi
- Veriye dayalı stratejik öneriler geliştirme

---

## 🔍 Veri Seti Yapısı

**Veri Seti:** `miuul_gezinomi.csv` - 59.164 rezervasyon kaydı  
**Temel Değişkenler:**
- `SaleDate`: Rezervasyon tarihi (gg.aa.yyyy formatı)
- `CheckInDate`: Otel giriş tarihi (gg.aa.yyyy formatı)
- `Price`: Rezervasyon fiyatı (virgülle ayrılmış ondalık)
- `SaleCityName`: Varış şehri
- `ConceptName`: Otel konsepti/türü
- `Seasons`: Mevsimsel sınıflandırma (High/Low)
- `SaleCheckInDayDiff`: Rezervasyon ile giriş arası gün farkı (hedef değişken)

---

## 🎭 Müşteri Segmentasyon Sonuçları

### Tatilci Tipi Dağılımı
`SaleCheckInDayDiff` analizi ve özel segmentasyon fonksiyonu kullanılarak:

```python
def segment_tourist(diff):
    if diff <= 5:
        return "son dakikacı"           # Son dakika rezervasyoncuları
    elif diff <= 30:
        return "kısa vadeli planlayıcı" # Kısa vadeli planlayıcılar
    elif diff <= 150:
        return "orta vadeli planlayıcı" # Orta vadeli planlayıcılar
    elif diff <= 250:
        return "uzun vadeli stratejist"  # Uzun vadeli stratejistler
    else:
        return "çok uzun vadeli stratejist" # Ultra uzun vadeli stratejistler
```

| 🏷️ Segment | 📊 Yüzde | 🎯 Rezervasyon Penceresi | 💡 Temel İçgörü |
|------------|-----------|---------------------------|------------------|
| **Son Dakikacı** | %39.1 | 0-5 gün | Baskın spontane davranış |
| **Kısa Vadeli Planlayıcı** | %33.9 | 6-30 gün | Esnek planlama yaklaşımı |
| **Orta Vadeli Planlayıcı** | %21.4 | 31-150 gün | Dengeli planlama davranışı |
| **Uzun Vadeli Stratejist** | %5.3 | 151-250 gün | Stratejik önceden planlama |
| **Çok Uzun Vadeli Stratejist** | %0.3 | 250+ gün | Ultra muhafazakar planlama |

---

## 🔬 İstatistiksel Analiz Pipeline'ı

### 1. Veri Ön İşleme ve Dönüştürme
```python
# Sütun başlığı atama ve veri temizleme
df.columns = df.iloc[0]
df = df[1:].reset_index(drop=True)

# Fiyat dönüştürme (virgülden ondalığa)
df["Price"] = df["Price"].str.replace(",", ".").astype(float)

# Tarih ayrıştırma ve özellik mühendisliği
df['SaleDate'] = pd.to_datetime(df['SaleDate'], format='%d.%m.%Y')
df['CheckInDate'] = pd.to_datetime(df['CheckInDate'], format='%d.%m.%Y')
df["SaleCheckInDayDiff"] = pd.to_numeric(df["SaleCheckInDayDiff"], errors="coerce")
```

### 2. Normallik Testi - Kolmogorov-Smirnov Testi
```python
from scipy.stats import kstest, norm

for group in df["TouristType"].unique():
    data = df[df["TouristType"] == group]["Price"]
    stat, p = kstest(data, "norm", args=(data.mean(), data.std()))
    print(f"{group}: p-değeri = {p:.4f}")
```
**Sonuç:** Tüm segmentlerde p < 0.05 → **Normal dağılımdan sapma doğrulandı**

### 3. Görsel Normallik Değerlendirmesi
- Her segment için **KDE ile histogramlar**
- Teorik normal dağılıma karşı **Q-Q plotları**
- **Temel Bulgu:** Son dakikacı, kısa vadeli, orta vadeli segmentler normalliğe en yakın

### 4. Varyans Homojenliği - Levene Testi
```python
from scipy.stats import levene

groups = [df[df["TouristType"] == g]["Price"] for g in df["TouristType"].unique()]
stat, p = levene(*groups)
print(f"Levene Testi: p-değeri = {p:.4f}")
```
**Sonuç:** p < 0.05 → **Varyans heterojenliği doğrulandı**

### 5. Fiyat Varyans Analizi
| Segment | Fiyat Varyansı |
|---------|----------------|
| Orta vadeli planlayıcı | 2.992,35 |
| Son dakikacı | 2.857,44 |
| Kısa vadeli planlayıcı | 2.415,03 |
| Uzun vadeli stratejist | 1.073,17 |
| Çok uzun vadeli stratejist | 753,81 |

**Temel İçgörü:** Daha uzun planlama süresi, daha düşük fiyat varyansı ile korelasyon gösteriyor

### 6. Non-Parametrik Grup Karşılaştırması - Kruskal-Wallis Testi
```python
from scipy.stats import kruskal

stat, p = kruskal(*groups)
print(f"Kruskal-Wallis: p-değeri = {p:.4f}")
```
**Sonuç:** p < 0.0001 → **Segmentler arası anlamlı fiyat farkları**

### 7. Post-Hoc Analizi - Bonferroni Düzeltmeli Dunn Testi
```python
import scikit_posthocs as sp

dunn_results = sp.posthoc_dunn(groups, p_adjust="bonferroni")
```

**Kritik Bulgu:** Sadece **orta vadeli planlayıcı** vs **uzun vadeli stratejist** arasında anlamlı fark yok (p = 1.000)

---

## 📈 Temel Analitik İçgörüler

### Davranışsal Kalıplar
- **%60+ rezervasyon** aynı gün rezervasyonları (SaleCheckInDayDiff = 0)
- **Mevsimsel dinamikler:** Yüksek sezon geniş davranış aralığı vs Düşük sezon yoğunlaşma
- **Şehir tercihleri:** Antalya tüm segmentlerde baskın, ancak Aydın/Muğla orta vadeli planlayıcılar tarafından tercih ediliyor

### Ekonomik İçgörüler
- **Fiyat duyarlılığı** daha uzun planlama ufukları ile azalıyor
- **Varyans analizi** segment başına farklı risk profilleri ortaya koyuyor
- **"Herşey Dahil" konsepti** tüm segmentlerde baskın, ancak son dakikacılar alternatiflere daha açık

### İstatistiksel Doğrulama
- **Non-parametrik yaklaşım** normallik ihlalleri nedeniyle gerekçeli
- **Bonferroni düzeltmesi** güvenilir çoklu karşılaştırma sonuçları sağlıyor
- **Etki büyüklükleri** istatistiksel anlamlılığın ötesinde pratik önem gösteriyor

---

## 🎯 Stratejik Öneriler

### 🔥 Yüksek Sezon Stratejisi (Haziran-Ağustos)
- Uzun vadeli segmentler için **erken kampanya başlangıcı**
- **Premium paketler** ve sadakat programları vurgusu
- Esneklik yerine **değer odaklı fiyatlandırma**

### ❄️ Düşük Sezon Stratejisi (Kasım-Mart)
- Spontane rezervasyoncuları hedefleyen **son dakika flaş kampanyaları**
- Anında dönüşüm için **mobil bildirim sistemleri**
- **Esnek fiyat yapıları** ve sınırlı süreli teklifler

### 📊 Segment Özelinde Yaklaşımlar

| Segment | Strateji | Kanal Odağı | Fiyatlandırma Yaklaşımı |
|---------|----------|-------------|-------------------------|
| **Son Dakikacı** | Sınırlı süreli fırsatlar | Push bildirimleri | Dinamik/Flaş fiyatlandırma |
| **Kısa Vadeli** | Sosyal medya kampanyaları | Sosyal platformlar | Esnek fiyatlandırma |
| **Orta Vadeli** | Geniş ürün yelpazesi | Display reklamcılık | Standart fiyatlandırma |
| **Uzun Vadeli** | Sadakat programları | Email beslenme | Erken rezervasyon indirimleri |

---

## 🛠️ Teknik Implementasyon

### Bağımlılıklar
```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kstest, levene, kruskal
import scikit_posthocs as sp
import scipy.stats as stats
```

### Temel Analiz Fonksiyonları
- Güvenilir tip dönüştürmeleri ile **veri ön işleme pipeline'ı**
- Rezervasyon önceden süresine dayalı **özel segmentasyon mantığı**
- **Kapsamlı istatistiksel test** iş akışı
- **Gelişmiş görselleştirme paketi** (histogramlar, Q-Q plotları, boxplotlar, heatmap'ler)

### Görselleştirme Öne Çıkanları
- Segment dağılımı için **pasta grafikleri**
- Grid stillemeli **mevsimsel analiz plotları**
- **Varyans karşılaştırma** bar grafikleri
- P-değeri açıklamalı **Dunn test heatmap'i**
- **Çok boyutlu boxplotlar** (segment × sezon × fiyat)

---

## 📊 Sonuçlar ve İş Etkisi

### İstatistiksel Doğrulama
- Uygun varsayım testlemeli **güvenilir metodoloji**
- Normal olmayan veri için **non-parametrik yaklaşım**
- Güvenilir sonuçlar için **çoklu karşılaştırma düzeltmesi**
- Kapsamlı çizimlerle **görsel doğrulama**

### İş Zekası
- Rezervasyon davranışına dayalı **net segmentasyon sınırları**
- Risk yönetimi için **fiyat varyansı içgörüleri**
- Veri destekli **mevsimsel strateji farklılaşması**
- Tanımlanmış **kanal optimizasyon** fırsatları

### Stratejik Değer
- **%39.1 pazar** anında yanıt kabiliyeti gerektiriyor
- **%73 toplam** (son dakikacı + kısa vadeli) çevik pazarlama ihtiyacı
- **Varyans analizi** fiyatlandırma stratejisi risk değerlendirmesini bilgilendiriyor
- **Coğrafi içgörüler** bölgesel kampanya optimizasyonu sağlıyor

---

## 🚀 Gelecek Geliştirme Fırsatları

### Gelişmiş Analitikler
- Aylık rezervasyon kalıbı tahmini için **zaman serisi analizi**
- Rezervasyon olasılığı tahmini için **makine öğrenmesi modelleri**
- Segment bazında **müşteri yaşam değeri** analizi
- **Gerçek zamanlı segmentasyon** sistem geliştirme

### İş Uygulamaları
- Segment davranışına dayalı **dinamik fiyatlandırma motoru**
- Farklı tatilci tipleri için **otomatik kampanya tetikleyicileri**
- Rezervasyon kalıplarına uyumlu **envanter optimizasyonu**
- Segment başına **gelir yönetimi** stratejileri

---

## 👩‍💼 Yazar

**Aslı Torun**  
Veri Analisti & Stratejik İçgörü Uzmanı

*"Rezervasyon davranışlarını iş stratejilerine dönüştürmek - her veri noktasıyla birlikte."*

---

## 📄 Proje Dosyaları

- `gezinomi_analysis.py` - Komple analiz pipeline'ı
- `miuul_gezinomi.csv` - Kaynak veri seti (59.164 kayıt)
- İstatistiksel test çıktıları ve görselleştirme dışa aktarımları
- Stratejik öneri çerçevesi

---

## 🙏 Teşekkürler

- Kapsamlı rezervasyon veri seti için **Gezinomi**
- Veri bilimi metodoloji rehberliği için **Miuul**
- Güvenilir test yaklaşımları için **istatistiksel analiz topluluğu**

---

*Bu analiz, rezervasyon kalıplarının güvenilir istatistiksel metodoloji ile iş stratejilerine nasıl dönüştürüldüğünü göstermektedir.*