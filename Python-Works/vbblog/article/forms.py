from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article # form ile modeli bağlantılı hale getiriyoruz.
        # iki input oluşturacağız. Çünkü tarih ve yazar bilgisi otomatik alınacak
        fields = ["title", "content", "article_image"]
