# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy() #SQLAlchemy 오브젝트(객체)를 생성해준다. 마치 app에다가 담아줬던 것처럼

class Post(db.Model): #약속이기 때문에 이건..
    __tablename__ = "posts"  # 객체와 데이터베이스간의 매핑.(ORM)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    comments = db.relationship("Comment", backref = "post") #comments는 한 게시판에 댓글이 1:다 / post는 하나에 걸리기 때문에.. 단 복수 주의
    # 보통 sql에서는 관계가 있다라는 것을 알려줘야한다.(relation) back reference..
    
    def __init__(self, title, content): #생성자 만들기
        self.title = title
        self.content = content
        self.created_at = datetime.datetime.now()

#sql문. 이걸 안써도 위에 명령어로 이와 같은 명령어가 실행된다.
# CREATE TABLE post(
#     id = SERIAL PRIMARY KEY,
#     title VARCHAR,
#     content TEXT,
#     created_at DATETIME
#     )
    

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    
    #FK
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable = False)
    def __init__(self, content):
        self.content = content
        self.created_at = datetime.datetime.now()