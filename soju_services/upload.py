from flask import Blueprint,request,jsonify, redirect,flash
import os
from werkzeug.utils import secure_filename
from markupsafe import escape
from . import upload
from . import innit
from flask_mysqldb import MySQL
import json
import shutil
upld = Blueprint('upload', __name__, template_folder='templates')

tkn = 'ballz'# replace hardcoded test with database query

mysql = innit.db
import random
import string
def get_random_string(length):
                    # choose from all lowercase letter
                    letters = string.ascii_lowercase
                    result_str = ''.join(random.choice(letters) for i in range(length))
                    return result_str


def verify_user_exists(token):
        cur = mysql.connection.cursor()
        query = "SELECT * FROM `users` WHERE `token` = '"+token+"'"
        cur.execute(query)
        rv = cur.fetchall()

        temp = str(rv)
        if temp == '()':
            return 0
        else:
            return 1


def register_upload(name,token_used):

    dot_pos = name.rfind(".")
    ext =  name[dot_pos:]
    raw_name = name[:dot_pos]
    cur = mysql.connection.cursor()
    query = "INSERT INTO uploads (name,ext,token_used) VALUES ('"+raw_name+"','"+ext+"','"+token_used+"');"
    cur.execute(query)
    mysql.connection.commit()
    rv = cur.fetchall()
    print(name+ ' - inserted')

@upld.route('/upload',defaults={'token':'invalid'},methods=['GET','POST'])
@upld.route('/upload/<token>', methods=['GET','POST'])
def upload_file(token):
    if request.method == 'POST':
     if token == 'invalid':
            return f'yo'
     else:

        cur = mysql.connection.cursor()
        query = "SELECT * FROM `users` WHERE `token` = '"+token+"'"
        cur.execute(query)
        rv = cur.fetchall()

        temp = str(rv)
        print(temp)
        JsonRes = jsonify(rv)

        badres = {'success':False}



        if temp == '()':
            return 'Invalid Token'
        else:
          #  return JsonRes #f'User token: {escape(token)}'
            if 'file' not in request.files:
                flash('no file found')
                return jsonify(badres)

            file = request.files['file']
            if file.filename == '':
                flash('file name error')
                return jsonify(badres)

            if file:
                filename = secure_filename(file.filename)

#   rename file to random string and save file to temp path first
#then rename and put in the destination folder
                file.save(os.path.join(innit.create_app().config['TEMP_DIRECTORY'],filename))

                dot_pos = file.filename.rfind(".")#flawless (no room for issues stg )

                ext_type = file.filename[dot_pos:]


                new_name_str = get_random_string(15)
                new_filename = new_name_str + ext_type

                shutil.move(os.path.join(innit.create_app().config['TEMP_DIRECTORY'],filename),os.path.join(innit.create_app().config['UPLOAD_FOLDER'],new_filename))
                #maybe works i believe too look cleaner i have to filter the
                #. part of the link string bc epic seggs )also need to randomise
                #filename
                dot_pos = file.filename.rfind(".")#flawless (no room for issues stg )

                url_ext_frm_sql = ''


                cur = mysql.connection.cursor()
                query = "SELECT `url` FROM `users` WHERE `token` = '"+token+"'"
                cur.execute(query)
                rv = cur.fetchall()

                temp = str(rv)
                url_tr = ''

                if temp =='()':
                    url_str = 'soju.services'
                else:
                    url_str = temp
                    url_str = url_str.strip(',)(\'')


                user_ext = 'https://' + url_str +'/' # do later need to add user link and sql db shit


               # res_link = user_ext+file.filename[:dot_pos]
                res_link = user_ext+new_name_str
                good_res = {

                "success": True,
                "files": [
                            {
                                "name": new_filename,
                                "url": res_link
                            }
                         ]

                }
                register_upload(new_filename,token)
                return jsonify(good_res)



    elif request.method == 'GET':

        if token == 'invalid':
            return f'yo'
        else:

            does_exist = verify_user_exists(token)
            if does_exist ==1:
                f'user exists {token}'
            else:
                return f'user token {token} invalid, fuck off?'




