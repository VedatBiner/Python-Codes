# Ekşi sözlük içinde bir maddeyi içinde geçen sayfalarda aratıp,
# rasgele 10 sayfadaki 10 başlığı bir dosyaya yazdıran kod
# kütüphanelerimizi alalım
from selenium import webdriver
import random
import time

browser = webdriver.Chrome() # chrome browser oluşturduk
# gitmek istediğimiz url
url = "https://eksisozluk.com/mustafa-kemal-ataturk--34712?p="
pageCount = 1 # sayfa sayacı
entries = [] # entry listesi
entryCount = 1

while pageCount <= 10:
    randomPage = random.randint(1, 2551) # rasgele sayfa no alıyoruz
    newUrl = url + str(randomPage) # sayfa no ya göre url oluşturduk
    browser.get(newUrl)
    elements = browser.find_elements("css selector", ".content") 
    for element in elements:
        entries.append(element.text) # entries listeye eklenir.
    time.sleep(3)
    pageCount += 1
    # dosyaya yazdıralım

with open("entries.txt","w", encoding = "UTF-8") as file:
        for entry in entries:
            file.write(str(entryCount)+".\n" + entry +"\n")
            file.write("*" * 60 + "\n")
            entryCount += 1

browser.close() # browser'ı kapat
