import json
import psycopg2
import os
from datetime import datetime

# Veritabanı bağlantı bilgileri
DB_HOST = "localhost"
DB_NAME = "ticard_db"
DB_USER = "postgres"
DB_PASS = "5432" 

DOSYA_YOLU = os.path.join(os.path.dirname(__file__), "kelimeler.json")

def aktar():
    try:
        # Veritabanına bağlan
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = conn.cursor()

        # Tabloyu oluştur (SM-2 değişkenleri eklendi)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kelimeler (
                id SERIAL PRIMARY KEY,
                deste_adi VARCHAR(100),
                kelime VARCHAR(100),
                anlam TEXT,
                cagrisim_ornek TEXT,
                n_degeri INTEGER DEFAULT 0,
                ef_degeri REAL DEFAULT 2.5,
                interval_gun INTEGER DEFAULT 0,
                sonraki_tekrar TIMESTAMP
            )
        """)

        # Mevcut JSON dosyasını oku
        with open(DOSYA_YOLU, "r", encoding="utf-8") as dosya:
            veriler = json.load(dosya)

        # Verileri PostgreSQL tablosuna ekle
        for deste_adi, kelimeler in veriler.items():
            for kelime, bilgiler in kelimeler.items():
                anlam = bilgiler.get("anlam", "")
                cagrisim = bilgiler.get("cagrisim_ornek", "")
                sonraki_tekrar = bilgiler.get("sonraki_tekrar", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                # Yeni değerler: n=0, ef=2.5, i=0
                cursor.execute("""
                    INSERT INTO kelimeler (deste_adi, kelime, anlam, cagrisim_ornek, n_degeri, ef_degeri, interval_gun, sonraki_tekrar)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (deste_adi, kelime, anlam, cagrisim, 0, 2.5, 0, sonraki_tekrar))

        conn.commit()
        cursor.close()
        conn.close()
        print("Veri göçü başarıyla tamamlandı. SM-2 altyapısı hazır!")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    aktar()