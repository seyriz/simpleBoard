class defaultconfig:
    """docstring for defaultconfig"""
    DEBUG = True
    PORT = 8080
    HOST = '0.0.0.0'
    SECRET_KEY = 'simpleBoard_sample_secret_key_this_is_not_secure'
    ADMIN = 'admin'
    ADMIN_PASSWORD = 'default'
    DATABASE_TYPE = 'sqlite3'
    DATABASE_ADD = 'BoardDB.sqlite3'
    UPLOAD_FOLDER = 'files'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    USING_BOARDS = ('portfolio','testBoard')