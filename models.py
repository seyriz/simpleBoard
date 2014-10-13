from sqlalchemy import Column, Integer, String
from DB import Base

class account(Base):
    __tablename__ = 'account'

    userSrl = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    passwd = Column(String(512), nullable=False)
    email = Column(String(200), nullable=False)

    def __init__(self, email=str(), name=str(), passwd=str()):
        self.passwd = passwd
        self.name = name
        self.email = email

    def validEmail(email=None):
        print('E-mail valid')
        validEmail = account.query.filter_by(email = email).first()
        if(validEmail is None):
            print('valid Email')
            return True
        else:
            print('invalid Email')
            return False

    def getValidLogin(email=None, passwd=None):
        getUser = account.query.filter_by(email = email).first()
        if(getUser==None):
            return False
        elif(getUser.email==email and getUser.passwd==passwd):
            return True
        else:
            False
    
    def getUserInfo(email=str()):
        userInfo = account.query.filter_by(email=email).first()
        return userInfo
    def updatePW(old, new):
        return False


class post(Base):
    __tablename__ = 'posts'

    postSrl = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(200), nullable=False)
    text = Column(String(2000), nullable=False)
    writer = Column(Integer, nullable=False)
    writeTime = Column(Integer, nullable=False)
    files = Column(String)

    def __init__(self, title=str(), text=str(), writer=str(), writeTime=int(), files=None):
        self.title = title
        self.text = text
        self.writer = writer
        self.writeTime = writeTime
        self.files = files
    
    def getPostList(offset=int(), limit=20):
        return post.query.offset(offset).limit(limit).all()

    def getPost(page):
        return post.query.filter_by(postSrl=page).first()

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

class files(Base):
    __tablename__ = 'files'

    fileSrl = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    fileName = Column(String(500), nullable=False)
    fileUploaded = Column(Integer, nullable=False)
    fileExtention = Column(String(10), nullable=False)
    fileSaved = Column(String(10000), nullable=False)

    def __init__(self, fileName=str(), fileUploaded=int(), fileExtention=str(), fileSaved=str()):
        self.post = post
        self.fileName = fileName
        self.fileUploaded = fileUploaded
        self.fileExtention = fileExtention
        self.fileSaved = fileSaved

    def getFileLoc(fileSrl):
        fileList = files.query.filter_by(fileSrl = fileSrl).first()
        entry = list()
        for item in fileList:
            temp = {'fileSrl': item[0], 'post': item[1], 'fileName': item[2], 'fileUploaded': item[3], 'fileExtention': item[4], 'fileSaved': item[5]}
            entry.appent(temp)
        return entry

    def getLatestFile():
        latestFile = file.query.limit(1).first()
        return latestFile.fileSrl