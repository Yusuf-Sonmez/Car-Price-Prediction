# 🚗 İkinci El Araç Fiyat Tahmin Motoru & Streamlit Arayüzü

Bu proje, Türkiye ikinci el araç pazarından alınan yaklaşık 48.000 ilan verisi kullanılarak, yapay zeka tabanlı bir **End-to-End (Uçtan Uca) Fiyat Tahmin Modeli** ve bu modelin canlıda test edilebilmesini sağlayan **Streamlit Web Arayüzü** projesidir.

---

## 🚀 Proje Özet Adımları

### 1. Veri Temizleme & Gürültü Arındırma (Data Cleaning)
* Veri setinde yer alan, kullanıcı hatalarından kaynaklı ekstrem gürültüler (Örn: Sisteme yanlış girilen 22 Milyon km'lik araçlar veya piyasa normlarının çok üstündeki 595 Milyon TL'lik ilanlar) iş mantığına (**Business Logic**) göre filtrelenerek veri seti arındırılmıştır.
* Boş bırakılan ekspertiz verileri (`degisen_sayisi`, `boyali_sayisi`) doğrudan sıfırlanmak yerine, modele eksiklik bilgisini de bir ipucu olarak beslemek adına **Missing Value Indicator** sütunları türetilmiştir.

### 2. Güvenli Veri Ön İşleme & Sızıntı Engelleme (Feature Engineering & Data Leakage Control)
* **High Cardinality (Yüksek Kardinalite)** problemine sahip olan `marka`, `seri`, `model` ve `renk` gibi yüzlerce benzersiz kategori içeren sütunlar, boyutların lanetinden (**Curse of Dimensionality**) kaçınmak adına **Target Encoding** yöntemiyle sayısallaştırılmıştır.
* Ölümcül bir hata olan **Data Leakage (Veri Sızıntısı)** riskini engellemek için, Target Encoding haritalama işlemi veri seti `train_test_split` ile bölündükten **sonra** sadece eğitim kümesi üzerinden öğrenilmiş ve test kümesine güvenli bir şekilde haritalandırılmıştır.
* Düşük kategorili alanlar ise `LabelEncoder` mimarisiyle optimize edilmiştir.

### 3. Makine Öğrenmesi Modeli Eğitimi (Model Training)
* Doğrusal olmayan ilişkileri ve pazar dinamiklerini en iyi yakalayan algoritmalardan biri olan **Random Forest Regressor** seçilmiştir.
* Model, veri sızıntısından arındırılmış en dürüst ve gerçekçi haliyle **%88.31 Test $R^2$ Skoru** elde etmiştir. Bu skor, canlı pazar tahminleri için üretim standartlarının üzerindedir.

---

## 🛠️ Klasör Yapısı

```text
Araba_Fiyat_Tahmini/
│
├── models/
│   └── random_forest_model.pkl      # Diske kaydedilmiş şampiyon yapay zeka modeli
│
├── src/ (veya ana dizin)
│   └── app.py                       # Streamlit Web Arayüzü kaynak kodu
│
├── main.ipynb                       # Veri analizi, ön işleme ve model eğitim notebook'u
├── car_price_prediction.csv        # Ham veri seti (Gitignore ile korunmaktadır)
└── README.md                        # Proje dokümantasyonu
