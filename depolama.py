import psycopg2

DB_HOST = "localhost"
DB_NAME = "ticard_db"
DB_USER = "postgres"
DB_PASS = "5432" 

def baglanti_olustur():
    """PostgreSQL veritabanına bağlantı açar."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def sorgu_calistir(sorgu, parametreler=None, fetch=False):
    """
    Gelen SQL sorgusunu çalıştırır.
    - fetch=True: SELECT işlemleri içindir, veritabanından okunan veriyi liste olarak döndürür.
    - fetch=False: INSERT, UPDATE, DELETE işlemleri içindir, veriyi yazar ve onaylar (commit).
    """
    conn = None
    try:
        conn = baglanti_olustur()
        cursor = conn.cursor()
        
        cursor.execute(sorgu, parametreler)
        
        if fetch:
            sonuc = cursor.fetchall()
            return sonuc
        else:
            conn.commit()
            return True
            
    except Exception as e:
        print(f"Veritabanı Hatası: {e}")
        if conn:
            conn.rollback() 
        return False
        
    finally:
        if conn:
            cursor.close()
            conn.close()