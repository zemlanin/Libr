from wtforms import Form, BooleanField, TextField, SelectMultipleField, \
    SubmitField, validators

class AuthorForm(Form):
    name = TextField('Name')

class BookForm(Form):
    title = TextField('Title')

class AuthorshipForm(Form):
    books = SelectMultipleField('Authors', coerce=int)

class SearchForm(Form):
    query = TextField('Query')