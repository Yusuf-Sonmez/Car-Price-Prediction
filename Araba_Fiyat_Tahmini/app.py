# app.py
import streamlit as st
import pandas as pd
import joblib

# Sayfa Tasarımı
st.set_page_config(page_title="AI Fiyat Tahmin Motoru", page_icon="🚗", layout="centered")
st.title("🚗 İkinci El Araç Fiyat Tahmin Motoru")
st.markdown("Yyapay zeka modelimizi kullanarak aracınızın piyasa değerini anlık olarak hesaplayın.")
st.write("---")

# Model Yükleme
@st.cache_resource
def load_production_model():
    return joblib.load("models/random_forest_model.pkl")

model = load_production_model()

st.subheader("📋 Araç Bilgilerini Giriniz")

col1, col2 = st.columns(2)

with col1:
    # Sayısal Girdiler
    kilometre = st.number_input("Kilometre", min_value=0, max_value=1000000, value=120000, step=5000)
    motor_hacmi = st.number_input("Motor Hacmi (cc)", min_value=600, max_value=7000, value=1600, step=100)
    motor_gucu = st.number_input("Motor Gücü (hp)", min_value=30, max_value=1000, value=110, step=5)
    yil = st.slider("Araç Model Yılı", min_value=1990, max_value=2026, value=2015)
    degisen = st.slider("Değişen Parça Sayısı", min_value=0, max_value=10, value=0)
    boyali = st.slider("Boyalı Parça Sayısı", min_value=0, max_value=12, value=0)

with col2:
    # Kategorik Girdiler (LabelEncoder sıralamana göre eşleştirildi)
    vites = st.selectbox("Vites Tipi", ["Düz (Manuel)", "Otomatik", "Yarı Otomatik"])
    vites_val = 0 if "Düz" in vites else (1 if "Otomatik" in vites else 2)
    
    yakit = st.selectbox("Yakıt Tipi", ["Benzin", "Dizel", "LPG & Benzin", "Hibrit", "Elektrik"])
    yakit_dict = {"Benzin": 0, "Dizel": 1, "LPG & Benzin": 2, "Hibrit": 3, "Elektrik": 4}
    yakit_val = yakit_dict.get(yakit, 0)
    
    kimden = st.selectbox("Kimden", ["Galeriden", "Sahibinden", "Yetkili Bayiden", "Rent a Car"])
    kimden_dict = {"Galeriden": 0, "Sahibinden": 1, "Yetkili Bayiden": 2, "Rent a Car": 3}
    kimden_val = kimden_dict.get(kimden, 0)
    
    kasa = st.selectbox("Kasa Tipi", ["Sedan", "Hatchback/5", "SUV", "Diğer"])
    kasa_val = 0 # Modelin train yapısına göre varsayılan ağırlık

st.write("---")

if st.button("💰 Aracın Değerini Hesapla", use_container_width=True):
    # 1. Ham veri sözlüğünü oluşturuyoruz (Sıralama fark etmez)
    input_dict = {
        "marka": 500000.0,
        "seri": 450000.0,
        "model": 400000.0,
        "yil": float(yil),
        "kilometre": float(kilometre),
        "vites_tipi": int(vites_val),
        "yakit_tipi": int(yakit_val),
        "kasa_tipi": int(kasa_val),
        "renk": 350000.0,
        "motor_hacmi": float(motor_hacmi),
        "motor_gucu": float(motor_gucu),
        "degisen_sayisi": float(degisen),
        "boyali_sayisi": float(boyali),
        "degisen_sayisi_missing": 0,
        "boyali_sayisi_missing": 0,
        "kimden": int(kimden_val)
    }
    
    # 2. DataFrame haline getiriyoruz
    input_df = pd.DataFrame([input_dict])
    
    try:
        # --- SİHRİ YAPTIĞIMIZ YER ---
        # Modelin eğitilirken hafızasına kazıdığı tam sütun sırasını alıyoruz:
        model_sutun_sirasi = model.feature_names_in_
        
        # DataFrame'imizi modelin tam olarak beklediği sıraya göre yeniden diziyoruz!
        input_df = input_df[model_sutun_sirasi]
        
        # 3. Artık sıra milimetrik olarak doğru, tahmini yapabiliriz
        prediction = model.predict(input_df)[0]
        
        st.success(f"### 🎯 Tahmin Edilen Piyasa Değeri: **{prediction:,.2f} TL**")
        #st.balloons()
        with st.spinner("Piyasa analizi yapılıyor..."):
            prediction = model.predict(input_df)[0]
    except Exception as e:
        st.error(f"Tahmin uyuşmazlığı oluştu, sütunları kontrol et: {e}")