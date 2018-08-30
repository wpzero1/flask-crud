from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import * #model.py 불러오기

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///app' #나중에 Mysql쓰면 이부분이 바뀜
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False #트레킹하는건데 메모리 많이 잡아먹어서 꺼둠
db.init_app(app)
migrate = Migrate(app, db) #플라스크 더 편하게 쓰게하는 것


@app.route("/")
def index():
    posts = Post.query.all()
    #sql문 SELECT * FROM posts 와 같은 문장
    
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
    Post(title=title, content=content) #객체조작하는 것과 동일. =뒤쪽은 model.py에 있는 변수
    db.session.add(post) #post 객체를 그대로 받기
    
    # 아래와같은 SQL문을 실행시키는 것과 같다
    # INSERT INTO posts (title, content)
    # VALUES ('1번글', '1번내용')
    db.session.commit()
    return render_template("create.html", post=post)
    
