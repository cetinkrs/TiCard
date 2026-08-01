import depolama
from datetime import datetime, timedelta #sadece import kullansaydık tüm datetime yi getirmek zorunda kalırdık bize sadece kullanacağımız kısmı getirsek kafidir.
#timedelta süre veya zaman üzerinde matematiksel işlemler yapabilmek için yazıyoruz.

class TiCardMotoru:
    def __init__(self):
        # Sistem açıldığında arşive gidip tüm JSON verisini RAM'e (hafızaya) alıyoruz
        self.veriler = depolama.verileri_yukle()

    def deste_olustur(self, deste_adi):
        # Yeni bir deste ekleme mantığı buraya yazılacak
        if self._deste_adi_var_mi(deste_adi):
            return False
        
        else:
            self.veriler[deste_adi] = {} #Sözlükler de köşeli parantez, sözlüğün içindeki bir "anahtar(key)" işaret etmek için kullanırız.
            depolama.verileri_kaydet(self.veriler)
            return True
    
    def kelime_olustur(self, deste_adi, kelime, anlam, cagrisim_ornek):
        if not self._deste_adi_var_mi(deste_adi):
            return False
        
        elif  self._kelime_var_mi(deste_adi, kelime):
            return False
        
        else:
            su_an = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.veriler[deste_adi][kelime] = {
                "anlam": anlam,
                "cagrisim_ornek": cagrisim_ornek,
                "durum": "yeni",
                "sonraki_tekrar": su_an# şimdilik rastgele bir tarih giriyoruz
            }
            depolama.verileri_kaydet(self.veriler)
            return True
    
    def kelime_sil(self, deste_adi, kelime):
        if not self._deste_adi_var_mi(deste_adi):
            return False 
        elif not self._kelime_var_mi(deste_adi, kelime):
            return False
        else:
            del self.veriler[deste_adi][kelime]
            depolama.verileri_kaydet(self.veriler)
            return True
    
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
        
    def _deste_adi_var_mi(self, deste_adi):
        return deste_adi in self.veriler
    def _kelime_var_mi(self, deste_adi, kelime):
        return kelime in self.veriler[deste_adi]
    
