from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
#from upload.upload import upload

db = MySQL()

def create_app():
    TEMP_DIRECTORY = 'storage/temp/'
    UPLOAD_FOLDER = 'storage/user/'
    ADMIN_UPLOAD_FOLDER = '/storage/admin'

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}#unused but can be implemented

    LIMIT_FILETYPES = False
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'nutz'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'soju_services'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['TEMP_DIRECTORY'] = TEMP_DIRECTORY
    app.static_folder = 'storage/'
    mysql = MySQL(app)
    from .upload import upld
    from .test import testing
    from .index import indx

    app.register_blueprint(upld)
    app.register_blueprint(indx)
    app.register_blueprint(testing)

    return app

