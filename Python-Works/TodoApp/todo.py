# Kütüphanelerimiz
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# bu üç satır her zaman olacak
# veri tabanımızı tam adresi ile ekleyelim.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////DATA/VEDAT/Python-Codes/denemeler/TodoApp/todo.db"
db = SQLAlchemy(app)

@app.route("/") # ana sayfa
def index():
    todos = Todo.query.all() # veri tabanndan tabloyu çek (liste dönecek)
    return render_template("index.html", todos = todos)

@app.route("/complete/<string:id>") # dinamik URL adresi oluşturalım
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first() # id alalım
    todo.complete = not todo.complete # True ise False, False ise True yapıyoruz
    db.session.commit() # Veri tabanına yaz
    return redirect(url_for("index")) # ana sayfaya git

@app.route("/add", methods=["POST"]) # ekleme sayfası
def addTodo():
    title = request.form.get("title") # title Aldık
    newTodo = Todo(title = title, complete = False) # obje oluşturalım
    db.session.add(newTodo) # objemizi veri tabanına ekleyelim.
    db.session.commit() # veri tabanına yazalım
    return redirect(url_for("index")) # ana sayfaya dönelim

@app.route("/delete/<string:id>") # silme sayfası
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo) # silme işlemi
    db.session.commit() # veri tabanına yazalım
    return redirect(url_for("index"))

# tablo class 
class Todo(db.Model): # model yapısı ORM içinden geliyor
    id = db.Column(db.Integer, primary_key=True) # auto increment ve PRIMARY_KEY
    title = db.Column(db.String(80)) # max. 80 karakter
    complete = db.Column(db.Boolean) # Başlangıçta False değeri alacak

# server 'ı ayağa kaldıralım
if __name__ == "__main__":
    with app.app_context():
        db.create_all() # tabloyu ekleyelim. Sadece bir tablo oluşuyor.
    app.run(debug = True)


