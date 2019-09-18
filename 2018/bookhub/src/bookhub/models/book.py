import datetime
from bookhub import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    img = db.Column(db.String(256))
    description = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Book %r>' % self.title
