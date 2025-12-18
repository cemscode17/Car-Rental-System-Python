# core/database.py
import json
import os
from datetime import datetime

class AracYonetici:
    def __init__(self, dosya_adi='araclar.json'):
        self.dosya_adi = dosya_adi
        self.veriler = self.veri_yukle()

    def veri_yukle(self):
        if not os.path.exists(self.dosya_adi):
            return {"araclar": [], "toplam_gelir": 0, "gecmis_islemler": []}
        try:
            with open(self.dosya_adi, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"araclar": [], "toplam_gelir": 0, "gecmis_islemler": []}

    def kaydet(self):
        with open(self.dosya_adi, 'w', encoding='utf-8') as f:
            json.dump(self.veriler, f, ensure_ascii=False, indent=4)

    # GÜNCELLENDİ: resim_yolu parametresi eklendi
    def arac_ekle(self, plaka, marka, model, ucret, resim_yolu="assets/default_car.png"):
        yeni_arac = {
            "plaka": plaka, "marka": marka, "model": model,
            "ucret": float(ucret), "durum": "Müsait",
            "resim": resim_yolu,  # Yeni alan
            "kiralayan": "", "baslangic": "", "bitis": ""
        }
        self.veriler["araclar"].append(yeni_arac)
        self.kaydet()

    def arac_sil(self, index):
        del self.veriler["araclar"][index]
        self.kaydet()

    def arac_guncelle(self, index, plaka, marka, model, ucret):
        arac = self.veriler["araclar"][index]
        arac["plaka"] = plaka
        arac["marka"] = marka
        arac["model"] = model
        arac["ucret"] = float(ucret)
        self.kaydet()

    def kiralama_yap(self, index, musteri, gun_sayisi, toplam_tutar, baslangic, bitis):
        arac = self.veriler["araclar"][index]
        arac["durum"] = "Kirada"
        arac["kiralayan"] = musteri
        arac["baslangic"] = baslangic
        arac["bitis"] = bitis
        
        self.veriler["toplam_gelir"] += toplam_tutar
        
        self.veriler["gecmis_islemler"].append({
            "plaka": arac["plaka"], 
            "marka": arac["marka"],  
            "model": arac["model"], 
            "tutar": toplam_tutar,
            "gun": gun_sayisi, 
            "tarih": datetime.now().strftime("%Y-%m-%d"), 
            "musteri": musteri
        })
        self.kaydet()

    def iade_al(self, index):
        arac = self.veriler["araclar"][index]
        arac["durum"] = "Müsait"
        arac["kiralayan"] = ""; arac["baslangic"] = ""; arac["bitis"] = ""
        self.kaydet()