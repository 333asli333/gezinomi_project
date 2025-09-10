
#* GEZİNOMİ PROJESİ

import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 
pd.set_option("display.max_columns", None)
df = pd.read_csv(r"C:\Users\TORUN\OneDrive\Desktop\gezinomi_tanıtım\miuul_gezinomi.csv", sep=";", header=None)

#* VERİ ÖN İŞLEME VE DÖNÜŞTÜRME

df.head()
df.tail()
df.info()
df.describe()
df.columns = df.iloc[0] # ilk satırı kolon ismi yaptım
df = df[1:].reset_index(drop=True)
df["Price"] = df["Price"].str.replace(",", ".").astype(float)
df['SaleDate'] = pd.to_datetime(df['SaleDate'], format='%d.%m.%Y')
df['CheckInDate'] = pd.to_datetime(df['CheckInDate'], format='%d.%m.%Y')
df["SaleCheckInDayDiff"] = pd.to_numeric(df["SaleCheckInDayDiff"], errors="coerce")
df = df.dropna(subset=["SaleCheckInDayDiff"])
df["SaleCheckInDayDiff"] = df["SaleCheckInDayDiff"].astype(int)
df["ConceptName"] = df["ConceptName"].astype("category")
df["SaleCityName"] = df["SaleCityName"].astype("category")
df["CInDay"] = df["CInDay"].astype("category")
df["Seasons"] = df["Seasons"].astype("category")
df['Seasons'].value_counts(normalize=True)
df.isna().sum()
df["Price"] = df["Price"].fillna(df["Price"].mean())


#* VERİ GÖRSELLEŞTİRME

sns.histplot(df["SaleCheckInDayDiff"], bins=50, kde=True)
plt.title("Rezervasyon Günü Farkı")
plt.xlabel("Satış ile Giriş Arasındaki Gün Farkı")
plt.ylabel("Frekans")
plt.show()

sns.boxplot(x="Seasons", y="SaleCheckInDayDiff", data=df )
plt.title("Sezonlara Göre Rezervasyon Süresi")
plt.xlabel("sezon")
plt.ylabel("gün farkı")
plt.show()

df.groupby("Seasons")["SaleCheckInDayDiff"].mean()

# Rezervasyon süresi dağılımı pozitif çarpık. 0. gün rezervasyonlar %60’den fazla.
# Sezon bazlı boxplot analizinde 
# ‘High’ sezonda geniş bir davranış aralığı varken, ‘Low’ sezonda kararlar sıkışık.
# Uç değerler özellikle yüksek sezonda anlamlı davranışsal segmentleri temsil ediyor.


def segment_tourist(diff):
    if diff <= 5:
        return "son dakikacı"
    elif diff <= 30:
        return "kısa vadeli planlayıcı"
    elif diff <= 150:
        return "orta vadeli planlayıcı"
    elif diff <= 250:
        return "uzun vadeli stratejist"
    else:
        return "çok uzun vadeli stratejist"

# Turist tiplerinini segmente ettim. 

df["TouristType"] = df["SaleCheckInDayDiff"].apply(segment_tourist)


# PİE Chart segmente edilen turist tiplerinin dağılımı 
df["TouristType"].value_counts().plot.pie(autopct = "%1.1f%%", figsize = (6,6),
                                          colors= sns.color_palette("pastel"))
plt.title("tatilci tipleri dağılımı")
plt.ylabel("")
plt.show()


sns.set_style("whitegrid") 
palette = sns.color_palette("Blues", n_colors=df["Seasons"].nunique())
sns.countplot(x="TouristType", hue="Seasons", data=df, palette=palette)
plt.title("Sezonlara Göre Tatilci Tipleri", fontsize=14, fontweight="bold")
plt.xlabel("Tatilci Tipi", fontsize=12)
plt.ylabel("Kişi Sayısı", fontsize=12)
plt.xticks(rotation=15)
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig("sezon_tatilci_tipleri.png", dpi=300, bbox_inches="tight")  # Canva için kaydetme
plt.show()




# Segmentasyonun sezonlara göre dağılımı, müşteri davranışının mevsimsel olarak nasıl değiştiğini gösteriyor. 
# High sezonda planlama süresi genişken, Low sezonda kararlar sıkışık. 
# Bu fark, kampanya stratejisi ve müşteri segmentasyonu açısından kritik.

df.groupby("TouristType")["Price"].mean().sort_values()

# Tatilci tipine göre ortalama fiyatlar farklılık gösteriyor. Çok uzun vadeli stratejistler daha
# uygun tatilleri tercih ederken uzun ve orta  vadeli stratejistler 64 bandına çıkmakta

sns.boxplot(x = "TouristType", y = "Price", hue = "Seasons", data = df)


df.groupby("TouristType")["SaleCityName"].value_counts(normalize=True).unstack().fillna(0)

# Antalya tüm tatilci tiplerinde baskın şehir. 
# Ancak Aydın ve Muğla gibi şehirler orta vadeli planlayıcılar tarafından tercih ediliyor.
# Bu, bölgesel kampanya stratejileri için önemli bir içgörü.


df.groupby("TouristType")["ConceptName"].value_counts(normalize=True).unstack().fillna(0)

# Herşey Dahil konsepti tüm tatilci tiplerinde baskın.
# Ancak son dakikacılar diğer konseptlere daha açık. 
# Bu, ürün çeşitliliği ve fiyat esnekliği açısından önemli.


#* NORMALLİK TESTİ

from scipy.stats import kstest
from scipy.stats import norm

#*K-S TESTİ

for group in df["TouristType"].unique():
    data = df[df["TouristType"] == group]["Price"]
    stat, p = kstest(data ,"norm",args = (data.mean(), data.std()))
    print(f"{group}: p-değeri = {p:.4f}")

# p değeri < 0.05 çıkması istatistiksel olarak normal dağılıma uymadığını gösterir.

#* Histogram Grafiği
import seaborn as sns 
import matplotlib.pyplot as plt 

for group in df["TouristType"].unique():
    plt.figure(figsize=(6,4))
    sns.histplot(df[df["TouristType"] == group]["Price"], bins=50, kde=True, color="pink")
    plt.title(f"Fiyat dağılımı - {group}")
    plt.xlabel("Fiyat")
    plt.ylabel("Frekans")
    plt.show()


#* Q-Q PLOT 
import scipy.stats as stats
import matplotlib.pyplot as plt

for group in df["TouristType"].unique():
    plt.figure(figsize=(6,5))
    stats.probplot(df[df["TouristType"] == group]["Price"], dist = "norm", plot = plt)
    plt.title(f"Q-Q Plot - {group}", fontsize = 14, fontweight = "bold")
    plt.xlabel("Teorik Kuantiller", fontsize = 12)
    plt.ylabel("Gözlenen Kuantiller", fontsize = 12)
    plt.grid(True, linestyle = "--", alpha = 0.5)
    plt.tight_layout()
    plt.show()

# Q–Q plot ile her segmentin fiyat dağılımını görsel olarak test ettim. 
# Son dakikacı, kısa vadeli, orta vadeli planlayıcılar normal dağılıma en yakınken,
# Uzun ve çok uzun vadeli gruplarda uçlarda sapmalar var. 
# Görseller, parametrik test varsayımlarının ihlalini sezgisel olarak da doğruluyor.

#* VARYANS HOMOJENLİĞİ TESTİ

from scipy.stats import levene 

groups = [df[df["TouristType"] == g]["Price"] for g in df["TouristType"].unique()]
stat, p = levene(*groups)
print(f"Levene Testi: p-değeri = {p: .4f}")


# grafik
sns.set(style="whitegrid")  # açık gri arka plan
plt.figure(figsize=(10,6))
palette = sns.color_palette("Blues", n_colors=df["TouristType"].nunique())
sns.boxplot(x="TouristType", y="Price", data=df, palette=palette)

# Başlık ve eksenler
plt.title("Turist Tiplerine Göre Fiyat Varyansı", fontsize=14, fontweight="bold")
plt.xlabel("Turist Tipi", fontsize=12)
plt.ylabel("Fiyat", fontsize=12)

# Grid ve düzen
plt.grid(True, linestyle="--", alpha=0.3)
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()

df.groupby("TouristType")["Price"].var().sort_values(ascending=False)

varyanslar = {
    "orta vadeli planlayıcı": 2992.35,
    "son dakikacı": 2857.44,
    "kısa vadeli planlayıcı": 2415.03,
    "uzun vadeli stratejist": 1073.17,
    "çok uzun vadeli stratejist": 753.81
}
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
colors = sns.color_palette("Blues", n_colors= len(varyanslar))
plt.bar(varyanslar.keys(), varyanslar.values(), color = colors)
plt.title("Turist Tiplerine Göre Fiyat Varyansı", fontsize=14, fontweight="bold")
plt.xlabel("Turist Tipi", fontsize=12)
plt.ylabel("Fiyat Varyansı", fontsize=12)
plt.xticks(rotation=15)
plt.grid(True, linestyle = "--", alpha = 0.3)
plt.tight_layout()
plt.show()


# En yüksek varyans orta vadeli planlayıcılarda gözlemlenirken, 
# çok uzun vadeli stratejistler en düşük varyansa sahiptir.
# Bu durum, müşteri gruplarının fiyat duyarlılığı ve 
# karar alma esnekliği açısından farklılaştığını göstermektedir.


#* KRUSKAL WALLİS TESTİ

from scipy.stats import kruskal
groups = [df[df["TouristType"] == g]["Price"] for g in df["TouristType"].unique()]
stat, p = kruskal(*groups)
print(f"Kruskal - Wallis: p-değeri = {p:.4f}")

# Kruskal-Wallis testi ile tatilci tipleri arasında 
# fiyat farkının istatistiksel olarak anlamlı olduğunu tespit ettim (p < 0.0001). 
# Bu, segmentasyonun sadece davranışsal değil, 
# aynı zamanda ekonomik olarak da farklılaştığını gösteriyor.



#* DUNN TESTİ

# Kruskal-Wallis sonrası segmentler arası fiyat farkının hangi çiftler arasında anlamlı olduğunu belirlemek amacıyla Dunn post-hoc testi uyguladım.
# Kruskal-Wallis testi, genel olarak gruplar arasında fark olup olmadığını gösterir.
# ancak bu farkın hangi gruplar arasında gerçekleştiğini belirtmez.
# Parametrik varsayımlar (normal dağılım ve varyans homojenliği) ihlal edildiği için,
# parametrik post-hoc testler (örneğin Tukey) yerine Dunn testi tercih edilmiştir.
# Bu test, çoklu karşılaştırmalarda güvenilir sonuç verir 
# Bonferroni düzeltmesiyle hata oranını kontrol eder. 

import scikit_posthocs as sp

groups = [df[df["TouristType"] == g]["Price"] for g in df["TouristType"].unique()]

dunn_results = sp.posthoc_dunn(groups, p_adjust="bonferroni")

dunn_results.index = df["TouristType"].unique()
dunn_results.columns = df["TouristType"].unique()
formatted_dunn = dunn_results.applymap(lambda x: f"{x:.4f}")
print(formatted_dunn)


# Dunn testi sonuçları, segmentler arasında genel olarak anlamlı farklılıklar
# olduğunu gösteriyor (p<0.05). Yalnızca orta vadeli planlayıcılar
# ile uzun vadeli stratejistler arasında fark çıkmamış (p=1.000). Bu da bize,
# bu iki grubun davranışlarının oldukça benzer olduğunu, 
# diğer segmentlerin ise birbirinden belirgin şekilde ayrıldığını gösteriyor.

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))
sns.heatmap(dunn_results, annot= formatted_dunn, fmt="", cmap="coolwarm", linewidths=0.5, linecolor="white")
plt.title("Segmentler Arası Dunn Testi p-değerleri", fontsize=14, fontweight="bold")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Bu tablo, segmentler arasında davranışsal ve ekonomik olarak net bir ayrışma olduğunu gösteriyor:
# kısa vadeli planlayıcılar ayrı bir grup oluştururken, 
# orta ve uzun vadeli stratejistler benzer davranışlar sergiliyor.

plt.figure(figsize=(10,6))
sns.boxplot(x="TouristType", y="Price", hue="Seasons", data=df, palette="Set2")
plt.title("Segment–Sezon–Fiyat Dağılımı", fontsize=14, fontweight="bold")
plt.xlabel("Turist Tipi")
plt.ylabel("Fiyat")
plt.legend(title="Sezon")
plt.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()


# Analiz edilen dört turist segmenti arasında fiyat beklentileri açısından belirgin farklılıklar 
# tespit edilmiştir. Kısa vadeli planlayıcılar 0-5000 TL arasında geniş bir fiyat 
# spektrumunda dağılım gösterirken,
# çok uzun vadeli stratejistler 0-500 TL gibi dar bir bantta yoğunlaşmaktadır.



