# -*- coding: utf-8 -*-
import datetime

class Post:
    db = []
    
    @classmethod
    def dball(cls):
        for data in cls.db:
            print(data.title)
            
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.datetime.now()
        Post.db.append(self)
        
    def get(self):
        print("제목: {title}, 내용: {content}".format(
            title = self.title, 
            content = self.content))
    
    def update(self, title=None, content=None):
        self.title = title if title is not None else self.title
        self.content = content if content is not None else self.content
        print("글이 수정되었습니다.")
    
    def __del__(self):
        print("글이 삭제되었습니다.")
    
    #str과 repr 둘 중 어떤걸 쓸 것이냐.
    def __repr__(self):
        return '''
        제목 : {} 
        내용 : {}
        '''.format(self.title, self.content)
        
def main():
    p1 = Post("1번글", "1번제목")
    p2 = Post("2번글", "1번제목")
    p3 = Post("3번글", "1번제목")
    Post.dball()
    # p2 = Post("2번글", "2번제목")
    # p1.get()
    # p2.get()
    # p1.update("1번제목")
    print(p1)

    
if __name__ == "__main__":
    main()