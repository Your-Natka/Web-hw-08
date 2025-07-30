from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from db.base import Base

# Таблиця зв'язку (багато-до-багатьох)
quote_tag = Table(
    'quote_tag', Base.metadata,
    Column('quote_id', ForeignKey('quotes.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    fullname = Column(String(255), nullable=False, unique=True)
    born_date = Column(String(255))
    born_location = Column(String(255))
    description = Column(Text)

    quotes = relationship('Quote', back_populates='author')

class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    quote = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship('Author', back_populates='quotes')
    tags = relationship('Tag', secondary=quote_tag, back_populates='quotes')

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    quotes = relationship('Quote', secondary=quote_tag, back_populates='tags')
