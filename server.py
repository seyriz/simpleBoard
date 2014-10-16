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
from simpleBoard import simpleBoard
from Account import accountModule
from portfolio import portfolio
from boardtest import testBoard
from uploader import fileUploader
import os

class server:
    app = Flask(__name__)
    app.config.from_object(defaultconfig)
    app.register_blueprint(simpleBoard.simpleBBS)
    app.register_blueprint(accountModule.accountModule, url_prefix='/account')
    app.register_blueprint(portfolio.portfolio)
    app.register_blueprint(testBoard.testBoard, url_prefix='/test')
    app.register_blueprint(fileUploader.fileOp, url_prefix='/files')

    @app.teardown_request
    def shutdown_session(exception=None):
        db_session.remove()

    @app.route('/')
    def index():
        return redirect(url_for('portfolio.index'))

    def __init__():
        app.run()

    if(__name__=='__main__'):
        if(not os.path.exists(defaultconfig.DATABASE_ADD)):
            init_db()
            for boardAdding in app.config['USING_BOARDS']:
                print(boardAdding)
                newboard =board(board=boardAdding)
                db_session.add(newboard)
                db_session.commit()
        __init__()