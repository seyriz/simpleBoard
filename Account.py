from flask import *
from models import *
from DB import db_session
from config import defaultconfig
import hashlib
class accountModule:
    

    accountModule = Blueprint('account', __name__, template_folder='template/accountModule')

    @accountModule.route('/join', methods=['POST', 'GET'])
    def joinUser():
        if(not request.method == 'POST'):
            if(not session.get('logged_in')==None):
                flash('User can not Re-join')
                return redirect(url_for('index'))
            return render_template('join.jinja')
        else:
            if(not session.get('logged_in')==None):
                flash('User can not Re-join')
                return redirect(url_for('index'))
            try:
                email = request.form['email']
                if(not account.validEmail(email=email)):
                    flash('Already exist E-Mail')
                    return render_template('join.jinja')
                userPass = request.form['Password']
                userPass = userPass+defaultconfig.SECRET_KEY
                userPass = hashlib.sha512(userPass.encode()).hexdigest()
                userName = request.form['name']
                newuser = account(email=email, name=userName, passwd=userPass)
                db_session.add(newuser)
                db_session.commit()
                userInfo = account.getUserInfo(email=email)
                if(not userInfo):
                    return render_template('join.jinja')
                session['logged_in'] = True
                session['userSrl'] = userInfo.userSrl
                session['userName'] = userInfo.name
                session['userMail'] = userInfo.email
                flash('Wellcome '+userName+'!')
            except Exception as e:
                print(e)
            finally:
                return redirect(url_for('index'))
    @accountModule.route('/leave', methods = ['POST', 'GET'])
    def leave():
        if(not session.get('logged_in')==None):
            try:
                user = account.getUserInfo(email=session['userMail'])
                db_session.delete(user)
                db_session.commit()
                session.pop('logged_in', None)
                session.pop('userSrl', None)
                session.pop('userName', None)
                session.pop('userMail', None)
                flash('Good bye!')
                return redirect(url_for('index'))
            except:
                flash('Invalid Access')
                session.pop('logged_in', None)
                session.pop('userSrl', None)
                session.pop('userName', None)
                session.pop('userMail', None)
                return redirect(url_for('index'))
        else:
            flash('Invalid Access')
            return redirect(url_for('index'))

    @accountModule.route('/login', methods=['POST'])
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
                flash('Hello! '+session['userName'])
                return redirect(request.referrer)
            else:
                flash('Invalid user account!')
                return redirect(request.referrer)
        else:
            flash('Invalid Access')
            return redirect(url_for('index'))

    @accountModule.route('/logout', methods = ['POST'])
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