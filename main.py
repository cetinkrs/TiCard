from motor import TiCardMotoru

def ana_menu():
    motor = TiCardMotoru()
    print("TiCard Kelime Öğrenme Sistemine Hoş Geldiniz!")

    while True:
        try:
            print("[1] Deste Oluştur\t[2] Kelime Ekle\t[3] Çalışmaya Başla\t[4] Kelime Sil\t[5] Kelime Güncelle\t[6] Çıkış ")
            secim = int(input("Yapmak İstediğiniz İşlemi Seçiniz: "))

            if secim == 1:

                deste_ismi = input("Desteye vermek istediğiniz metni giriniz: ")
                sonuc = motor.deste_olustur(deste_ismi)
                if sonuc == True:
                    print("Desteniz başarıyla oluşturuldu")
                else:
                    print("Zaten bu adda bir deste var")
            
            elif secim == 2:

                print(f"Mevcut desteler: {list(motor.veriler.keys())}")
                deste_ismi = input("İşlemini yapmak istediğiniz destenin adını giriniz: ")
                kelime = input("Girmek istediğiniz kelimeyi seçiniz: ")
                anlam = input("Girdiğiniz kelimenin anlamını giriniz: ")
                cagrisim_ornek = input("Buraya yardımcı bir cümle gibi metinler girmek isterseniz giriniz yoksa sadece entere basınız:")
                sonuc = motor.kelime_olustur(deste_ismi, kelime, anlam, cagrisim_ornek)
             
                if sonuc == True:
                    print(f"\nBaşarılı: '{kelime}' kelimesi desteye eklendi!")

                else:
                    print("\nHata: Deste bulunamadı veya bu kelime zaten destede var!")

            elif secim == 3:

                print(f"Mevcut Desteler: {list(motor.veriler.keys())}")
                deste_ismi = input("Çalışmak istediğiniz desteyi seçiniz: ")
                sonuc = motor.calisicak_kelimeleri_getir(deste_ismi)

                if len(sonuc) == 0:
                    print("Listede şuan çalışılıcak kelime yok.")
                else:
                    print(f"Çalışmamız gereken {len(sonuc)} kelime var ")

                    for kelime in sonuc:
                        print(f"\nSıradaki kelime: {kelime}")

                        input("Cevabı görmek için entere basın.")

                        anlam = motor.veriler[deste_ismi][kelime]["anlam"]
                        ornek = motor.veriler[deste_ismi][kelime]["cagrisim_ornek"]

                        print(f"Anlamı: {anlam}")
                        print(f"Örnek Cümle: {ornek}")

                        print("\nNe kadar zorlandın?")
                        print("[1] Kolay (4 gün sonra)")
                        print("[2] Orta (1 gün sonra)")
                        print("[3] Zor (10 dakika sonra)")
                        zorluk_secimi = input("Seçiminiz (1/2/3): ")

                        if zorluk_secimi == "1":
                            motor.tekrar_zamani_guncelle(deste_ismi, kelime, "kolay")
                        elif zorluk_secimi == "2":
                            motor.tekrar_zamani_guncelle(deste_ismi, kelime, "orta")
                        elif zorluk_secimi == "3":
                            motor.tekrar_zamani_guncelle(deste_ismi, kelime, "zor")

            elif secim == 4:

                print(f"Mevcut Desteler:{list(motor.veriler.keys())}")
                deste_ismi = input("Silmek istediğiniz destenin ismini giriniz:")
                kelime = input("Silmek istediğiniz kelimeyi seçiniz:")
                sonuc = motor.kelime_sil(deste_ismi, kelime)

                if sonuc == False:
                    print("Böyle bir desteniz yok veya girdiğiniz kelime yok.")
                else:
                    print("işleminiz başarıyla gerçekleştirildi")

            elif secim == 5:

                print(f"Mevcut desteler{list(motor.veriler.keys())}")
                deste_ismi = input("Güncellemek istediğiniz desteyi seçiniz.")
                kelime = input("Güncellemek istediğiniz kelimeyi seçiniz.")
                anlam = input("anlam kısmını değiştirmek isterseniz yazınız yoksa boş bırakınız.") or None
                cagrisim_ornek = input("cagrisim_ornek kısmını değiştirmek isterseniz yazınız yoksa boş bırakınız.") or None
                sonuc = motor.kelime_güncelle(deste_ismi, kelime, anlam, cagrisim_ornek)
                
                if sonuc is False:
                    print("deste ismi yok veya kelime yok.")
                else:
                    print("işleminiz başarıyla gerçekleştirildi")

            elif secim == 6:
                print("Uygulamadan çıkış yapılıyor iyi günler...")
                break
            
            else:
                print("Geçersiz seçim.")
        except KeyboardInterrupt:
            print("Zorla çıkış yapıldı.")
            break
        except ValueError:
            print("Geçersiz giriş. lütfen [1-6] arasında bir sayı girerek tekrar deneyiniz.")
        except Exception as e:
            print(f"Beklenmedik bir hata oluştu{e}.")
            print("Ana menüye dönülüyor.")

if __name__ ==  "__main__":
    ana_menu()

        