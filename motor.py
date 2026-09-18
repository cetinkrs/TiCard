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
            deste_id = self._deste_id_bul(deste_adi)

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
            deste_id = self._deste_id_bul(deste_adi)

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

            if zorluk_secimi == "tekrar":
                q = 2
            elif zorluk_secimi == "zor":
                q = 3
            elif zorluk_secimi == "orta":
                q = 4
            elif zorluk_secimi == "kolay":
                q = 5
            else:
                print("Yanlış zorluk seçimi.")
                return False

            deste_id = self._deste_id_bul(deste_adi)

            mevcut_sonuc = depolama.sorgu_calistir(
                """
                SELECT k.n_degeri, k.ef_degeri, k.interval_gun
                FROM kelimeler k 
                JOIN desteler d ON k.deste_id = d.id
                WHERE d.deste_adi = %s AND k.kelime = %s
                """,
                (deste_adi, kelime),
                fetch = True
            )
            n = mevcut_sonuc[0][0]
            ef = mevcut_sonuc[0][1]
            i = mevcut_sonuc[0][2]

            n, yeni_ef, yeni_i = self._sm2_hesapla(n, ef, i, q)

            yeni_tarih = datetime.now() + timedelta(days = yeni_i)
            sonraki_tekrar = yeni_tarih.strftime("%Y-%m-%d %H:%M:%S")

            sonuc = depolama.sorgu_calistir(
            """
            UPDATE kelimeler
            SET n_degeri = %s, ef_degeri = %s, interval_gun = %s, sonraki_tekrar = %s
            WHERE deste_id = %s AND kelime = %s
            """,
            (n, yeni_ef, yeni_i, sonraki_tekrar, deste_id, kelime)
            )
            return sonuc


    def calisicak_kelimeleri_getir(self, deste_adi):
        if not self._deste_adi_var_mi(deste_adi):
            return []
        else:
            ham_sonuc = depolama.sorgu_calistir(
               "SELECT k.kelime FROM kelimeler k JOIN desteler d ON k.deste_id = d.id WHERE d.deste_adi = %s AND k.sonraki_tekrar <=NOW()",
                (deste_adi,),
                fetch = True
            )
            return [satir[0] for satir in ham_sonuc]
    
    def kelime_güncelle(self, deste_adi, kelime, anlam = None, cagrisim_ornek = None):
        if not self._deste_adi_var_mi(deste_adi):
            return False
        elif not self._kelime_var_mi(deste_adi, kelime):
            return False
        else:# şimdilik tekrarlı bir şekilde netlik amaçlı sorgular yazıcaz. İleride dinamik sql kurma mantığı ile burayı düzelticez.
            deste_id = self._deste_id_bul(deste_adi)

            if anlam is not  None and cagrisim_ornek is not None:
                sorgu = depolama.sorgu_calistir(
                    """
                    UPDATE kelimeler
                    SET anlam = %s, cagrisim_ornek = %s
                    WHERE deste_id = %s AND kelime = %s
                    """,
                    (anlam, cagrisim_ornek, deste_id, kelime)
                )
                return sorgu
            
            elif anlam is not None:
                sorgu = depolama.sorgu_calistir(
                    """
                    UPDATE kelimeler
                    SET anlam = %s
                    WHERE deste_id = %s AND kelime = %s
                    """,
                    (anlam, deste_id, kelime)
                )
                return sorgu
            elif cagrisim_ornek is not None:
                sorgu = depolama.sorgu_calistir(
                    """
                    UPDATE kelimeler
                    SET cagrisim_ornek = %s
                    WHERE deste_id = %s AND kelime = %s
                    """,
                    (cagrisim_ornek, deste_id, kelime)
                )
                return sorgu
            

    def deste_sil(self, deste_adi):
        if not self._deste_adi_var_mi(deste_adi):
            return False
        else:
            deste_id = self._deste_id_bul(deste_adi)
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
        toplam_sonuc = depolama.sorgu_calistir(
            "SELECT COUNT(*) FROM desteler",
            fetch = True
        )
        toplam_deste = toplam_sonuc[0][0]
        desteler = {}
        bugun_calisilicak_sonuc = depolama.sorgu_calistir(
            "SELECT COUNT(*) FROM kelimeler WHERE sonraki_tekrar <= NOW()",
            fetch = True
        )
        bugun_calisilicak = bugun_calisilicak_sonuc[0][0]

        desteler_sonuc = depolama.sorgu_calistir(
            """
            SELECT d.deste_adi, COUNT(k.id)
            FROM desteler d
            LEFT JOIN kelimeler k ON k.deste_id = d.id
            GROUP BY d.deste_adi
            """,
            fetch = True
        )
        for satir in desteler_sonuc:
            deste_adi = satir[0]
            kelime_sayisi = satir[1]
            desteler[deste_adi] = kelime_sayisi

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

    def _sm2_hesapla(self, n, ef, i, q):
        yeni_ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        if yeni_ef < 1.3:
            yeni_ef = 1.3

        if q < 3:
            yeni_n = 0
            yeni_i = 1
        else:
        
            if n == 0:
                yeni_i = 1
            elif n == 1:
                yeni_i = 6
            else:
                yeni_i = i * ef
            yeni_n = n + 1

        return yeni_n, yeni_ef, yeni_i

    def _deste_id_bul(self, deste_adi):
        deste_id = depolama.sorgu_calistir(
            "SELECT id FROM desteler WHERE deste_adi = %s",
            (deste_adi,),
            fetch = True
        )
        return deste_id[0][0]

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
    #main.py için
    def kelime_detay_getir(self, deste_adi, kelime):
        sonuc = depolama.sorgu_calistir(
            """
            SELECT k.anlam, k.cagrisim_ornek 
            FROM kelimeler k 
            JOIN desteler d ON k.deste_id = d.id 
            WHERE d.deste_adi = %s AND k.kelime = %s
            """,
            (deste_adi, kelime),
            fetch=True
        )
        if not sonuc:
            return None
        return {"anlam": sonuc[0][0], "cagrisim_ornek": sonuc[0][1]}