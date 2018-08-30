# -*- coding: utf-8 -*-
# utf-8 인코딩 코드. 위에 주석이지만 특이하게 이건 먹힌다. 쉬뱅
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import * #model.py load


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///app' #나중에 Mysql쓰면 이부분이 바뀜
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False #트레킹하는건데 메모리 많이 잡아먹어서 꺼둠
db.init_app(app)
migrate = Migrate(app, db) #플라스크 더 편하게 쓰게하는 것


@app.route("/")
def index():
    posts = Post.query.order_by(Post.id.desc()).all()  #최신순 정렬.  #게시글 전부에 관련되기 때문에 복수를 쓴다.
    # sql문 SELECT * FROM posts; 와 같은 문장
    # SELECT * FROM posts ORDER BY id DESC; (디폴트는 ASC)
    
    return render_template("index.html",posts=posts)
    
@app.route("/posts/new")
def new():
        return render_template("new.html")

@app.route("/post", methods=["POST"]) #method가 없다고 나오는데, 이를 해결하기 위해 post를 쓴다고 명시를 해줘야한다.
def create():
    # 사용자로부터 값을 가져와서
    title = request.form.get('title') #argument대신 form을 가져옴 지금은.
    content = request.form.get('content')
    
    # DB에 저장
    post = Post(title=title, content=content) #객체조작하는 것과 동일. =뒤쪽은 model.py에 있는 변수. 게시글 하나를 저장하기 때문에 단수를 씀.
    db.session.add(post) #post 객체를 그대로 받기
    
    # 아래와같은 SQL문을 실행시키는 것과 같다
    # INSERT INTO posts (title, content)
    # VALUES ('1번글', '1번내용')
    db.session.commit()
    return redirect("/")


@app.route("/posts/<int:id>") #variable routing
def read(id):
    # DB에서 특정한 게시글을 가져와!(id값을 기준으로. 인자로 id를 넘겨야함)
    post = Post.query.get(id) #쿼리문. id에 해당하는 것을 가져와서 변수에 담아줘라. Post 클래스의 메소드.
    # SELECT * FROM posts WHERE id=1(특정값);
    
    return render_template("read.html", post=post) #사용자에게 보여주기 위하여 post를 post에 담아서 보내주기.
    
@app.route("/posts/<int:id>/delete")
def delete(id):
    # DB에서 특정 게시글 가져오기
    post = Post.query.get(id)
    # post 오브젝트 삭제하기
    db.session.delete(post)
    db.session.commit()
    #sql문 : DELETE FROM posts WHERE id=2;
    
    return redirect('/') #재요청. 처리하고 해당 페이지로 요청을 보낸다 (@app.route("/"가 실행) #flask에서 import
    
    #return render_template("delete.html", post=post) #delete view 페이지로 넘겨주기. 여기서 index.html이라면 페이지가 "/posts/<int:id>/delete"로 유지

#update는 특정 form값을 받아와야하고, 이걸 수정해야한다.
@app.route("/posts/<int:id>/edit") #get 요청
def edit(id):
    post = Post.query.get(id)
    
    return render_template("edit.html", post=post)


@app.route("/posts/<int:id>/update", methods=["POST"]) #post요청
def update(id):
    post = Post.query.get(id)
    
    post.title = request.form.get("title")
    post.content = request.form.get("content")
    db.session.commit()
    return redirect("/posts/{}".format(post.id))
    
    # UPDATE posts SET title = "hihi"
    # WHERE id = 2;
    # UPDATE posts SET title = "hihi"
    # WHERE id=2;

# -> 타이틀이 1인거 필터
# Post.query.filter_by(title = "1").all()
# SELECT * FROM posts
# WHERE title = '1';

# -> 해당사항에 대한 개수 count
# Post.query.filter_By(title="1").count()
# SELECT COUNT(*) FROM posts
# WHERE title = '1';

# -> 타이틀이 1인거 하나만 필터
# Post.query.filter_by(title = "1").first()
# SELECT * FROM posts
# WHERE title = '1' LIMIT 1;

#  -> 1 아닌것만 필터
# Post.query.filter(Post.title != "1").all()
# SELECT * FROM posts
# WHERE title != '1';

#  -> 1이라는 글자가 들어간 것만 출력
# Post.query.filter(Post.title.like("%1%")).all()
# SELECT * FROM posts
# WHERE title LIKE '%1%';

#  -> 제목과 내용이 1인 글 필터
# from sqlalchemy import and_, or_
# Post.query.filter(and_(Post.title == "1", Post.content == "1")).all()                                                                           
# SELECT * FROM posts
# WHERE title = "1" AND content = "1";

