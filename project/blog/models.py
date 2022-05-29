from datetime import datetime

from project import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)
    author_id = db.Column(
        db.Integer(), db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "<Post:{}>".format(self.text[:10])
