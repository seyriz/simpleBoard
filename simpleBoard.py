from flask import *
from models import *
from DB import db_session
import time, os, misaka, random
class simpleBoard:
    

    simpleBBS = Blueprint('simpleBBS', __name__, template_folder='templates/simpleBoard')

    @simpleBBS.route('/<args>')
    def postRead(args=dict()):
        getPostList = post.getPostList(boardname=args.get('board'))
        if(getPostList == None):
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
                    temp = {'commentWriter': commentTemp.writer, 'commentWriten': commentWriten, 'comment': commentR}
                    comments.append(temp)
                viewPost = {'postSrl': getPost.postSrl, 'postTitle': getPost.title, 'postText': rendered, \
                'postWriter': getPost.writer, 'postWriten': writen, \
                'board': getPost.board , 'commentCount': getPost.commantCount,\
                'comments': comments}
                postList.append(viewPost)
        return render_template('postView.jinja', postList=postList, isBoard=True, getBoard=args.get('board'))

    @simpleBBS.route('/write', methods = ['POST'])
    def postWrite():
        if(request.method=='POST'):
            if(not session.get('logged_in')==None):
                try:
                    board = request.form['board']
                    newTitle = request.form['Title']
                    newText = request.form['Text']
                    Writer = session['userName']
                    writeTime = int(time.time())
                    print(board)
                    newPost = post(title=newTitle, text=newText, writer=Writer, writeTime=str(writeTime), boardname=board)
                    db_session.add(newPost)
                    db_session.commit()
                except Exception as e:
                    print(e)
                    return redirect(request.referrer)
                finally:
                    return redirect(url_for(endpoint=board+'.index'))
            else:
                flash('You have not perm')
                return redirect(request.referrer)
        else:
            flash('Invalid user account!')
            return redirect(request.referrer)

    @simpleBBS.route('/commentWrite/<postSrl>', methods=['POST'])
    def commentWrite(postSrl):
        if(request.method=='POST'):
            if(not session.get('logged_in')==None):
                try:
                    getComment = request.form['Comment']
                    getWriter = session['userName']
                    now = time.time()
                    newComment = comment(post=postSrl, comment=getComment, writer=getWriter, writeTime=now)
                    posts = post.query.get(postSrl)
                    posts.commantCount += 1
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


    @simpleBBS.route('/testB/<int:seed>/<int:count>')
    def rendPost(seed,count=100):
        if(not session.get('logged_in')==None):
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
                    newPost = post(title=newTitle, text=newText, writer=Writer, writeTime=str(writeTime),files = None)
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
        if(not session.get('logged_in')==None):
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