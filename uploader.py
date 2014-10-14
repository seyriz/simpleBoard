from flask import *
from models import *
from config import defaultconfig
from werkzeug import secure_filename
import os
import json
import glob
from uuid import uuid4

class fileUploader:
    fileOp = Blueprint('fileOp', __name__, template_folder='templates/uploader')

    @fileOp.route("/")
    def index():
        return render_template("index.html")


    @fileOp.route("/upload", methods=["POST"])
    def upload(files):
        """Handle the upload of a file."""
        form = request.form
    # Create a unique "session ID" for this particular batch of uploads.
        upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
        is_ajax = False
        if form.get("__ajax", None) == "true":
            is_ajax = True

    # Target folder for these uploads.
        target = defaultconfig.UPLOAD_FOLDER+"/{}".format(upload_key)
        try:
            os.mkdir(target)
        except:
            if is_ajax:
                return ajax_response(False, "Couldn't create upload directory: {}".format(target))
            else:
                return "Couldn't create upload directory: {}".format(target)

        print('=== Form Data ===')
        for key, value in list(form.items()):
            print(key, "=>", value)

        for upload in files:
            try:
                filename = upload.filename.rsplit("/")[0]
                filename = (secure_filename(filename))
                destination = "/".join([target, filename])
                print("Accept incoming file:", filename)
                print("Save it to:", destination)
                upload.save(destination)
            except Exception as e:
                print(e)

        if is_ajax:
            return ajax_response(True, upload_key)
        else:
            return upload_key


    @fileOp.route("/files/<uuid>")
    def serving(uuid):
        """The location we send them to at the end of the upload."""

    # Get their files.
        root = defaultconfig.UPLOAD_FOLDER+"/{}".format(uuid)
        if not os.path.isdir(root):
            return "Error: UUID not found!"

        files = []
        for file in glob.glob("{}/*.*".format(root)):
            fname = file.split("/")[-1]
            files.append(fname)

        return {'uuid':uuid, 'files':files}


    def ajax_response(status, msg):
        status_code = "ok" if status else "error"
        return json.dumps(dict( status=status_code, msg=msg,))