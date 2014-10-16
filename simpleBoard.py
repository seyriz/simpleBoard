from flask import *
from models import *
from uploader import *
from DB import db_session
import time
import misaka
import random
import shutil

class simpleBoard:
    

    simpleBBS = Blueprint('simpleBBS', __name__, template_folder='templates/simpleBoard')

    @simpleBBS.route('/<args>')
    def postRead(args=dict()):
        getPostList = post.getPostList(boardname=args.get('board'))
        if(getPostList is None):
            viewPost = {'postSrl': 'getPost.postSrl', 'postTitle': 'getPost.title', 'postText': 'getPost.text', 'postWriter': 'getPost.writer', 'postWriten': 'getPost.writeTime', 'files': 'getPost.files'}
        else:
            postList = list()
            for getPost in getPostList:
                t = time.localtime(getPost.writeTime)
                writen = str(t[1])+'월'+str(t[2])+'일 '+str(t[3])+':'+str(t[4])
                rendered = misaka.html(getPost.text)
                commentList = comment.getComment(getPost.postSrl)
                comments = list()
                for commentTemp in commentList:
                    ct = time.localtime(commentTemp.writeTime)
                    commentWriten = str(ct[1])+'월'+str(ct[2])+'일 '+str(ct[3])+':'+str(ct[4])
                    commentR = misaka.html(commentTemp.comment)
                    temp = {'commentWriter': commentTemp.writer, 'commentWriten': commentWriten, 'comment': commentR, 'commentSrl': commentTemp.commentSrl}
                    comments.append(temp)
                fileDict = fileUploader.serving(getPost.files)
                viewPost = {'postSrl': getPost.postSrl, 'postTitle': getPost.title, 'postText': rendered,\
                    'postWriter': getPost.writer, 'postWriten': writen,\
                    'board': getPost.board, 'commentCount': getPost.commentCount,\
                    'comments': comments, 'fileList': fileDict}
                postList.append(viewPost)
            postList.reverse()
            return render_template('postView.jinja', postList=postList, isBoard=True, getBoard=args.get('board'))

    @simpleBBS.route('/write', methods=['POST'])
    def postWrite():
        if(request.method == 'POST'):
            if(not session.get('logged_in') is None):
                try:
                    board = request.form['board']
                    newTitle = request.form['Title']
                    newText = request.form['Text']
                    Writer = session['userName']
                    writeTime = int(time.time())
                    files=request.files.getlist("file")
                    for file in files:
                        print(files)
                    fileUUID = fileUploader.upload(files=files)
                    newPost = post(title=newTitle, text=newText, writer=Writer, writeTime=str(writeTime), boardname=board, files=fileUUID)
                    db_session.add(newPost)
                    db_session.commit()
                except Exception as e:
                    print(e)
                    flash(e)
                    return redirect(request.referrer)
                finally:
                    return redirect(url_for(endpoint=board+'.index'))
            else:
                flash('You have not perm')
                return redirect(request.referrer)
        else:
            flash('Invalid user account!')
            return redirect(request.referrer)

    @simpleBBS.route('/deletePost/<int:postSrl>')
    def deletePost(postSrl):
        postInfo = post.getPost(postSrl)
        if(not session.get('logged_in') is None and session.get('userName') == postInfo.writer):
            try:
                postName = postInfo.title
                postFiles = postInfo.files
                shutil.rmtree(defaultconfig.UPLOAD_FOLDER+'/'+postFiles)
                db_session.delete(postInfo)
                db_session.commit()
                flash('Deleted ' + postName + '!')
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                flash("Error! : " + str(e))
                return redirect(request.referrer)
        else:
            flash('Invalid access!')
            return redirect(url_for('index'))

    @simpleBBS.route('/modifyPost/<int:postSrl>', methods=['POST', 'GET'])
    def modifyPost(postSrl):
        postInfo = post.getPost(postSrl)
        boardname = board.query.get(post.query.get(postSrl).board).board
        if(not session.get('logged_in') is None and session.get('userName')==postInfo.writer):
            if(request.method == 'POST'):
                try:
                    postInfo.title = request.form['Title']
                    postInfo.text = request.form['Text']
                    db_session.add(postInfo)
                    db_session.commit()
                    return redirect(url_for(boardname+'.index'))
                except Exception as e:
                    print(e)
                    flash("Error! : " + str(e))
                    return redirect(url_for(boardname+'.index'))
            else:
                modiPost = {'Title': postInfo.title, 'postSrl': postSrl, 'Text':postInfo.text}
                return render_template('postModify.jinja', modiPost=modiPost)
        flash('Invalid access!')
        return redirect(url_for('index'))

    @simpleBBS.route('/commentWrite/', methods=['POST'])
    def commentWrite():
        if(request.method == 'POST'):
            if(not session.get('logged_in') is None):
                try:
                    getComment = request.form['Comment']
                    getWriter = session['userName']
                    postSrl = request.form['postSrl']
                    now = time.time()
                    newComment = comment(post=postSrl, comment=getComment, writer=getWriter, writeTime=now)
                    posts = post.query.get(postSrl)
                    posts.commentCount += 1
                    db_session.add(posts)
                    db_session.add(newComment)
                    db_session.commit()
                    return redirect(request.referrer)
                except Exception as e:
                    print(e)
                    return redirect(request.referrer)
            else:
                flash('You have not perm')
                return redirect(request.referrer)
        else:
            flash('You have not perm')
            return redirect(url_for('index'))

    @simpleBBS.route('/commentDelete/<int:commentSrl>')
    def commentDelete(commentSrl):
        print(str(commentSrl)+'!')
        commentInfo = comment.getCommentOnce(commentSrl)
        if(not session.get('logged_in') is None and session.get('userName')==commentInfo.writer):
            try:
                print('in')
                commentPost = commentInfo.post
                print(1)
                db_session.delete(commentInfo)
                print(2)
                postInfo = post.query.get(commentPost)
                print(3)
                postInfo.commentCount -= 1
                print(4)
                db_session.add(postInfo)
                print(5)
                db_session.commit()
                flash('Deleted!')
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                flash("Error! : " + str(e))
                return redirect(request.referrer)
        else:
            flash('Invalid access!')
            return redirect(url_for('app.index'))

    @simpleBBS.route('/testB/<int:seed>/<int:count>')
    def rendPost(seed,count=100):
        if(not session.get('logged_in') is None):
            start = time.time()
            for x in range(1,count):
                time.sleep(0.2)
                tempseed = random.randint(1, random.randint(x, x+seed)*seed)
                print(tempseed)
                tempseed2 = tempseed-random.randint(1,seed)
                try:
                    newTitle = str(x)+' : '+ str(tempseed)
                    newText = tempseed2*tempseed
                    Writer = session['userName']
                    writeTime = int(time.time())
                    newPost = post(title=newTitle, text=newText, writer=Writer, writeTime=str(writeTime),files=None)
                    db_session.add(newPost)
                    db_session.commit()
                except Exception as e:
                    print(e)
                    allof = time.time()-start
                    return "Fail("+allof+"sec) : "+e
            return "Success"
        else:
            flash('You have not perm')
            return redirect(url_for('index'))

    @simpleBBS.route('/testC/<int:seed>/<int:count>')
    def randComment(seed,count=100):
        if(not session.get('logged_in') is None):
            start = time.time()
            maxPost = 1610
            print(maxPost)
            for x in range(1,count):
                time.sleep(0.2)
                tempseed = random.randint(1, random.randint(x, x+seed)*seed)
                targetPost = random.randint(1, maxPost)
                print(str(x)+'-'+str(targetPost)+' : '+str(tempseed))
                try:
                    getComment = tempseed
                    getWriter = session['userName']
                    now = time.time()
                    newComment = comment(post=targetPost, comment=getComment, writer=getWriter, writeTime=now)
                    posts = post.query.get(targetPost)
                    posts.commantCount += 1
                    db_session.add(posts)
                    db_session.add(newComment)
                    db_session.commit()
                except Exception as e:
                    print(e)
                    allof = time.time()-start
                    return "Fail("+allof+"sec) : "+e
            return "Success"
        else:
            flash('You have not perm')
            return redirect(url_for('index'))