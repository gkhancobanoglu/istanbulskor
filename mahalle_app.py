import streamlit as st
import pandas as pd
import osmnx as ox
import json
from geopy.geocoders import Nominatim
import time
from mahalle_yasam_degerlendirici import hesapla_yasam_skoru
from gelisim_analizi import gelisim_analizi

with open("istanbul_ilce_mahalleler.json", "r", encoding="utf-8") as f:
    ilce_mahalleler = json.load(f)

st.markdown("<h1 style='color:#56B4E9;'>🌉 İstanbul Mahalle Yaşam Skoru</h1>", unsafe_allow_html=True)

ilce = st.selectbox("📍 İlçenizi seçin:", list(ilce_mahalleler.keys()))
mahalle = st.selectbox("🏨 Mahalle seçin:", ilce_mahalleler[ilce])

st.markdown("### 🎯 Kriterlere verdiğiniz önemi puanlayın (1: En az, 5: En çok):")
priority_options = ["Park", "Okul", "Market", "Hastane", "Ulaşım"]
user_priorities = {}

cols = st.columns(len(priority_options))
for i, kriter in enumerate(priority_options):
    with cols[i]:
        user_priorities[kriter] = st.slider(kriter, 1, 5, 3)

if st.button("Yaşam Skorunu Hesapla"):
    st.info("⏳ Mahalle analiz ediliyor, lütfen bekleyin...")

    try:
        sonuc = hesapla_yasam_skoru(mahalle, ilce, user_priorities)

        lat, lon = sonuc["koordinat"]
        st.map(pd.DataFrame([[lat, lon]], columns=["lat", "lon"]))

        st.markdown("### 📊 Yaşam Skoru Detayları")
        st.dataframe(pd.DataFrame(sonuc["detaylar"]))

        st.success(f"🏁 Toplam Skor: {sonuc['toplam_skor']} / 500")

        st.markdown("### 🏩 15 Dakika Uyum Durumu")
        st.info(sonuc["uyum"])

        st.markdown("### 🧠 Stratejik Yatırım ve Gelişim Önerisi")
        sonuc_text = gelisim_analizi(
            mahalle,
            ilce,
            sonuc["detaylar"],
            sonuc["toplam_skor"],
            nufus_json_path="nufus_verisi.json"
        )

        if "✅" in sonuc_text and "<b>" not in sonuc_text:
            st.success(sonuc_text)
        elif "⚠️" in sonuc_text or "❌" in sonuc_text:
            st.warning(sonuc_text)
        else:
            st.markdown(sonuc_text, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Hata: {e}")
