from flask import *
from models import *
from DB import db_session
import time, os, misaka
class simpleBoard:
    

    simpleBBS = Blueprint('simpleBBS', __name__, template_folder='template/simpleBoard')

    @simpleBBS.route('/', defaults={'page':1})
    @simpleBBS.route('/<int:page>')
    def postRead(page=1):
        getPost = post.getPost(page)
        if(page<=10):
            getPostListPrev = post.getPostList(offset=0, limit=int(page)-1)
            getPostListNext = post.getPostList(offset=int(page), limit=20-int(page))
        else:
            getPostListPrev = post.getPostList(offset=int(page)-10, limit=int(page)-1)
            getPostListNext = post.getPostList(offset=int(page), limit=10)
        if(getPost == None):
            viewPost = {'postSril': 'getPost.postSrl', 'postTitle': 'getPost.title', 'postText': 'getPost.text', 'postWriter': 'getPost.writer', 'postWriten': 'getPost.writeTime', 'files': 'getPost.files'}
        else:
            t = time.localtime(getPost.writeTime)
            writen = str(t[1])+'월'+str(t[2])+'일 '+str(t[3])+':'+str(t[4])
            print(getPost.text)
            rendered = misaka.html(getPost.text)
            viewPost = {'postSril': getPost.postSrl, 'postTitle': getPost.title, 'postText': rendered, 'postWriter': getPost.writer, 'postWriten': writen, 'files': getPost.files}
        viewPostPrev = list()
        viewPostNext = list()
        for Post in getPostListPrev:
            t = time.localtime(Post.writeTime)
            writen = str(t[1])+'월'+str(t[2])+'일 '+str(t[3])+':'+str(t[4])
            temp = {'postSrl': Post.postSrl, 'postTitle': Post.title, 'postWriter': Post.writer, 'postWriten': writen}
            viewPostPrev.append(temp)
        for Post in getPostListNext:
            t = time.localtime(Post.writeTime)
            writen = str(t[1])+'월'+str(t[2])+'일 '+str(t[3])+':'+str(t[4])
            temp = {'postSrl': Post.postSrl, 'postTitle': Post.title, 'postWriter': Post.writer, 'postWriten': writen}
            viewPostNext.append(temp)
        return render_template('postView.jinja', viewPost=viewPost, viewPostPrev=viewPostPrev, viewPostNext=viewPostNext)

    @simpleBBS.route('/write', methods = ['POST', 'GET'])
    def postWrite():
        if(request.method=='POST'):
            if(not session.get('logged_in')==None):
                try:
                    newTitle = request.form['Title']
                    newText = request.form['Text']
                    Writer = session['userName']
                    writeTime = int(time.time())
                    print(newTitle)
                    print(newText)
                    print(Writer)
                    print(writeTime)
                    # if(not request.files.get('files')==None):
                    #     print('files')
                    #     fileList = list()
                    #     for file in request.files['files']:
                    #         uploadFile(file)
                    #         fileList.append(files.getLatestFile())
                    # else:
                    #     print('no files')
                    #     fileList = None
                    newPost = post(title=newTitle, text=newText, writer=Writer, writeTime=str(writeTime),files = None)
                    db_session.add(newPost)
                    db_session.commit()
                except Exception as e:
                    print(e)
                    return redirect(request.referrer)
                finally:
                    return redirect(url_for(endpoint='.postRead'))
            else:
                flash('You have not perm')
                return redirect(request.referrer)
        else:
            if(not session.get('logged_in')==None):
                    return render_template('postWrite.jinja')
            else:
                flash('You have not perm')
                return redirect(url_for('index'))

    # def allowed_file(filename):
    #     return ('.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS)

    # def uploadFile(file):
    #     if(request.method == 'POST'):
    #         if file and allowed_file(file.filename):
    #             nowTime = int(time.time())
    #             filename = secure_filename(file.filename)
    #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #             fileUp = files(fileName=file.fileName, fileUploaded= str(nowTime), fileExtention=file.fileName.split('.')['-1'], fileSaved=secure_filename(file.fileName))
    #             print('fileUp : ' + fileUp)
    #             db_session.add(fileUp)
    #             db_session.commit

    # @simpleBBS.route('/uploads/<filename>')
    # def sendFile(filename):
    #     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)