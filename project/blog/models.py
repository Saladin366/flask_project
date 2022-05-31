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
    favorites = db.relationship(
        'Favorite', backref='post', cascade='all,delete-orphan')
    comments = db.relationship(
        'Comment', backref='post', cascade='all,delete-orphan')

    def __repr__(self):
        return "<Post:{}>".format(self.text[:10])


class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(), db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(
        db.Integer(), db.ForeignKey('posts.id'), nullable=False)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(
        db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)
    author_id = db.Column(
        db.Integer(), db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(
        db.Integer(), db.ForeignKey('posts.id'), nullable=False)

    def __repr__(self):
        return "<Comment:{}>".format(self.text[:10])
