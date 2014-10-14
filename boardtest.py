from flask import *
from models import *
from DB import db_session
from simpleBoard import *
import time, os, misaka, random

class testBoard:
    testBoard = Blueprint('testBoard', __name__, template_folder='templates/testBoard')
    
    @testBoard.route('/list')
    def index():
        return simpleBoard.postRead({'board': 'testBoard'})

    @testBoard.route('/new')
    def newPost():
        if(not session.get('logged_in')==None):
            return render_template('postWrite.jinja', getboard='testBoard')
        else:
            flash('You have not perm')
            return redirect(url_for('index'))