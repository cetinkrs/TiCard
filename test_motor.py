import os 
import depolama
import pytest
from motor import TiCardMotoru  

# @ diğer bir diyişle decorator, bir fonkiyonu başka bir fonksiyonun içine sararak ona ekstra özellik kazandırır.
@pytest.fixture 
def motor():
    m = TiCardMotoru()
    yield m #return a benzer ama return deki gibi fonksiyon tamamen kapanmaz
    if os.path.exists("test_kelimeler.json"):
        os.remove("test_kelimeler.json")

depolama.DOSYA_YOLU = "test_kelimeler.json"

#DESTE_OLUSTUR
def test_deste_olustur_basarili(motor):
    sonuc = motor.deste_olustur("Test_Destesi") 
    assert sonuc == True
#assert: Fonksiyonun döndürdüğü değer, beklediğim değerle eşleşmeli demektir.
def test_deste_olustur_ayni_isim(motor):
    motor.deste_olustur("Test_Destesi")
    sonuc = motor.deste_olustur("Test_Destesi")
    assert sonuc == False

#KELİME_OLUSTUR
def test_kelime_olustur_basarili_ekleme(motor):
    motor.deste_olustur("Test_Destesi")
    sonuc = motor.kelime_olustur("Test_Destesi", "variable", "değişken", "")
    assert sonuc == True

def test_kelime_olustur_deste_yok(motor):
    sonuc = motor.kelime_olustur("Test_Destesi", "variable", "değişken", "")
    assert sonuc == False

def test_kelime_olustur_kelime_var(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "Elde Etmek", "")
    sonuc = motor.kelime_olustur("Test_Destesi", "Acquire", "Elde Etmek", "")
    assert sonuc == False

#KELİME_SİL
def test_kelime_sil_basarili(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "Elde Etmek", "")
    sonuc = motor.kelime_sil("Test_Destesi", "Acquire")
    assert sonuc == True

def test_kelime_sil_deste_yok(motor):
    sonuc = motor.kelime_sil("Test_Destesi", "Acquire")
    assert sonuc == False

def test_kelime_sil_kelime_yok(motor):
    motor.deste_olustur("Test_Destesi")
    sonuc = motor.kelime_sil("Test_Destesi", "Acquire")
    assert sonuc == False

#TEKRAR_ZAMANİ_GUNCELLE
def test_tekrar_zamani_guncelle_basarili(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "Elde Etmek", "")
    sonuc = motor.tekrar_zamani_guncelle("Test_Destesi", "Acquire", "zor")
    assert sonuc == True

def test_tekrar_zamani_guncelle_deste_yok(motor):
    sonuc = motor.tekrar_zamani_guncelle("Test_Destesi", "Acquire", "zor")
    assert sonuc == False

def test_tekrar_zamani_guncelle_kelime_yok(motor):
    motor.deste_olustur("Test_Destesi")
    sonuc = motor.tekrar_zamani_guncelle("Test_Destesi", "Acquire", "zor")
    assert sonuc == False
    
def test_tekrar_zamani_guncelle_kolay(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "Elde Etmek", "")
    sonuc = motor.tekrar_zamani_guncelle("Test_Destesi", "Acquire", "kolay")
    assert sonuc == True

def test_tekrar_zamani_guncelle_orta(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "Elde Etmek", "")
    sonuc = motor.tekrar_zamani_guncelle("Test_Destesi", "Acquire", "orta")
    assert sonuc == True

def test_tekrar_zamani_guncelle_gecersiz_secim(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "Elde Etmek", "")
    sonuc = motor.tekrar_zamani_guncelle("Test_Destesi", "Acquire", "4")
    assert sonuc == False

#KELİME_GUNCELLE
def test_kelime_guncelle_basarili(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "Elde Etmek", "")
    sonuc = motor.kelime_güncelle("Test_Destesi", "Acquire", "Edinmek", "Örnek cümle")
    assert sonuc == True

def test_kelime_guncelle_deste_yok(motor):
    sonuc = motor.kelime_güncelle("Test_Destesi", "Acquire", "Edinmek", "Örnek cümle")
    assert sonuc == False

def test_kelime_guncelle_kelime_yok(motor):
    motor.deste_olustur("Test_Destesi")
    sonuc = motor.kelime_güncelle("Test_Destesi", "Acquire", "Edinmek", "Örnek cümle")
    assert sonuc == False

def test_kelime_guncelle_sadece_ornek(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "eski anlam", "eski örnek")
    motor.kelime_güncelle("Test_Destesi", "Acquire", cagrisim_ornek="yeni örnek")
    
    assert motor.veriler["Test_Destesi"]["Acquire"]["cagrisim_ornek"] == "yeni örnek"
    assert motor.veriler["Test_Destesi"]["Acquire"]["anlam"] == "eski anlam"

def test_kelime_guncelle_sadece_anlam(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "eski anlam", "eski örnek")
    motor.kelime_güncelle("Test_Destesi", "Acquire", anlam="yeni anlam")

    assert motor.veriler["Test_Destesi"]["Acquire"]["cagrisim_ornek"] == "eski örnek"
    assert motor.veriler["Test_Destesi"]["Acquire"]["anlam"] == "yeni anlam"

def test_kelime_guncelle_her_ikiside(motor):
    motor.deste_olustur("Test_Destesi")
    motor.kelime_olustur("Test_Destesi", "Acquire", "eski anlam", "eski örnek")
    motor.kelime_güncelle("Test_Destesi", "Acquire", anlam="yeni anlam", cagrisim_ornek="yeni örnek")

    assert motor.veriler["Test_Destesi"]["Acquire"]["cagrisim_ornek"] == "yeni örnek"
    assert motor.veriler["Test_Destesi"]["Acquire"]["anlam"] == "yeni anlam"

#DESTE_SİL
def test_deste_sil_basarili(motor):
    motor.deste_olustur("Test_Destesi")
    sonuc = motor.deste_sil("Test_Destesi")

    assert sonuc == True

def test_deste_sil_deste_yok(motor):
    sonuc = motor.deste_sil("Test_Destesi")

    assert sonuc == False