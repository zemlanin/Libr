#-*- coding: utf-8 -*-
from wtforms import Form, BooleanField, TextField, SelectMultipleField, \
    SubmitField, validators

class AuthorForm(Form):
    name = TextField('Name', [validators.Length(min=2)])

class BookForm(Form):
    title = TextField('Title', [validators.Length(min=2)])

class AuthorshipForm(Form):
    books = SelectMultipleField('Authors', coerce=int)

class SearchForm(Form):
    query = TextField('Query')