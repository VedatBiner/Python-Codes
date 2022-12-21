# Kitapyurdu scrap örneği
# Kodda bir hata var bulmadım. txt dosyası oluşmuyor?
# json dosyası oluşuyor ama.
import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    page_count = 0
    book_count = 1
    file = open("books.txt", "a", encoding = "UTF-8") # dosyayı bir kez açalım.
    start_urls = [
        # ilk request bu sayfa
        'https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=16&filter_in_stock=1&filter_in_stock=1&page=1'
    ]

    def parse(self, response):
        book_names = response.css("div.name.ellipsis a span::text").extract() 
        book_authors = response.css("div.author span a span::text").extract() 
        book_publishers = response.css("div.publisher span a span::text").extract()
        i = 0
        # 20 kitabın bilgisini alalım
        while (i < len(book_names)) :
            """
            # json dosya oluşturmak  için gerekli
            yield {
                "name" : book_names[i],
                "author" : book_authors[i],
                "publisher : " : book_publishers[i]
            }
            """
            self.file.write("---------------------------------------------------------\n")
            self.file.write(str(self.book_count)) + ".\n" # kitap no
            self.file.write("Kitap İsmi : " + book_names[i] + "\n") # Kitap Adı
            self.file.write("Yazar : " + book_authors[i] + "\n") # Kitap yazarı
            self.file.write("Yayınevi : " + book_publishers[i] + "\n") # Kitap yayınevi
            self.file.write("---------------------------------------------------------\n")
            self.book_count += 1
            i += 1
        next_url = response.css("a.next::attr(href)").extract_first()
        self.page_count += 1 
        # bir sonra url var mı?
        if next_url is not None and self.page_count != 5:
            yield scrapy.Request(url = next_url, callback = self.parse)
        else:
            self.file.close() # dosyayı kapatalım
