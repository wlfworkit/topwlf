# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
import mysql.connector
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:wlf93958@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# VIP
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.INTEGER, primary_key=True)  # user_id
    name = db.Column(db.String(50), unique=True)
    pwd = db.Column(db.String(15))
    email = db.Column(db.String(30), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.TEXT)
    face = db.Column(db.String(255))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)
    uuid = db.Column(db.String(25), unique=True)
    userlog = db.relationship('Userlog', backref='user')  # yonghu
    comments = db.relationship('Comment', backref='user')  # pinglun foreign key
    moviecols = db.relationship('Moviecol', backref='user')

    def __repr__(self):
        return "<User %r>" % self.name


# vip login log
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)

    def __abs__(self):
        return "<Userlog %r>" % self.id


# tag
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标理
    addtine = db.Column(db.DateTime, index=True, default=datetime.now)
    movies = db.relationship("Movie", backref='tag')  # foreign_key

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablenane__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship("Comment", backref='movie')
    moviecols = db.relationship('Moviecol', backref='movie')  # collection

    def __repr__(self):
        return "<Movie %r>" % self.title


# preview
class Preview(db.Model):
    __tablenane__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Preview %r>" % self.title


# comment
class Comment(db.Model):
    __tablenane__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Comment %r>" % self.id


# collection
class Moviecol(db.Model):
    __tablenane__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# permission
class Auth(db.Model):
    __tablenane__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name


# role
class Rule(db.Model):
    __tablenane__ = "rule"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(500))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Role %r>" % self.name


# administrator
class Admin(db.Model):
    __tablenane__ = "admin"
    id = db.Column(db.INTEGER, primary_key=True)  # user_id
    name = db.Column(db.String(50), unique=True)
    pwd = db.Column(db.String(15))
    is_super = db.Column(db.SmallInteger)  # 0 is super administrator
    role_id = db.Column(db.INTEGER, db.ForeignKey('role.id'))  # own role
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship('Adminlog', backref='admin')  # foreign
    oplogs = db.relationship('Oplog', backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.name


# administrator login log
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.INTEGER, primary_key=True)
    admin_id = db.Column(db.INTEGER, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)

    def __abs__(self):
        return "<Adminlog %r>" % self.id


# operating log
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.INTEGER, primary_key=True)
    admin_id = db.Column(db.INTEGER, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)

    def __abs__(self):
        return "<Oplog %r>" % self.id
if __name__ == "__main__":
    db.create_all()
