from flask import Flask,session
from flask_mysqldb import MySQL
#print('file name is '+__name__)


db = MySQL()

def create_app():

    app = Flask(__name__)
    app.secret_key = 'soju69'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'soju_services'


    import route
    app.register_blueprint(route.router)
    mysql = MySQL(app)
    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1',port=6942)

