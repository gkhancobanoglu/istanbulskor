import osmnx as ox
import pandas as pd
from geopy.geocoders import Nominatim
import time

def hesapla_yasam_skoru(mahalle, ilce, user_priorities):
    geolocator = Nominatim(user_agent="mahalle_app")
    location = geolocator.geocode(f"{mahalle}, {ilce}, Turkey")

    if not location:
        raise ValueError("❌ Mahalle bulunamadı.")

    lat, lon = location.latitude, location.longitude

    tags_dict = {
        "Park": {"leisure": ["park", "garden", "recreation_ground", "nature_reserve"]},
        "Okul": {"amenity": ["school", "college", "kindergarten"]},
        "Market": {"shop": ["supermarket", "convenience", "greengrocer", "bakery"]},
        "Hastane": {"amenity": ["hospital", "clinic", "doctors", "health_post", "healthcare"]},
        "Ulaşım": {"public_transport": ["station", "stop_position", "platform"], "amenity": ["bus_station", "ferry_terminal"]}
    }

    detaylar = []
    toplam_skor = 0
    max_poi_sayisi = 20
    kategori_uyum = {}

    for kategori, tag in tags_dict.items():
        try:
            pois = ox.features_from_point((lat, lon), tags=tag, dist=800)
            pois = pois[pois["name"].notna()]
            count = len(pois)
        except:
            count = 0

        agirlik = user_priorities.get(kategori, 1)

        if count == 0:
            puan = 0
        elif count < 3:
            puan = agirlik * 10
        elif count < 6:
            puan = agirlik * 20
        elif count < 10:
            puan = agirlik * 30
        elif count < 15:
            puan = agirlik * 35
        elif count < 20:
            puan = agirlik * 40
        else:
            puan = agirlik * 45

        toplam_skor += puan
        kategori_uyum[kategori] = count > 0

        detaylar.append({
            "Kategori": kategori,
            "Sayı": count,
            "Ağırlık": agirlik,
            "Puan": round(puan, 2)
        })

        time.sleep(1)

    if all(kategori_uyum.values()):
        uyum_durumu = "✅ Bu mahalle 15 Dakikalık Şehir modeline uygundur."
    else:
        eksikler = [k for k, v in kategori_uyum.items() if not v]
        uyum_durumu = f"❌ 15 Dakika Uyumlu Değil. Eksikler: {', '.join(eksikler)}"

    return {
        "koordinat": (lat, lon),
        "detaylar": detaylar,
        "toplam_skor": round(toplam_skor, 2),
        "uyum": uyum_durumu
    }
