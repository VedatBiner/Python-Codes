from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Article, Comment
from .forms import ArticleForm

# Create your views here.
# her view fonksiyonunda ilk parametre olarak request bulunmalıdır.

def articles(request): # Makaleler fonksiyonu
    keyword = request.GET.get("keyword") # arama değerini al
    
    if keyword: # arama düğmesine basıldı mı?
        # keyword 'un geçtiği article 'ları getir
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", {"articles" : articles})

    articles = Article.objects.all() # tüm makaleleri al
    return render(request, "articles.html", {"articles" : articles})

def index(request): # Anasayfa için fonksiyon
    return render(request, "index.html")

def about(request): # about için fonksiyon
    return render(request, "about.html")

@login_required(login_url = "user:login")
def dashboard(request): # Kontrol Paneli için fonk.
    # Giriş yapmış olan kullanıcının makalelerini alalım
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request, "dashboard.html", context)

@login_required(login_url = "user:login")
def addArticle(request): # addArticle fonk.
    form = ArticleForm(request.POST or None, request.FILES or None) # obje oluşturalım
    if form .is_valid(): # fomda bir sorun yoksa
        article = form.save(commit=False) # obje olarak formu dönelim
        article.author = request.user # giriş yapan kullanıcı hesabı
        article.save() # veri tabanına kayıt yapılır.
        messages.success(request, "Makale başarıyla oluşturuldu ...")
        print("Article eklendi : ", article) # silinebilir
        return redirect("article:dashboard")
    # sözlük olarak gönderiyoruz
    return render(request, "addArticle.html", {"form" : form})

def detail(request, id): # dinamik id alıyoruz
    # sorgumuzu yazıyoruz, gördüğü ilk article 'ı döndür
    # article = Article.objects.filter(id = id).first() 
    # article varsa gelecek yoksa 404 sayfası gelecek
    article = get_object_or_404(Article, id = id)
    # comment saklayacak listemiz
    comments = article.comments.all()
    return render(request, "detail.html", {"article" : article, "comments" : comments})

@login_required(login_url = "user:login")
def updateArticle(request, id): # güncelleme fonksiyonu, dinamik URL
    article = get_object_or_404(Article, id = id) # linkteki id alalım
    # article içindeki bilgiler ile formu oluşturalım.
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)
    if form.is_valid(): # formda sorun yoksa
        article = form.save(commit=False) # obje olarak formu dönelim
        article.author = request.user # giriş yapan kullanıcı hesabı
        article.save() # veri tabanına kayıt yapılır.
        messages.success(request, "Makale başarıyla güncellendi ...")
        return redirect("article:dashboard")
    return render(request, "update.html", {"form" : form})

@login_required(login_url = "user:login")
def deleteArticle(request, id): # silme fonksiyonu, dinamik URL
    article = get_object_or_404(Article, id = id)
    article.delete() # veri tabanından silme
    messages.success(request,"Makale başarıyla silindi ...")
    return redirect("article:dashboard")

@login_required(login_url = "user:login")
def addComment(request, id): 
    # post request'in id'ye göre alınması gerekiyor.
    article = get_object_or_404(Article, id = id)
    # POST mu GET mi kontrol edelim
    if request.method == "POST": # POST ise,
        # input ve textarea name bilgilerini alalım.
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        # comment modelinden obje oluşturlım
        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save() # comment tablosuna ekleyelim
    # burada url yönlendirmesini reverse fonk. ile yapıyoruz
    return redirect(reverse("article:detail", kwargs = {"id" : id}))
