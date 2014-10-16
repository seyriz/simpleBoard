from sqlalchemy import Column, Integer, String
from DB import *
import bcrypt

class account(Base):
    __tablename__ = 'account'

    userSrl = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    passwd = Column(String(512), nullable=False)
    email = Column(String(200), nullable=False)

    def __init__(self, email=str(), name=str(), passwd=str()):
            self.passwd = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
            self.name = name
            self.email = email

    def validEmail(email=str()):
        print('E-mail valid')
        validEmail = account.query.filter_by(email=email).first()
        if(validEmail is None):
            print('valid Email')
            return True
        else:
            print('invalid Email')
            return False

    def getValidLogin(email=None, passwd=None):
        getUser = account.query.filter_by(email=email).first()
        PasswdValid = (bcrypt.hashpw(passwd.encode(), getUser.passwd) == getUser.passwd)
        if(getUser.email==email and PasswdValid):
            getUser.passwd = None
            return getUser
        else:
            return None
    
    def getUserInfo(email=str()):
        userInfo = account.query.filter_by(email=email).first()
        return userInfo
    def updatePW(old, new):
        return False
        
class board(Base):
    __tablename__ = 'boards'

    boardSrl = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    board = Column(String)

    def __init__(self, board=str()):
        self.board = board

    def getBoardSrl(boardname=str()):
        qr = board.query.filter_by(board = boardname).first()
        return qr.boardSrl

class post(Base):
    __tablename__ = 'posts'

    postSrl = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    board = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    text = Column(String(2000), nullable=False)
    writer = Column(Integer, nullable=False)
    writeTime = Column(Integer, nullable=False)
    commentCount = Column(Integer, nullable=False)
    files = Column(String)

    def __init__(self, title=str(), text=str(), writer=str(), writeTime=int(), boardname=str(), files=str()):
        boardSrl = board.getBoardSrl(boardname=boardname)
        self.board = boardSrl
        self.title = title
        self.text = text
        self.writer = writer
        self.writeTime = writeTime
        self.commentCount = 0
        self.files = files
    
    def getPostList(limit=20, boardname=str()):
        boardSrl = board.getBoardSrl(boardname=boardname)
        return post.query.filter_by(board=boardSrl).limit(limit).all()

    def getPost(page=int()):
        return post.query.get(page)

class comment(Base):
    __tablename__ = 'comment'

    commentSrl = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    post = Column(Integer, nullable=False)
    comment = Column(String(1000), nullable=False)
    writer = Column(Integer, nullable=False)
    writeTime = Column(Integer, nullable=False)

    def __init__(self,post=int(), comment=str(), writer=str(), writeTime=int()):
        self.comment = comment
        self.writer = writer
        self.writeTime = writeTime
        self.post = post

    def getComment(post):
        return comment.query.filter_by(post = post).order_by(comment.commentSrl).all()

    def getCommentOnce(commentSrl):
        return comment.query.get(commentSrl)