import json
import psycopg2
import os
from datetime import datetime

DB_HOST = "localhost"
DB_NAME = "ticard_db"
DB_USER = "postgres"
DB_PASS = "5432"

DOSYA_YOLU = os.path.join(os.path.dirname(__file__), "kelimeler.json")

def aktar():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        cursor = conn.cursor()

        # Eski tabloları temizle (şema değişti, sıfırdan kuruyoruz)
        cursor.execute("DROP TABLE IF EXISTS kelimeler")
        cursor.execute("DROP TABLE IF EXISTS desteler")

        cursor.execute("""
            CREATE TABLE desteler (
                id SERIAL PRIMARY KEY,
                deste_adi VARCHAR(100) UNIQUE
            )
        """)

        cursor.execute("""
            CREATE TABLE kelimeler (
                id SERIAL PRIMARY KEY,
                deste_id INTEGER REFERENCES desteler(id),
                kelime VARCHAR(100),
                anlam TEXT,
                cagrisim_ornek TEXT,
                n_degeri INTEGER DEFAULT 0,
                ef_degeri REAL DEFAULT 2.5,
                interval_gun INTEGER DEFAULT 0,
                sonraki_tekrar TIMESTAMP
            )
        """)

        with open(DOSYA_YOLU, "r", encoding="utf-8") as dosya:
            veriler = json.load(dosya)

        for deste_adi, kelimeler in veriler.items():
            cursor.execute(
                "INSERT INTO desteler (deste_adi) VALUES (%s) RETURNING id",
                (deste_adi,)
            )
            deste_id = cursor.fetchone()[0]

            for kelime, bilgiler in kelimeler.items():
                anlam = bilgiler.get("anlam", "")
                cagrisim = bilgiler.get("cagrisim_ornek", "")
                sonraki_tekrar = bilgiler.get("sonraki_tekrar", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                cursor.execute("""
                    INSERT INTO kelimeler (deste_id, kelime, anlam, cagrisim_ornek, n_degeri, ef_degeri, interval_gun, sonraki_tekrar)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (deste_id, kelime, anlam, cagrisim, 0, 2.5, 0, sonraki_tekrar))

        conn.commit()
        cursor.close()
        conn.close()
        print("Veri göçü başarıyla tamamlandı. desteler + kelimeler tabloları hazır!")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    aktar()