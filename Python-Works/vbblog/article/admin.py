from django.contrib import admin
from .models import Article, Comment # article ve comment 'i alalım

# Register your models here.
admin.site.register(Comment) # kaydedelim
@admin.register(Article) # admin paneline kayıt
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date"] # sütun başlıkları ile listeleme
    list_display_links = ["title", "created_date"] # istenen seçeneğe göre link verme
    search_fields = ["title"] # istediğimiz bilgiye göre arama
    list_filter = ["created_date"] # belli özelliğe göre filtreleme
    class Meta: # ArticleAdmin ile Article 'ı bağlamak için
        model = Article

