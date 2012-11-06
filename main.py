#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from wtforms import form
from database import db_session, init_db
from models import Book, Author

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def index():
    books = Book.query.all()
    authors = Author.query.all()
    page = {'title': 'Libr'}
    return render_template("index.html", **locals())

@app.route("/author/add", methods=["POST"])
def addauthor():
    a = Author(request.form["author_name"])
    db_session.add(a)
    db_session.commit()
    return redirect(url_for("singleauthor", a_id=a.id))

@app.route("/author/<int:a_id>", methods=["GET", "POST", "DELETE"])
def singleauthor(a_id):
    author = Author.query.filter(Author.id == a_id).one()
    if request.method == "GET":
        books = author.books
        page = {'title': author.name}
        return render_template("author.html", **locals())
    elif request.method == "POST":
        author.name = request.form["author_name"]
        db_session.commit()
        return redirect(url_for("singleauthor", a_id=a_id))
    elif request.method == "DELETE":
        db_session.delete(author)
        db_session.commit()
        return url_for("index")

@app.route("/book/add", methods=["POST"])
def addbook():
    b = Book(request.form["book_title"])
    db_session.add(b)
    db_session.commit()
    return redirect(url_for("singlebook", b_id=b.id))

@app.route("/book/<int:b_id>", methods=["GET", "POST", "DELETE"])
def singlebook(b_id):
    book = Book.query.filter(Book.id == b_id).one()
    if request.method == "GET":
        authors = book.authors
        page = {'title': book.title}
        return render_template("book.html", **locals())
    elif request.method == "POST":
        book.title = request.form["book_title"]
        db_session.commit()
        return redirect(url_for("singlebook", b_id=b_id))
    elif request.method == "DELETE":
        db_session.delete(book)
        db_session.commit()
        return url_for("index")

@app.route("/signbook/<int:a_id>/<int:b_id>", methods=["PUT", "DELETE"])
def signbook(a_id, b_id):
    author = Author.query.filter(Author.id == a_id).one()
    if request.method == "PUT":
        author.books.append(Book.query.filter(Book.id == b_id).one())
        db_session.commit()
        return url_for("singleauthor", a_id=author.id)
    elif request.method == "DELETE":
        author.books.remove(Book.query.filter(Book.id == b_id).one())
        db_session.commit()
        return url_for("index")

if __name__ == "__main__":
    app.run()