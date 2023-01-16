
from flask import Blueprint,request,render_template,jsonify
import os
from werkzeug.utils import secure_filename
from markupsafe import escape
from . import innit
mysql = innit.db

testing = Blueprint('testing', __name__, template_folder='templates')

@testing.route('/test/<token>', methods=['GET','POST'])
def route_test(token):
    if request.method == 'POST':
       cur = mysql.connection.cursor()
       query = "SELECT `url` FROM `users` WHERE `token` = '"+token+"'"
       cur.execute(query)
       rv = cur.fetchall()

       temp = str(rv)
       url_tr = ''

       if temp =='()':
                    url_str = 'soju.services'
                    return url_str

       else:
                    url_str = temp

                    return url_str.strip(',)(\'')

    elif request.method == 'GET':
        return f'haha'


