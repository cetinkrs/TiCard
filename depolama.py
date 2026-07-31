#bu modülün amacı fiziksel diske kazıma veya diskten okuma gibi düşünebilirsin.
import json
import os #Pythona windows ve mac in dosya sistemine müdahele etmesine izin veren yetki diyebiliriz.(operating system- işletim sistemi denir.)

klasor = os.path.dirname(__file__)
DOSYA_YOLU = os.path.join(klasor, "kelimeler.json")

def verileri_yukle():
    """Program açıldığında JSON dosyasını okur. Dosya yoksa otomatik oluşturur."""
    # Dosya sistemde var mı diye kontrol et
    if not os.path.exists(DOSYA_YOLU): # buradaki kod satırı Bulunduğum klasörün içerisinde ... dosya adında bir dosya varmı ona bakar True veya False döndürür.
        # Dosya yoksa 'w' modunda açıp içine boş bir süslü parantez (sözlük) yazıyoruz
        with open(DOSYA_YOLU, "w", encoding="utf-8") as dosya:
            json.dump({}, dosya)
        return {} # Boş sözlük döndür
    try:
        # Dosya varsa 'r' (varsayılan) moduyla okuyup içindeki veriyi Python'a aktar
        with open(DOSYA_YOLU, "r", encoding="utf-8") as dosya:
                return json.load(dosya)
    except json.JSONDecodeError:
        os.rename(DOSYA_YOLU, DOSYA_YOLU.replace(".json", "_bozuk.json"))
        print("UYARI: kelimeler.json bozuk görünüyor.Bozuk dosya 'kelimeler_bozuk.json' olarak yedeklendi.Uygulama boş veriyle başlatılıyor.")
        return {}
    except OSError:
        print("Dosya açılamadı.")
        return {}
def verileri_kaydet(veri):
    """Sistemdeki güncel veriyi (sözlüğü) alıp JSON formatında dosyaya yazar."""
    with open(DOSYA_YOLU, "w", encoding="utf-8") as dosya:
        json.dump(veri, dosya, ensure_ascii=False, indent=4)
