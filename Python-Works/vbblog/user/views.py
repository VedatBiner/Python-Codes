from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def register(request): # register user
    form = RegisterForm(request.POST or None)  # obje oluştur. Boş form oluşur
    if form.is_valid(): # clean metodu çağırılıyor. POST request ise
        # usernme ve password alanını alalım
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        # user oluşturalım
        newUser = User(username = username)
        newUser.set_password(password)
        # user kaydedelim. Kullanıcımız veri tabanına kaydediliyor.
        newUser.save()
        # user 'ın sisteme girmesi
        login(request, newUser)
        messages.info(request, "Başarıyla kayıt oldunuz ...") # mesaj yayınlayalım
        # ana sayfaya gidiş
        return redirect("index")
    # GET request ise
    context = {
        "form" : form
    }
    return render(request, "register.html", context)

def loginUser(request): # login func.
    form = LoginForm(request.POST or None)
    context = {
        "form" : form
    }
    # Burada clean() fonksiyonu için bir override işlemi yapmıyoruz.
    if form.is_valid(): # formda sorun yoksa,
        # kullanıcı bilgilerini alalım
        username = form.cleaned_data.get("username")
        password = form = form.cleaned_data.get("password")
        # kullanıcı ver tabanında var mı ? yok mu?
        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, "Kullanıcı adı veya parola Hatalı ...")
            return render(request, "login.html", context)
        messages.success(request, "Başarıyla giriş yaptınız")
        login(request, user) # sisteme giriş yapılıyor
        return redirect("index") # ana sayfaya dön
    return render(request, "login.html", context)

def logoutUser(request): # logut func.
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız ...")
    return redirect("index") # ana sayfaya dönülür
