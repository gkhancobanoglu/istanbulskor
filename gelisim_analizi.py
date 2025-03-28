import json

def gelisim_analizi(mahalle, ilce, detaylar, toplam_skor, nufus_json_path="nufus_verisi.json"):
    try:
        with open(nufus_json_path, "r", encoding="utf-8") as f:
            nufus_data = json.load(f)
    except FileNotFoundError:
        return "❌ Nüfus verisi dosyası bulunamadı."
    except json.JSONDecodeError:
        return "❌ Nüfus verisi okunurken bir hata oluştu."

    key = f"{mahalle}, {ilce}"
    mahalle_verisi = nufus_data.get(key)


    if not mahalle_verisi or "nufus" not in mahalle_verisi:
        return "⚠️ Bu mahalle için nüfus bilgisi bulunamadı."

    nufus = mahalle_verisi["nufus"]
    yuksek_nufus = nufus >= 5000
    dusuk_skor = toplam_skor <= 350

    if not (yuksek_nufus and dusuk_skor):
        return "✅ Bu mahalle yatırım önceliği taşımamaktadır."

    eksik_kategoriler = [item["Kategori"] for item in detaylar if item["Sayı"] < 2]

    if not eksik_kategoriler:
        return "💡 Bu mahallede altyapı yeterli düzeydedir, yatırım önerisi bulunmamaktadır."

    sonuc = f"🔴 <b>{mahalle}, {ilce}</b><br>"
    sonuc += f"👥 <b>Nüfus:</b> {nufus:,} kişi<br>"
    sonuc += f"📉 <b>Skor:</b> {toplam_skor} <span style='color:red'>(Düşük)</span><br>"
    sonuc += f"<hr><b>🧱 Eksik Altyapılar:</b> {', '.join(eksik_kategoriler)}<br><br>"

    sonuc += "<b>🛠️ Önerilen Yatırımlar:</b><ul>"
    for eksik in eksik_kategoriler:
        sonuc += f"<li>{eksik} altyapısı artırılmalı.</li>"
    sonuc += "</ul>"

    return sonuc
