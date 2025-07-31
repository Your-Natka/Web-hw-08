"""MongoEngine моделі для авторів, цитат і тегів"""
# pyright: reportMissingImports=false

from mongoengine import Document, StringField, ReferenceField, ListField


class Tag(Document):
    name = StringField(required=True, unique=True)

    def to_json(self):
        return {"id": str(self.id), "name": self.name}


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

    def to_json(self):
        return {
            "id": str(self.id),
            "fullname": self.fullname,
            "born_date": self.born_date,
            "born_location": self.born_location,
            "description": self.description
        }


class Quote(Document):
    quote = StringField(required=True)
    author = ReferenceField(Author, reverse_delete_rule=2)
    tags = ListField(ReferenceField(Tag))

    def to_json(self):
        return {
            "id": str(self.id),
            "quote": self.quote,
            "author": self.author.to_json() if self.author else None,
            "tags": [tag.to_json() for tag in self.tags]
        }
