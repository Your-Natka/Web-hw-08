"""Скрипт для імпорту JSON-даних у MongoDB"""

import json
from mongoengine import connect
from db.models import Author, Quote, Tag


def load_json(filename):
    """Завантажити дані з JSON-файлу"""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def seed_authors():
    """Завантажити авторів у базу"""
    data = load_json("data/authors.json")
    for author_data in data:
        author = Author(**author_data)
        author.save()


def seed_quotes():
    """Завантажити цитати та теги у базу"""
    data = load_json("data/qoutes.json")
    for quote_data in data:
        tags = []
        for tag_name in quote_data.get("tags", []):
            tag = Tag.objects(name=tag_name).first()  # pylint: disable=no-member
            if not tag:
                tag = Tag(name=tag_name)
                tag.save()
            tags.append(tag)
        author = Author.objects(fullname=quote_data["author"]).first()  # pylint: disable=no-member
        if author:
            quote = Quote(
                quote=quote_data["quote"],
                author=author,
                tags=tags
            )
            quote.save()


if __name__ == "__main__":
    connect(
        db="quotes_db",
        host="mongodb+srv://<your-connection-string>",
        alias="default"
    )

    seed_authors()
    seed_quotes()
    print("✅ Дані успішно імпортовано.")

