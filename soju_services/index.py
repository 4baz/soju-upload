from flask import Blueprint,request,render_template,url_for
import os
from werkzeug.utils import secure_filename
from markupsafe import escape

indx = Blueprint('index', __name__, template_folder='templates')


# file types list

img_file_type = ['webp','svg','png','jpg','jpeg','jfif','pjpeg','pjp','gif','avif','apng']

video_file_type = ['mp4','webm','ogg']

audio_file_type = ['mp3','wav']

from . import innit
mysql = innit.db

def check_file_exists(filename):

    try:
        open(os.path.join(innit.create_app().config['UPLOAD_FOLDER'],filename))
        print(filename + 'found')
        return 1
    except:
        print(filename + 'not found')
        return 0



def check_file_ext(filename):

    cur = mysql.connection.cursor()
    query = "SELECT `ext` FROM `uploads` WHERE name = '"+filename+"'"
    cur.execute(query)
    rv = cur.fetchall()
    temp = str(rv)

    temp = temp.strip(',)(\'')

    return temp


@indx.route('/', defaults={'link':'index'}, methods=['GET','POST'])
@indx.route('/<link>',methods=['GET','POST'])
def route_indx(link):
    if request.method == 'POST':
        return f'keked why tf u sending post request here lababa cuh'

    elif request.method == 'GET':

        if link == 'index':
            return render_template('index.html')
        else:
             #SQL query to check files extension then return the files name and
            #extenshion combined to check file exists function

            EXT = check_file_ext(link)

            if EXT == '()':
                return 'url error'

            else:
                FULL_filename = link + EXT
                print(EXT)
                c =  check_file_exists(FULL_filename)
                if c == 1:#<img src='{url_for('static',filename='user/'+FULL_filename)}' alt="Italian Trulli">

                # this is aids surely this is python knowledge issue and theres a less
                #shit way to do this the fuck? why no cases fr fr
                #    if EXT == '.apng' or EXT == '.avif' or EXT == '.gif' or EXT == '.jpg' or EXT == '.jpeg' or EXT == '.jfif' or EXT == '.pjpeg' or EXT == '.pjp'or EXT == '.png'or EXT == '.svg' or EXT == '.webp':
                 #           return render_template('image_template.html',file='user/'+FULL_filename)#parse filename to templates

 #  elif EXT == '.gif' or EXT == '.webp':
                    #         return  render_template('gif_template.html',file='user/'+FULL_filename)


                    if EXT.strip('.') in img_file_type:
                        return render_template('image_template.html',file='user/'+FULL_filename,name=FULL_filename)
                    elif EXT.strip('.') in video_file_type:
                            return render_template('video_template.html',file='user/'+FULL_filename,name=FULL_filename)
                    elif EXT.strip('.') in audio_file_type:
                            return render_template('audio_template.html',file='user/'+FULL_filename,name=FULL_filename)

                    else:
                            return render_template('download_template.html',file='user/'+FULL_filename,name=FULL_filename)

                else:
                        return 'url error'




#need to search for file with that name. then get the extension then based of extension
#choose template and return template with file in it

#need to add extra table with file and extension that gets inserted into upon sucessful upload

# SELECT `ext` from `uploads` WHERE `name` = link

#BLAH BLAH add insert statement on uploader side too


