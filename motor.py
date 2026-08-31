import depolama
from datetime import datetime, timedelta #sadece import kullansaydık tüm datetime yi getirmek zorunda kalırdık bize sadece kullanacağımız kısmı getirsek kafidir.
#timedelta süre veya zaman üzerinde matematiksel işlemler yapabilmek için yazıyoruz.

class TiCardMotoru:
    def __init__(self):
        try: 
            baglanti = depolama.baglanti_olustur()
            if baglanti:
                baglanti.close()
        except Exception:
            print("Uyarı: Veritabanı bağlantısı kurulamadı!")

    def deste_olustur(self, deste_adi):
        
        if self._deste_adi_var_mi(deste_adi):
            return False
        
        else:
            sonuc = depolama.sorgu_calistir(
                "INSERT INTO desteler (deste_adi) VALUES (%s)",
                (deste_adi,)
            )
            return sonuc
    
    def kelime_olustur(self, deste_adi, kelime, anlam, cagrisim_ornek):
        if not self._deste_adi_var_mi(deste_adi):
            return False
        
        elif  self._kelime_var_mi(deste_adi, kelime):
            return False
        
        else:
            deste_sonuc = depolama.sorgu_calistir(
                "SELECT id FROM desteler WHERE deste_adi = %s",
                (deste_adi,),
                fetch=True
            )
            deste_id = deste_sonuc[0][0]

            su_an = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sonuc = depolama.sorgu_calistir(
                """
                INSERT INTO kelimeler (deste_id, kelime, anlam, cagrisim_ornek, n_degeri, ef_degeri, interval_gun, sonraki_tekrar)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (deste_id, kelime, anlam, cagrisim_ornek, 0, 2.5, 0, su_an)
            )
            return sonuc
        
    def kelime_sil(self, deste_adi, kelime):
        if not self._deste_adi_var_mi(deste_adi):
            return False 
        elif not self._kelime_var_mi(deste_adi, kelime):
            return False
        else:
            deste_sonuc = depolama.sorgu_calistir(
                "SELECT id FROM desteler WHERE  deste_adi = %s",
                (deste_adi,),
                fetch = True
            )
            deste_id = deste_sonuc[0][0]

            sonuc = depolama.sorgu_calistir(
                "DELETE FROM kelimeler WHERE deste_id = %s AND kelime = %s",
                (deste_id, kelime)
            )
            return sonuc
    def tekrar_zamani_guncelle(self, deste_adi, kelime, zorluk_secimi):
        if not self._deste_adi_var_mi(deste_adi):
            return False
        elif not self._kelime_var_mi(deste_adi, kelime):
            return False
        else:
            su_an = datetime.now()
            if zorluk_secimi == "zor":
                yeni_tarih = su_an + timedelta(minutes=10)

            elif zorluk_secimi == "orta":
                yeni_tarih = su_an + timedelta(days=1)

            elif zorluk_secimi == "kolay":
                yeni_tarih = su_an + timedelta(days=4)

            else:
                print("Yanlış zorluk seçimi lütfen daha sonra tekrar deneyiniz.")
                return False
                #UI de burayı kullanıcının tekrar bir seçim yapmasına olanak tanıyacağımız şekilde düzenlememiz laızm .
            self.veriler[deste_adi][kelime]["sonraki_tekrar"] = yeni_tarih.strftime("%Y-%m-%d %H:%M:%S")
            depolama.verileri_kaydet(self.veriler)
            
            return True
    
    def calisicak_kelimeleri_getir(self, deste_adi):
        if not self._deste_adi_var_mi(deste_adi):
            return []
        else:
            su_an = datetime.now()
            calisilacaklar = []
            for kelime,bilgiler in self.veriler[deste_adi].items(): #items() hem anahtar hem de değeri getirir
                kayitli_tarih = datetime.strptime(bilgiler["sonraki_tekrar"], "%Y-%m-%d %H:%M:%S") #burada metni zamana çeviriyoruz jsson dosyasında metin olarak saklamıştık çünkü.
                if kayitli_tarih <= su_an:
                    calisilacaklar.append(kelime)
            return calisilacaklar
    
    def kelime_güncelle(self, deste_adi, kelime, anlam = None, cagrisim_ornek = None):
        if not self._deste_adi_var_mi(deste_adi):
            return False
        elif not self._kelime_var_mi(deste_adi, kelime):
            return False
        else:
            if anlam is not  None:
                self.veriler[deste_adi][kelime]["anlam"] = anlam
            if cagrisim_ornek is not None:
                self.veriler[deste_adi][kelime]["cagrisim_ornek"] = cagrisim_ornek
            depolama.verileri_kaydet(self.veriler)
            return True

    def deste_sil(self, deste_adi):
        if not self._deste_adi_var_mi(deste_adi):
            return False
        else:
            deste_sonuc = depolama.sorgu_calistir(
                "SELECT id FROM desteler WHERE  deste_adi = %s",
                (deste_adi,),
                fetch = True
            )
            deste_id = deste_sonuc[0][0]
            sonuc = depolama.sorgu_calistir(
                "DELETE FROM kelimeler WHERE deste_id = %s",
                (deste_id,)
            )
            sonuc2 = depolama.sorgu_calistir(
                "DELETE FROM desteler WHERE deste_adi = %s",
                (deste_adi,)
            )
            return sonuc2
            
    def istatistik_getir(self):
        toplam_deste = len(self.veriler)
        desteler = {}
        bugun_calisilicak = 0
        for deste in self.veriler:
            desteler[deste] = len(self.veriler[deste])
            bugun_calisilicak += len(self.calisicak_kelimeleri_getir(deste))
        return {
            "toplam_deste" : toplam_deste,
            "desteler" : desteler,
            "bugun_calisilicak" : bugun_calisilicak
        }

#Yardımcı metotlar

    def _deste_adi_var_mi(self, deste_adi):
        sonuc = depolama.sorgu_calistir(
            "SELECT id FROM desteler WHERE deste_adi = %s",
            (deste_adi,),
            fetch=True
        )
        return len(sonuc) > 0 
    
    def _kelime_var_mi(self, deste_adi, kelime):
        sonuc = depolama.sorgu_calistir(
            "SELECT d.deste_adi ,k.kelime FROM kelimeler k JOIN desteler d ON k.deste_id = d.id WHERE d.deste_adi = %s AND k.kelime = %s",
            (deste_adi, kelime),
            fetch = True
        )
        return len(sonuc) > 0 
#API ye implementasyonu sonrası burayı bir kontrol et çünkü performans düşürüyor 
    def deste_listesi_getir(self):
        ham_sonuc = depolama.sorgu_calistir("SELECT deste_adi FROM desteler", fetch = True)
        return [satir[0] for satir in ham_sonuc]

    def kelime_listesi_getir(self, deste_adi):
        ham_sonuc = depolama.sorgu_calistir(
            "SELECT k.kelime FROM kelimeler k JOIN desteler d ON k.deste_id = d.id WHERE d.deste_adi = %s",
            (deste_adi,),
            fetch=True
        )
        return [satir[0] for satir in ham_sonuc]