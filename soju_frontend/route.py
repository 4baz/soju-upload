from flask import Flask,Blueprint,request,render_template,session,redirect,url_for,jsonify,flash

#may need to set session token/save a individualised token as a user token in in discord so i can verify i will look into what the token is set to in firefox

import main
import json

router = Blueprint('routes', __name__, template_folder='templates')
mysql = main.db

def validate_form_data(username,password):

    query = 'SELECT * FROM `users` WHERE `username` =' +'\''+ username +'\''+ 'AND `password` = '+'\''+ password +'\';'

    cur = mysql.connection.cursor()
    cur.execute(query)
    rv = cur.fetchall()
    temp = str(rv)

    if temp == '()':
        return False
    #temp = temp.strip(',)(\'')
    else:
        return True

def check_session():

    seshcheck = session.get('valid')

    if seshcheck == 'true':
        return True

    else:
        return False


def get_domain_list():
    query = 'SELECT `url` FROM `urls`'
    cur = mysql.connection.cursor()
    cur.execute(query)
    rv = cur.fetchall()
    ret = jsonify(rv)
    return json.loads(ret)


def update_user_domain(domain,user):
    query = 'UPDATE `users` SET `url` = ' +'\''+domain+'\''+' WHERE `username` =' + '\''+user + '\''

    cur = mysql.connection.cursor()
    cur.execute(query)
    return True

    #should probs run statement to check but fug it

def get_user_uploads(username):
    query1 = 'SELECT `upload_token` FROM `users` WHERE `username` ='+"'"+username+"'"
    cur = mysql.connection.cursor()
    cur.execute(query1)
    rv = cur.fetchall()
    utoken = str(rv)
    utoken = utoken.strip(',)(\'')

    query2 = 'SELECT `name`,`ext` FROM `uploads` WHERE `token_used` ='+"'"+utoken+"'"
    cur.execute(query2)
    rv2 = cur.fetchall()
    res = jsonify(rv2)
    return json.loads(res)

def get_user_domain(username):

    query = 'SELECT `url` FROM `users` WHERE `username` = '+"'"+username+"'"
    cur = mysql.connection.cursor()
    cur.execute(query)
    rv = cur.fetchall()
    dmn = str(rv)
    return dmn.strip(',)(\'')

@router.route('/',methods=['GET','POST'])
def index_():
    if request.method == 'GET':
       # from . import lists
        return render_template('index/index.html')

    elif request.method == 'POST':
        return '0'



@router.route('/login',methods=['GET','POST'])
def login_():
    if request.method == 'GET':

        return render_template('login.html')

    elif request.method == 'POST':

        session['username'] = request.form['username']
        session['password'] = request.form['password']

        valid_user = validate_form_data(session.get('username'),session.get('password'))

        if valid_user == True:
            session['valid'] = 'true'
            return redirect(url_for('routes.dashboard_'))

        else:
            #set user and password to blank but the valid session check is always invalid so doesnt need to be checked
            session.pop('username')
            session.pop('password')
            return redirect(url_for('routes.index_'))
       # query = 'SELECT * FROM `users` WHERE `username` =' +'\''+ session.get('username') +'\''+ 'AND `password` = '+'\''+ session.get('password')+'\';'


@router.route('/dashboard',methods=['GET','POST'])
def dashboard_():
    if request.method == 'GET':

        if check_session() == True:

            domain_list = get_domain_list()
            #return f'username is {session.get("username")} and value of set session is {session.get("valid")}'
            return render_template('dashboard/dash.html',username=session.get('username'),domain_list=domain_list)


        else:
            return redirect(url_for('routes.index_'))

    elif request.method == 'POST':

        domain_selection = request.form['domain']
        update_user_domain(domain_selection,session.get('username'))




        return 0


@router.route('/dashboard-uploads',methods=['GET','POST'])
def uploads_():
    if request.method == 'GET':

        if session.get('valid') == 'true':


            uploads= get_user_uploads(session.get('username'))#python list/dict

            usr_domain_selection = get_user_domain(session.get('username'))# raw string

            return render_template('dashboard/uploads.html',username=session.get('username'),uploads=uploads,usr_domain_selection=usr_domain_selection)


        else: return redirect(url_for('routes.index_'))




@router.route('/logout',methods=['GET','POST'])
def logout_():
    if request.method == 'GET':

        if session.get('valid') == 'true':
            session.pop('valid')
            flash('user logged out')
            return redirect(url_for('routes.index_'))

    elif request.method == 'POST':
        return 0


