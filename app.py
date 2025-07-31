"""Flask API для отримання авторів, тегів та цитат"""

from flask import Flask, jsonify
from mongoengine import connect
from db.models import Author, Quote, Tag

app = Flask(__name__)

connect(
    db="quotes_db",
    host="mongodb+srv://<your-connection-string>",
    alias="default"
)


@app.route("/authors")
def get_authors():
    """Отримати список авторів"""
    authors = Author.objects()  # pylint: disable=no-member
    return jsonify([author.to_json() for author in authors])


@app.route("/tags")
def get_tags():
    """Отримати список тегів"""
    tags = Tag.objects()  # pylint: disable=no-member
    return jsonify([tag.to_json() for tag in tags])


@app.route("/quotes")
def get_quotes():
    """Отримати список цитат"""
    quotes = Quote.objects()  # pylint: disable=no-member
    return jsonify([quote.to_json() for quote in quotes])


if __name__ == "__main__":
    app.run(debug=True)

