from motor import TiCardMotoru

def ana_menu():
    motor = TiCardMotoru()
    print("TiCard Kelime Ö?renme Sistemine Ho? Geldiniz!")

    while True:
        try:
            print("[1] Deste Olu?tur\t[2] Kelime Ekle\t[3] Çal??maya Ba?la\t[4] Kelime Sil\t[5] Kelime Güncelle\t[6] Ç?k?? ")
            secim = int(input("Yapmak ?stedi?iniz ??lemi Seçiniz: "))

            if secim == 1:

                deste_ismi = input("Desteye vermek istedi?iniz metni giriniz: ")
                sonuc = motor.deste_olustur(deste_ismi)
                if sonuc == True:
                    print("Desteniz ba?ar?yla olu?turuldu")
                else:
                    print("Zaten bu adda bir deste var")
            
            elif secim == 2:

                print(f"Mevcut desteler: {list(motor.veriler.keys())}")
                deste_ismi = input("??lemini yapmak istedi?iniz destenin ad?n? giriniz: ")
                kelime = input("Girmek istedi?iniz kelimeyi seçiniz: ")
                anlam = input("Girdi?iniz kelimenin anlam?n? giriniz: ")
                cagrisim_ornek = input("Buraya yard?mc? bir cümle gibi metinler girmek isterseniz giriniz yoksa sadece entere bas?n?z:")
                sonuc = motor.kelime_olustur(deste_ismi, kelime, anlam, cagrisim_ornek)
             
                if sonuc == True:
                    print(f"\nBa?ar?l?: '{kelime}' kelimesi desteye eklendi!")

                else:
                    print("\nHata: Deste bulunamad? veya bu kelime zaten destede var!")

            elif secim == 3:

                print(f"Mevcut Desteler: {list(motor.veriler.keys())}")
                deste_ismi = input("Çal??mak istedi?iniz desteyi seçiniz: ")
                sonuc = motor.calisicak_kelimeleri_getir(deste_ismi)

                if len(sonuc) == 0:
                    print("Listede ?uan çal???l?cak kelime yok.")
                else:
                    print(f"Çal??mam?z gereken {len(sonuc)} kelime var ")

                    for kelime in sonuc:
                        print(f"\nS?radaki kelime: {kelime}")

                        input("Cevab? görmek için entere bas?n.")

                        anlam = motor.veriler[deste_ismi][kelime]["anlam"]
                        ornek = motor.veriler[deste_ismi][kelime]["cagrisim_ornek"]

                        print(f"Anlam?: {anlam}")
                        print(f"Örnek Cümle: {ornek}")

                        print("\nNe kadar zorland?n?")
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
                deste_ismi = input("Silmek istedi?iniz destenin ismini giriniz:")
                kelime = input("Silmek istedi?iniz kelimeyi seçiniz:")
                sonuc = motor.kelime_sil(deste_ismi, kelime)

                if sonuc == False:
                    print("Böyle bir desteniz yok veya girdi?iniz kelime yok.")
                else:
                    print("i?leminiz ba?ar?yla gerçekle?tirildi")

            elif secim == 5:

                print(f"Mevcut desteler{list(motor.veriler.keys())}")
                deste_ismi = input("Güncellemek istedi?iniz desteyi seçiniz.")
                kelime = input("Güncellemek istedi?iniz kelimeyi seçiniz.")
                anlam = input("anlam k?sm?n? de?i?tirmek isterseniz yaz?n?z yoksa bo? b?rak?n?z.") or None
                cagrisim_ornek = input("cagrisim_ornek k?sm?n? de?i?tirmek isterseniz yaz?n?z yoksa bo? b?rak?n?z.") or None
                sonuc = motor.kelime_güncelle(deste_ismi, kelime, anlam, cagrisim_ornek)
                
                if sonuc is False:
                    print("deste ismi yok veya kelime yok.")
                else:
                    print("i?leminiz ba?ar?yla gerçekle?tirildi")

            elif secim == 6:
                print("Uygulamadan ç?k?? yap?l?yor iyi günler...")
                break
        except KeyboardInterrupt:
            print("Zorla ç?k?? yap?ld?.")
            break
        except ValueError:
            print("Geçersiz giri?. lütfen [1-6] aras?nda bir say? girerek tekrar deneyiniz.")
        except Exception as e:
            print(f"Beklenmedik bir hata olu?tu{e}.")
            print("Ana menüye dönülüyor.")

if __name__ ==  "__main__":
    ana_menu()

        