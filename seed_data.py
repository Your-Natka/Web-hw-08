import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Author, Quote, Tag
from db.base import Base

engine = create_engine("postgresql+psycopg2://user:password@localhost:5432/dbname")  # Замінити на свої
Session = sessionmaker(bind=engine)
session = Session()

def load_authors():
    with open("data/authors.json", encoding="utf-8") as f:
        authors = json.load(f)
        for item in authors:
            author = Author(
                fullname=item["fullname"],
                born_date=item["born_date"],
                born_location=item["born_location"],
                description=item["description"]
            )
            session.add(author)
        session.commit()

def load_quotes():
    with open("data/qoutes.json", encoding="utf-8") as f:
        quotes = json.load(f)
        for item in quotes:
            author = session.query(Author).filter_by(fullname=item["author"]).first()
            if not author:
                continue
            quote = Quote(quote=item["quote"], author=author)

            for tag_name in item["tags"]:
                tag = session.query(Tag).filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                quote.tags.append(tag)

            session.add(quote)
        session.commit()

if __name__ == "__main__":
    load_authors()
    load_quotes()
