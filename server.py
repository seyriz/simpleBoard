"""
    simpleBoard
    --------------------------------------

    A simpleBoard is python3-flask based simplb web BBS.
    

    :copyright: (c) 2014 by Lee, Han-Wool.
    :license: GPLv3
"""
from flask import *
from DB import db_session, init_db
from models import *
from config import defaultconfig
import os, sys, hashlib, datetime
from werkzeug import secure_filename

class server:
           
    app = Flask(__name__)
    app.config.from_object(defaultconfig)

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()

    @app.route('/')
    def index():
        return render_template('index.jinja')

    @app.route('/join', methods=['POST', 'GET'])
    def joinUser():
        if(not request.method == 'POST'):
            return render_template('join.jinja')
        else:
            try:
                email = request.form['email']
                if(not account.validEmail(email = email)):
                    print('fail to valid')
                    flash('Already exist E-Mail')
                    return render_template('join.jinja')
                userPass = request.form['Password']
                userPass = userPass+defaultconfig.SECRET_KEY
                userPass = hashlib.sha512(userPass.encode()).hexdigest()
                userName = request.form['name']
                newuser = account(email=email, name=userName, passwd=userPass)
                db_session.add(newuser)
                db_session.commit()
                flash('Wellcome '+userName+'!')
            except Exception as e:
                print(e)
            finally:
                return redirect(url_for('index'))
    @app.route('/leave', methods = ['POST', 'GET'])
    def leave():
        if(session['logged_in']):
            user = account.getUserInfo(email=session['userMail'])
            db_session.delete(user)
            db_session.commit()
            session.pop('logged_in', None)
            session.pop('userSrl', None)
            session.pop('userName', None)
            session.pop('userMail', None)
            print('point : 2')
            flash('Good bye!')
            return redirect(url_for('index'))
        else:
            flash('Invalid Access')
            return redirect(url_for('index'))

    @app.route('/login', methods=['POST'])
    def login():
        error = None
        if(request.method == 'POST'):
            userId = request.form['email']
            userPass = request.form['Password']
            userPass = userPass+defaultconfig.SECRET_KEY
            userPass = hashlib.sha512(userPass.encode()).hexdigest()
            if(account.getValidLogin(email=userId, passwd=userPass)):
                userInfo = account.getUserInfo(email=userId)
                session['logged_in'] = True
                session['userSrl'] = userInfo.userSrl
                session['userName'] = userInfo.name
                session['userMail'] = userInfo.email
                print(session)
                print(session['logged_in'])
                flash('Hello! '+session['userName'])
                return redirect(request.referrer)
            else:
                flash('Invalid user account!')
                return redirect(request.referrer)
        else:
            flash('Invalid Access')
            return redirect(url_for('index'))

    @app.route('/logout', methods = ['POST'])
    def logout():
        error = None
        if(request.method == 'POST'):
            if(session['logged_in']):
                session.pop('logged_in', None)
                session.pop('userSrl', None)
                session.pop('userName', None)
                session.pop('userMail', None)
                flash('Good bye!')
                return redirect(request.referrer)
            else:
                flash('Invalid Access')
                return redirect(url_for('index'))
        else:
            flash('Invalid Access')
            return redirect(url_for('index'))


    


    def allowed_file(filename):
        return ('.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS)

    @app.route('/upload', methods = ['POST'])
    def upload_file(file):
        if(request.method == 'POST'):
            files = {'fileName': file.fileName, 'fileUploaded': datetime.now(), 'fileExtention': file.fileName.split('.')[-1], 'fileSaved': file.secure_filename(file.fileName)}
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return files

    if(__name__=='__main__'):
        if(not os.path.exists(defaultconfig.DATABASE_ADD)):
            init_db()
        app.run()