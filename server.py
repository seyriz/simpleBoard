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
import os, sys, hashlib, datetime, time
from werkzeug import secure_filename
from simpleBoard import simpleBoard
from Account import accountModule

class server:
    app = Flask(__name__)
    app.config.from_object(defaultconfig)
    app.register_blueprint(simpleBoard.simpleBBS, url_prefix='/post')
    app.register_blueprint(accountModule.accountModule, url_prefix='/account')

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()

    @app.route('/')
    def index():
        return render_template('index.jinja')

    

    

    if(__name__=='__main__'):
        if(not os.path.exists(defaultconfig.DATABASE_ADD)):
            init_db()
        app.run()