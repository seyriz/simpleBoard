from flask import *
from models import *
from config import defaultconfig
from DB import db_session
from simpleBoard import *
import time, os, misaka, random

class portfolio:
    portfolio = Blueprint('portfolio', __name__, template_folder='templates/portfolio')

    @portfolio.route('/')
    def index():
        return redirect(url_for('.pofolList'))

    @portfolio.route('/portfolio')
    def pofolList():
        return simpleBoard.postRead({'board': 'portfolio'})

    @portfolio.route('/portfolio/new')
    def newPost():
        if(not session.get('logged_in')==None):
            return render_template('postWrite.jinja', getboard='portfolio')
        else:
            flash('You have not perm')
            return redirect(url_for('index'))