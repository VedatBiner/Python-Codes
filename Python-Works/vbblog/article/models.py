from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

# tablo yapımızı class halinde oluşturalım.
class Article(models.Model):
    # Django 'nun users yapısını referans alıyor. user silinirse,
    # ilşkili olan herşey de siliniyor.
    author = models.ForeignKey("auth.user", on_delete=models.CASCADE, verbose_name="Yazar")
    title = models.CharField(max_length=50, verbose_name="Başlık") # başlığımız 50 karakter
    # content = models.TextField(verbose_name="İçerik") # içerik
    content = RichTextField() # ck editördeki RichTet özelliğini kullanıyoruz.
    # otomatik alınacak ekleme tarihi (eklenme zamanı)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi") 
    # imaj eklenirse
    article_image = models.FileField(blank = True, null = True, verbose_name="Makaleye Fotoğraf Ekleyin")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_date'] # son eklenen makale ilk gösterilecek

# comment modeli
class Comment(models.Model):
    # articel ile comment 'i bağlantılı hale getirelim.
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Makale", related_name="comments")
    # comment yazarı
    comment_author = models.CharField(max_length = 50, verbose_name="İsim")
    # comment içeriği
    comment_content = models.CharField(max_length = 200, verbose_name="Yorum")
    # comment tarihi
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date'] # son eklenen yorum ilk gösterilecek
        

