# kütüphanelerimiz
import sqlite3
import time

# Kitap sınıfı
class Kitap():

    def __init__(self, isim, yazar, yayinevi, tur, baski):
        self.isim = isim 
        self.yazar = yazar 
        self.yayinevi = yayinevi
        self.tur = tur 
        self.baski = baski

    def __str__(self):
        return "Kitap İsmi : {}\nYazar : {}\nYayınevi : {}\nTür : {}\nBaskı : {}\n".format(self.isim, self.yazar, self.yayinevi, self.tur, self.baski)

# Kütüphane sınıfı
class Kutuphane():

    def __init__(self):
        self.baglanti_olustur()

    # bağlantımızı ve tablomuzu oluşturalım.
    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("kutuphane.db")
        self.cursor = self.baglanti.cursor()
        sorgu = "CREATE TABLE IF NOT EXISTS kitaplar (isim TEXT, yazar TEXT, yayinevi TEXT, tur TEXT, baski INT)"
        self.cursor.execute(sorgu)
        self.baglanti.commit()

    # Bağlantıyı keselim
    def baglantiyi_kes(self): 
        self.baglanti.close()

    # Kitap listesini görelim
    def kitaplari_goster(self):
        sorgu = "SELECT * FROM kitaplar"
        self.cursor.execute(sorgu)
        kitaplar = self.cursor.fetchall()
        if (len(kitaplar) == 0): 
            print("Kütüphanede kitap bulunmuyor")
        else: 
            for i in kitaplar: 
                # Kitap objesi 
                kitap = Kitap(i[0], i[1], i[2], i[3], i[4])
                print(kitap)
    
    # Kitap sorgulama
    def kitap_sorgula(self, isim):
        sorgu = "SELECT * FROM kitaplar WHERE isim = ?"
        self.cursor.execute(sorgu, (isim,))
        kitaplar = self.cursor.fetchall()
        if (len(kitaplar) == 0):
            print("Böyle bir kitap bulunmuyor ...")
        else:
            kitap = Kitap(kitaplar[0][0], kitaplar[0][1], kitaplar[0][2], kitaplar[0][3], kitaplar[0][4])
            print(kitap)

    # Kitap ekleme
    def kitap_ekle(self, kitap):
        sorgu = "INSERT INTO kitaplar VALUES(?, ?, ?, ?, ?)"
        self.cursor.execute(sorgu, (kitap.isim, kitap.yazar, kitap.yayinevi, kitap.tur, kitap.baski))
        self.baglanti.commit() # bilgileri güncelle

    # Kitap silme
    def kitap_sil(self, isim):
        sorgu = "DELETE FROM kitaplar WHERE isim = ?"
        self.cursor.execute(sorgu, (isim,))
        self.baglanti.commit()

    # baskı sayısı arttıralım
    def baski_yukselt(self, isim): 
        sorgu = "SELECT * FROM kitaplar WHERE isim = ?"
        self.cursor.execute(sorgu, (isim,))
        kitaplar = self.cursor.fetchall()
        if (len(kitaplar) == 0): 
            print("Böyle bir kitap bulunmuyor")
        else: 
            baski = kitaplar[0][4]
            baski += 1
            sorgu2 = "UPDATE kitaplar set baski = ? WHERE isim = ?"
            self.cursor.execute(sorgu2, (baski, isim))
            self.baglanti.commit()

# sqlite bağlantısı kuralım
# dosya yoksa oluşturacak ve bağlanacak.
def dosya_ac():
    con = sqlite3.connect("kutuphane.db")
    cursor = con.cursor() # imleç oluşturduk.