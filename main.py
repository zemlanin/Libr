#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from forms import BookForm, AuthorForm, AuthorshipForm, SearchForm
from database import db_session
from models import Book, Author

DEBUG = True

app = Flask(__name__, static_path='/static', static_url_path='/static', static_folder='static')
app.config.from_object(__name__)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def index():
    books = Book.query.all()
    authors = Author.query.all()
    forms = {
        'book': BookForm(),
        'author': AuthorForm(),
        'search': SearchForm()
    }
    page = {'title': 'Libr'}
    return render_template("index.html", **locals()) # I REGRET NOTHING

@app.route("/author/add", methods=["POST"])
def addauthor():
    form = AuthorForm(request.form)
    if form.validate():
        a = Author(form.name.data)
        db_session.add(a)
        db_session.commit()
        return redirect(url_for("singleauthor", a_id=a.id))
    else:
        return redirect(url_for("index"))

@app.route("/author/<int:a_id>", methods=["GET", "POST", "DELETE"])
def singleauthor(a_id):
    author = Author.query.filter(Author.id == a_id).one()
    if request.method == "GET":
        books = author.books
        page = {'title': author.name}
        forms = {
            'author': AuthorForm(),
            'book': BookForm(),
            'authorship': AuthorshipForm(),
            'search': SearchForm()
        }
        forms['authorship'].books.choices = [(b.id, b.title) for b in Book.query.all()]
        return render_template("author.html", **locals())
    elif request.method == "POST":
        author.name = request.form["name"]
        db_session.commit()
        return redirect(url_for("singleauthor", a_id=a_id)) # либо рендерить?..
    elif request.method == "DELETE":
        db_session.delete(author)
        db_session.commit()
        return url_for("index")

@app.route("/book/add", methods=["POST"])
def addbook():
    b = Book(request.form["title"])
    db_session.add(b)
    db_session.commit()
    return redirect(url_for("singlebook", b_id=b.id))

@app.route("/book/<int:b_id>", methods=["GET", "POST", "DELETE"])
def singlebook(b_id):
    book = Book.query.filter(Book.id == b_id).one()
    if request.method == "GET":
        authors = book.authors
        page = {'title': book.title}
        forms = {
            'book': BookForm(),
            'search': SearchForm()
        }
        return render_template("book.html", **locals())
    elif request.method == "POST":
        book.title = request.form["title"]
        db_session.commit()
        return redirect(url_for("singlebook", b_id=b_id))
    elif request.method == "DELETE":
        db_session.delete(book)
        db_session.commit()
        return url_for("index")

@app.route("/author/<int:a_id>/sign", methods=["POST"])
def signbook(a_id):
    author = Author.query.filter(Author.id == a_id).one()
    b_ids = request.form.getlist('books')
    books = Book.query.filter(Book.id.in_(b_ids)).all()
    for b in books:
        author.books.append(b)
    db_session.commit()
    return redirect(url_for("singleauthor", a_id=a_id))

# Да, лучше бы было DELETE, но форму с ним не засабмитить нормально
@app.route("/author/<int:a_id>/unsign/<int:b_id>", methods=["POST"])
def unsignbook(a_id, b_id):
    author = Author.query.filter(Author.id == a_id).one()
    author.books.remove(Book.query.filter(Book.id == b_id).one())
    db_session.commit()
    return url_for("singleauthor", a_id=a_id)

@app.route("/search", methods=["POST"])
def search():
    query = request.form['query']
    authors = Author.query.filter(Author.name.like('%'+query+'%')).all()
    books = Book.query.filter(Book.title.like('%'+query+'%')).all()
    page = {'title': 'Search: '+query}
    forms = {'search': SearchForm()}
    return render_template("search.html", **locals())

if __name__ == "__main__":
    app.run()