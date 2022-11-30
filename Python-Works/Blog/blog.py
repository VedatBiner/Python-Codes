# Kütüphaneleri yükleyelim
from flask import Flask, render_template, flash
from flask import redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField
from wtforms import PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

# Kullanıcı giriş decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın", "danger")
            return redirect(url_for("login"))
    return decorated_function

# Kullanıcı kayıt formu
class RegisterForm(Form): # input alanları
    name = StringField("İsim Soyisim", validators=[validators.Length(min=4, max=25)])
    validators.DataRequired(message = "Lütfen 4 -25 karakter arası isim soy isim giriniz")
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=4, max=35)])
    email = StringField("Email Adresi", validators=[
        validators.Email(message = "Lütfen geçerli bir email adresi giriniz")
    ]) 
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message = "Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname = "confirm", message = "Parolanız uyuşmuyor")
    ])
    confirm = PasswordField("Parola Doğrula")

# Login Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

app = Flask(__name__) # Flask objesi oluşturuyoruz
app.secret_key = "vbblog"
# MySQL bilgilerini verelim
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "vbblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
# MySQL sınıfı oluşturlım.
mysql = MySQL(app)

# makale Formu
class ArticleForm(Form):
    title = StringField("Makale Başlığı", validators=[
        validators.Length(min = 5, max = 100)
    ])
    # alan büyük olacağı için TextAreaField kulalnılıyor
    content = TextAreaField("Makale İçeriği", validators =[
        validators.Length(min = 10)]) 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Makale Sayfası 
@app.route("/articles")
def articles():
    # cursor Oluşturalım
    cursor = mysql.connection.cursor()
    # bütün makaleleri alalım
    sorgu = "SELECT * FROM articles" # tüm makaleri al
    result = cursor.execute(sorgu) # sorguyu çalıştır.
    if result > 0: # Veri tabanında makale var
        # tüm makaleleri sözlük olarak alıyoruz.
        articles = cursor.fetchall()
        return render_template("articles.html", articles = articles)
    else: # Veri yok
        return render_template("articles.html")

@app.route("/article/<string:id>") # article id adresi
def detail(id): # dinamik URL yapısı kuruldu
    return "Article ID : " + id

@app.route("/dashboard") # dashboard sayfası
@login_required # decorator buraya ekelnince kontrol yapılacak
def dashboard():
    # cursor Oluşturalım
    cursor = mysql.connection.cursor()
    # sorgu Oluşturalım
    sorgu = "SELECT * FROM articles WHERE author = %s"
    # sorguyu çalıştıralım
    result = cursor.execute(sorgu, (session["username"],))
    if result > 0: # eğer belli kullanıcı adına makale varsa
        articles = cursor.fetchall()
        return render_template("dashboard.html", articles = articles)
    else:
        return render_template("dashboard.html")

# register işlemi
@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm(request.form) # Form objesi
    if request.method == "POST" and form.validate():
        # Eğermetod POST ise ve Form 'da sıkıntı yoksa
        # veriler MySQL tablosuna girilecek. 
        name = form.name.data # formdan name alındı
        username = form.username.data # formdan username alındı
        email = form.email.data # formdan email adresi alındı
        # parolayı gizleyerek gönderiyoruz.
        password = sha256_crypt.encrypt(form.password.data)
        # veri tabanına erişim için bir cursor oluşturalım
        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)"
        cursor.execute(sorgu, (name, email, username, password)) # tupple göndermek gerekli
        mysql.connection.commit() # veritabanına güncelleme, silme olunca bu işle  zorunlu
        cursor.close() # veri tabanı kapatıldı.
        flash("Başarıyla kayıt oldunuz ...", "success")
        return redirect(url_for("login"))
    else: # oluşturulan formu register.html 'e gönderme
         return render_template("register.html", form = form)

# login işlemi
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        # veri tabanına erişim için bir cursor oluşturalım
        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM users WHERE username = %s"
        # tupple oluşturup, tek eleman için böyle göndermek gerekli
        result = cursor.execute(sorgu, (username,))
        if result > 0: # kullanıcını tüm bilgilerini alalım
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered, real_password):
                # parola doğru ise
                flash("Başarıyla Giriş Yaptınız ...", "success")
                # session başlatmak
                session["logged_in"] = True # giriş yaptığımız için True
                session["username"] = username # giriş yapan kullanıcı adı
                return redirect(url_for("index"))
            else: # parola yanlış ise
                flash("Parolanızı Yanlış girdiniz ...", "danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor !!!", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", form = form)

# Detay Sayfası
# dinamik url yapısı oluşturuluyor
@app.route("/article/<string:id>") # makale id string olarak alınıyor
def article(id): # id fonksiyon çağırılınca otomatik gelecek
    # cursor Oluşturalım
    cursor = mysql.connection.cursor()
    # sorgu oluşturalım
    sorgu = "SELECT * FROM articles WHERE id = %s"
    # sorguyu çalıştıralım
    result = cursor.execute(sorgu, (id,))
    if result > 0:
        article = cursor.fetchone()
        return render_template("article.html", article = article)
    else:
        return render_template("article.html")

# log out işlemi
@app.route("/logout")
def logout():
    session.clear() # session kapatılıyor.
    return redirect(url_for("index")) # ana sayfaya dönüyoruz.

# Makale ekleme
@app.route("/addarticle", methods = ["GET", "POST"])
def addarticle():
    form = ArticleForm(request.form) # Form objesi
    if request.method == "POST" and form.validate():
        # bilgileri alalım
        title = form.title.data
        content = form.content
        cursor = mysql.connection.cursor() # cursor oluşturacağız
        # Sorgu oluşturalım
        sorgu = "INSERT INTO articles (title, author, content) VALUES(%s, %s, %s)"
        # sorgu çalıştıralım
        cursor.execute(sorgu, (title, session["username"], content))
        mysql.connection.commit() # veri tabnına kayıt
        cursor.close() # veri tabanı bağlantısını kes
        flash("Makale başarıyla eklendi.", "success")
        return redirect(url_for("dashboard")) # Dasboard sayfasına dön
    return render_template("addarticle.html", form = form)

if __name__ == "__main__": # local host çalıştırma
    app.run(debug=True) # Hata Mesajlarını açtık

    