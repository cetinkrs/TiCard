import customtkinter as ctk
from motor import TiCardMotoru

class TiCardApp(ctk.CTk ):
    def __init__(self):
        super().__init__()
        self.title("TiCard")
        self.motor = TiCardMotoru() # self lerin kullanımını araştır
        self.calisma_listesi = []
        self.calisma_index = 0
        self.geometry("900x600")
        self.giris_ekrani_goster()
    
    def giris_ekrani_goster(self):
        # Üst frame — başlık
        baslik_frame = ctk.CTkFrame(self)
        baslik_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        baslik = ctk.CTkLabel(
            baslik_frame, 
            text="TiCard", 
            font=("Arial", 40, "bold")
        )
        baslik.pack(pady=15)
        
        # Alt frame — açıklama + buton
        icerik_frame = ctk.CTkFrame(self)
        icerik_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        aciklama = ctk.CTkLabel(
            icerik_frame,
            text="Spaced Repetition yöntemiyle\nİngilizce kelime öğrenme uygulaması",
            font=("Arial", 14)
        )
        aciklama.pack(expand=True)
        
        basla_btn = ctk.CTkButton(
            icerik_frame,
            text="Başla",
            width=200,
            height=45,
            font=("Arial", 14, "bold"),
            command=self.ana_ekran_goster
        )
        basla_btn.pack(pady=30)
    
    def ana_ekran_goster(self):
        # Giriş ekranını temizle
        for widget in self.winfo_children():
            widget.destroy()
        
        # Ana container
        ana_frame = ctk.CTkFrame(self)
        ana_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sol panel
        sol_panel = ctk.CTkFrame(ana_frame, width=220)
        sol_panel.pack(side="left", fill="y", padx=(0, 10))
        sol_panel.pack_propagate(False)  # genişliği sabit tut
        
        sol_baslik = ctk.CTkLabel(
            sol_panel, 
            text="İşlemler",
            font=("Arial", 16, "bold")
        )
        sol_baslik.pack(pady=15)

        islemler = [
            ("Deste Oluştur", self.deste_olustur_ekrani),
            ("Kelime Ekle", self.kelime_ekle_ekrani),
            ("Çalışmaya Başla", self.calis_ekrani),
            ("Kelime Sil", self.kelime_sil_ekrani),
            ("Kelime Güncelle", self.kelime_guncelle_ekrani),
            ("Deste Sil", self.deste_sil_ekrani),
            ("İstatistikler", self.istatistik_ekrani),
        ]

        for metin, fonksiyon in islemler:
            btn = ctk.CTkButton(
                sol_panel,
                text=metin,
                command=fonksiyon
            )
            btn.pack(pady=5, padx=10, fill="x")

        # Sağ panel
        self.sag_panel = ctk.CTkFrame(ana_frame)
        self.sag_panel.pack(side="right", fill="both", expand=True)
        
        # Sağ üst — kelime gösterimi
        self.kelime_frame = ctk.CTkFrame(self.sag_panel)
        self.kelime_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        kelime_label = ctk.CTkLabel(
            self.kelime_frame,
            text="Hoşgeldiniz",
            font=("Arial", 24, "bold")
        )
        kelime_label.pack(pady=20)
        
        # Sağ alt — açıklama/istatistik
        self.icerik_frame = ctk.CTkFrame(self.sag_panel)
        self.icerik_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        icerik_label = ctk.CTkLabel(
            self.icerik_frame,
            text="Açıklama ve istatistikler burada görünecek",
            font=("Arial", 14)
        )
        icerik_label.pack(expand=True)

    def deste_olustur_ekrani(self):
        # icerik_frame'in eski içeriğini temizle
        for widget in self.icerik_frame.winfo_children():
            widget.destroy()

        baslik = ctk.CTkLabel(
            self.icerik_frame,
            text="Yeni Deste Oluştur",
            font=("Arial", 18, "bold")
        )
        baslik.pack(pady=(20, 10))
        
        self.deste_giris = ctk.CTkEntry(
            self.icerik_frame,
            placeholder_text="Deste adını yazın",
            width=250
        )
        self.deste_giris.pack(pady=10)

        sonuc_label = ctk.CTkLabel(self.icerik_frame, text="")
        sonuc_label.pack(pady=5)

        def olustur_tiklandi():
            deste_adi = self.deste_giris.get().strip()
            if deste_adi == "":
                sonuc_label.configure(text="Lütfen bir deste adı girin.", text_color="orange")
                return

            sonuc = self.motor.deste_olustur(deste_adi)
            if sonuc:
                sonuc_label.configure(text=f"'{deste_adi}' oluşturuldu!", text_color="green")
                self.deste_giris.delete(0, "end")
            else:
                sonuc_label.configure(text="Bu isimde bir deste zaten var.", text_color="red")

        olustur_btn = ctk.CTkButton(
            self.icerik_frame,
            text="Oluştur",
            command=olustur_tiklandi
        )
        olustur_btn.pack(pady=10)

    def kelime_ekle_ekrani(self):
        pencere = ctk.CTkToplevel(self)
        pencere.title("Kelime Ekle")
        pencere.geometry("400x400")
        baslik = ctk.CTkLabel(
            pencere,
            text = "Kelime Ekle",
            font = ("Arial", 20, "bold")
        )
        baslik.pack(pady=(20))
        
        deste_secenekleri = self.motor.deste_listesi_getir()
        #sonradan bu kısımda eğer deste yoksa hiç sıkıntı olabilir bunu en son bakıcaz hata düzeltmeleri olarak.!!!!
        self.deste_secim = ctk.CTkOptionMenu(
            pencere,
            values = deste_secenekleri
        )
        self.deste_secim.pack(pady=10)

        kelime_giris = ctk.CTkEntry(
            pencere,
            placeholder_text="Kelime giriniz",
            width=200
        )
        kelime_giris.pack(pady=(15))

        anlam_giris = ctk.CTkEntry(
            pencere,
            placeholder_text="Anlam giriniz",
            width=200
        )
        anlam_giris.pack(pady=(15))

        cagrisim_ornek_giris = ctk.CTkEntry(
            pencere,
            placeholder_text="Çağrışım örnek giriniz",
            width=200
        )
        cagrisim_ornek_giris.pack(pady=(15))

        sonuc_label = ctk.CTkLabel(pencere, text="")
        sonuc_label.pack(pady=(5))

        def kelime_tiklandi():
            deste_adi = self.deste_secim.get()
            kelime = kelime_giris.get().strip()
            anlam = anlam_giris.get().strip()
            cagrisim_ornek = cagrisim_ornek_giris.get().strip()

            if kelime == "" or anlam =="":
                sonuc_label.configure(text="Kelime ve anlam boş olamaz.", text_color = "orange")
                return 

            sonuc = self.motor.kelime_olustur(deste_adi, kelime, anlam, cagrisim_ornek)
            if sonuc:
                sonuc_label.configure(text=f"Kelimeniz eklendi!", text_color="green")
                kelime_giris.delete(0, "end")
                anlam_giris.delete(0, "end")
                cagrisim_ornek_giris.delete(0, "end")
            else:
                sonuc_label.configure(text="Deste bulunamadı veya kelime zaten var.", text_color="red")

        kelime_ekle = ctk.CTkButton(
            pencere,
            text="Oluştur",
            command=kelime_tiklandi
        )
        kelime_ekle.pack(pady=(15))
        
    def calis_ekrani(self):
        for widget in self.icerik_frame.winfo_children():
            widget.destroy()

        baslik = ctk.CTkLabel(
            self.icerik_frame,
            text="Çalışmaya Başlıyalım",
            font=("Arial", 18, "bold")
        )
        baslik.pack(pady = 10)

        desteler = self.motor.deste_listesi_getir()
        deste_secim = ctk.CTkOptionMenu(
            self.icerik_frame,
            values=desteler
        )
        deste_secim.pack(pady=15)

        def basla_tiklandi():
            self.deste_adi = deste_secim.get()
            self.calisma_listesi = self.motor.calisicak_kelimeleri_getir(self.deste_adi)
            self.calisma_index = 0
            for widget in self.icerik_frame.winfo_children():
                widget.destroy()
            if not self.calisma_listesi:
                bos_label = ctk.CTkLabel(self.icerik_frame, text="Çalışılacak kelime yok.")
                bos_label.pack(pady=15)
                return
            self.kelime_goster()

        deste_button = ctk.CTkButton(
            self.icerik_frame,
            text = "Başla",
            command=basla_tiklandi
        )
        deste_button.pack(pady=(10,15))

    def cevap_goster(self):
        for widget in self.icerik_frame.winfo_children():
            widget.destroy()
        su_anki_kelime = self.calisma_listesi[self.calisma_index]
        su_anki_anlam = self.motor.veriler[self.deste_adi][su_anki_kelime]["anlam"]
        su_anki_cagrisim = self.motor.veriler[self.deste_adi][su_anki_kelime]["cagrisim_ornek"]

        anlam_goster = ctk.CTkLabel(
            self.icerik_frame,
            text = f"Anlam:{su_anki_anlam}",
            font=("Arial", 12, "bold")
        )
        anlam_goster.pack(pady = 10)

        ornek_goster = ctk.CTkLabel(
            self.icerik_frame,
            text = f"Örnek: {su_anki_cagrisim}",
            font=("Arial", 12, "bold")
        )
        ornek_goster.pack(pady = 10)

        def zorluk_tiklandi(zorluk):
            self.motor.tekrar_zamani_guncelle(self.deste_adi, su_anki_kelime, zorluk)
            self.calisma_index +=1
            if self.calisma_index < len(self.calisma_listesi):
                self.kelime_goster()
            else:
                for widget in self.icerik_frame.winfo_children():
                    widget.destroy()
                for widget in self.kelime_frame.winfo_children():
                    widget.destroy()
                mesaj_lbl = ctk.CTkLabel(
                    self.icerik_frame,
                    text="Tebrikler Desteyi Bitirdiniz.",
                    font=("Arial", 24, "bold")
                )
                mesaj_lbl.pack(pady=15)
        btn_frame = ctk.CTkFrame(self.icerik_frame)
        btn_frame.pack(pady=150)

        kolay_btn = ctk.CTkButton(
            btn_frame,
            text = "Kolay",
            command=lambda: zorluk_tiklandi("kolay")
        )
        kolay_btn.pack(side="left", padx=10, pady=10)

        orta_btn = ctk.CTkButton(
            btn_frame,
            text = "Orta",
            command=lambda: zorluk_tiklandi("orta")
        )
        orta_btn.pack(side="left", padx=10, pady=10)

        zor_btn = ctk.CTkButton(
            btn_frame,
            text = "Zor",
            command=lambda: zorluk_tiklandi("zor")
        )
        zor_btn.pack(side="left", padx=10, pady=10) 
        
    def kelime_goster(self):
        for widget in self.kelime_frame.winfo_children():
            widget.destroy()
        for widget in self.icerik_frame.winfo_children():
            widget.destroy()        
        su_anki_kelime = self.calisma_listesi[self.calisma_index]

        kelime_label = ctk.CTkLabel(
            self.kelime_frame,
            text = su_anki_kelime,
            font=("Arial", 24, "bold")
        )
        kelime_label.pack(pady=20)

        cvp_btn = ctk.CTkButton(
            self.icerik_frame,
            text = "Cevabı Gör",
            command=self.cevap_goster
        )
        cvp_btn.pack(pady=20) 
            
    def kelime_sil_ekrani(self):
        pencere = ctk.CTkToplevel(self)
        pencere.title("Kelime Sil")
        pencere.geometry("400x400")

        baslik = ctk.CTkLabel(
            pencere,
            text = "Kelime Sil",
            font = ("Arial", 20, "bold")
        )
        baslik.pack(pady = (10))

        deste_secenekleri = self.motor.deste_listesi_getir()
        deste_secim = ctk.CTkOptionMenu(
            pencere,
            values= deste_secenekleri
        )
        deste_secim.pack(pady = (10))

        kelime_secenekleri = self.motor.kelime_listesi_getir(deste_secim.get())
        kelime_secim = ctk.CTkOptionMenu(
            pencere,
            values= kelime_secenekleri,
        )
        kelime_secim.pack(pady = (10))

        def deste_degisti(secilen_deste):
            yeni_kelimeler = self.motor.kelime_listesi_getir(secilen_deste)
            kelime_secim.configure(values=yeni_kelimeler)
            if yeni_kelimeler:
                kelime_secim.set(yeni_kelimeler[0])
            else:
                kelime_secim.set("")

        deste_secim.configure(command=deste_degisti)

        sonuc_label = ctk.CTkLabel(pencere, text="")
        sonuc_label.pack(pady=5)

        def sil_tiklandi():
            deste_adi = deste_secim.get()
            kelime = kelime_secim.get()

            if kelime == "":
                sonuc_label.configure(text="Silinecek kelime yok.", text_color="orange")
                return
            sonuc = self.motor.kelime_sil(deste_adi, kelime)
            if sonuc:
                sonuc_label.configure(text=f"'{kelime}' silindi!", text_color="green")
                deste_degisti(deste_adi)
            else:
                sonuc_label.configure(text="Silme işlemi başarısız.", text_color="red")
        sil_btn = ctk.CTkButton(
            pencere,
            text="Sil",
            command=sil_tiklandi
        )   
        sil_btn.pack(pady=(15))
    
    def kelime_guncelle_ekrani(self):
        pencere = ctk.CTkToplevel(self)
        pencere.title("Kelime Güncelle")
        pencere.geometry("400x400")

        baslik = ctk.CTkLabel(
            pencere,
            text = "Kelime Güncelle",
            font = ("Arial", 20, "bold")
        )
        baslik.pack(pady=15)

        desteler = self.motor.deste_listesi_getir()
        deste_secim = ctk.CTkOptionMenu(
            pencere,
            values = desteler
        )
        deste_secim.pack(pady=15)

        kelime_secenekleri = list(self.motor.veriler[deste_secim.get()].keys())
        kelime_secim = ctk.CTkOptionMenu(
            pencere,
            values= kelime_secenekleri,
        )
        kelime_secim.pack(pady = (10))

        anlam_entry = ctk.CTkEntry(
            pencere,
            placeholder_text = "anlam giriniz",
            width = 200
        )
        anlam_entry.pack(pady=15)


        cagrisim_entry = ctk.CTkEntry(
            pencere,
            placeholder_text = "örnek giriniz",
            width = 200
        )
        cagrisim_entry.pack(pady=15)

        def deste_degisti(secilen_deste):
            yeni_kelimeler = list(self.motor.veriler[secilen_deste].keys())
            kelime_secim.configure(values=yeni_kelimeler)
            if yeni_kelimeler:
                kelime_secim.set(yeni_kelimeler[0])
            else:
                kelime_secim.set("")
        
        deste_secim.configure(command=deste_degisti)

        sonuc_label = ctk.CTkLabel(pencere, text="")
        sonuc_label.pack(pady=5)

        def guncelle_tiklandi():
            yeni_anlam = anlam_entry.get().strip()
            if yeni_anlam == "":
                 yeni_anlam = None

            yeni_cagrisim = cagrisim_entry.get().strip()
            if yeni_cagrisim == "":
                yeni_cagrisim = None           
            deste_adi = deste_secim.get()
            kelime = kelime_secim.get()
            if kelime == "":
                sonuc_label.configure(text="güncellenecek kelime yok", text_color="orange")
                return
            
            sonuc = self.motor.kelime_güncelle(deste_adi, kelime, yeni_anlam, yeni_cagrisim)
            if sonuc:
                sonuc_label.configure(text=f"'{kelime}' güncellendi!", text_color="green")
                deste_degisti(deste_adi)
            else:
                sonuc_label.configure(text="Güncelleme işlemi başarısız.", text_color="red")

        guncelle_btn = ctk.CTkButton(
            pencere,
            text = "Güncelle",
            command=guncelle_tiklandi
        )
        guncelle_btn.pack(pady=15)

    def deste_sil_ekrani(self):
        pencere = ctk.CTkToplevel(self)
        pencere.title("Deste Sil")
        pencere.geometry("400x400")

        baslik = ctk.CTkLabel(
            pencere,
            text="Deste Sil",
            font=("Arial", 20, "bold")
        )
        baslik.pack(pady=(15))
        desteler = self.motor.deste_listesi_getir()
        deste_secim = ctk.CTkOptionMenu(
            pencere,
            values = desteler
        )
        deste_secim.pack(pady=15)

        
        sonuc_label = ctk.CTkLabel(pencere, text="")
        sonuc_label.pack(pady=5)

        def sil_tiklandi():
            deste_adi = deste_secim.get()

            if deste_adi == "":
                sonuc_label.configure(text="Silinecek deste yok", text_color = "orange")
                return

            sonuc = self.motor.deste_sil(deste_adi)
            if sonuc:
                sonuc_label.configure(text="Desteniz silinmiştir", text_color = "green")
                deste_guncelle() 
            else:
                sonuc_label.configure(text="Silme işlemi başarısız.", text_color="red")
                

        sil_btn = ctk.CTkButton(
            pencere,
            text="Sil",
            command=sil_tiklandi
        )
        sil_btn.pack(pady=5)

        def deste_guncelle():
            deste = self.motor.deste_listesi_getir()
            deste_secim.configure(values = deste)
            if deste:
                deste_secim.set(deste[0])
            else:
                deste_secim.set("")
        
    def istatistik_ekrani(self):
        for widget in self.icerik_frame.winfo_children():
            widget.destroy()
        
        baslik = ctk.CTkLabel(
            self.icerik_frame,
            text="İstatistikler",
            font=("Arial", 30, "bold")
        )
        baslik.pack(pady=15)

        sonuc = self.motor.istatistik_getir()

        toplam_label = ctk.CTkLabel(
            self.icerik_frame,
            text=f"Toplam deste sayısı: {sonuc['toplam_deste']}"
        )
        toplam_label.pack(pady=10)
        
        for i, (deste_adi, kelime_sayisi) in enumerate(sonuc["desteler"].items(), start = 1):
            satir = ctk.CTkLabel(
                self.icerik_frame,
                text=f"{i}.Deste: {deste_adi}. Kelime sayisi: {kelime_sayisi}"
            )
            satir.pack(pady=5)
            
        
        bugun_calis = ctk.CTkLabel(
            self.icerik_frame,
            text=f"Bugün Çalışılıcak Kelime Sayısı: {sonuc['bugun_calisilicak']}"
        )
        bugun_calis.pack(pady=10)



if __name__ == "__main__":
    app = TiCardApp()
    app.mainloop()