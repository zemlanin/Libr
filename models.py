from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

ab_table = Table('association', Base.metadata,
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)

    def __init__(self, title=None):
        self.title = title

    def __repr__(self):
        return '<Book %r>' % (self.title)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    books = relationship("Book",
                    secondary=ab_table,
                    backref="authors")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Author %r>' % (self.name)