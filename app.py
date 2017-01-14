from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

#Import database_setup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Item, Category, Base

engine = create_engine('sqlite:///catelog_app.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
#----------------------------------------------------
#anti-forgery solution
import random, string
from flask import session as login_session
#------------------------------------------------------
#server-side http request for FB connec
import httplib2
import json
from flask import make_response
#--------------------------------------
import hashlib
#items number showed in index page
ITEM_SHOW_NUM = 9


@app.route('/')
def index():
    #check if login in
    isLogin = False
    if 'user_id' in login_session:
        isLogin = True
    #db query
    categories_all = session.query(Category).all()
    items_all = session.query(Item).limit(ITEM_SHOW_NUM).all()
    #---------
    #anti-forgery
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state 
    #------------
    return render_template('main.html', cates = categories_all, items = items_all, latests = True, STATE = state, isLogin = isLogin)
  
@app.route('/catalog/<string:category>/items/')
def showItems(category):
    #check if login in
    isLogin = False
    if 'user_id' in login_session:
        isLogin = True    
    #db query
    categories_all = session.query(Category).all()
    category = session.query(Category).filter_by(name = category).one()
    items = session.query(Item).filter_by(category_id = category.id).limit(ITEM_SHOW_NUM).all()
    count = len(items)
    #--------
    return render_template('main.html', cates = categories_all, items = items, latests = False, uni_cate = category, count = count, isLogin = isLogin, STATE = login_session['state'])

@app.route('/catalog/<string:category>/<string:item>/')

def showDescription(category, item):
    #db query
    item = session.query(Item).filter_by(name = item).one()
    #--------
    user_id = None
    isLogin = False
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        isLogin = True
    return render_template("item_info.html", item = item, user_id = user_id, isLogin = isLogin)

@app.route('/catalog/new/', methods = ['POST', 'GET'])
def addItem():
    if request.method == 'GET':
        isLogin = False
        if 'user_id' in login_session:
            isLogin = True
        categories_all = session.query(Category).all()
        return render_template('item_add.html', cates = categories_all, STATE = login_session['state'], isLogin = isLogin)
    else:
        if request.args.get('state') != login_session['state']:
            return respondToClient("Invaild State.", 401) 
        if 'user_id' not in login_session:
            return respondToClient("Please login first.", 401) 
        #login and state is correct      
        name = request.form['title']
        description = request.form['description']
        category_id = request.form['category_id']
        if not name or not description or not category_id:
            return respondToClient("Failed to get required input", 400)
        newItem = Item(name = name, description = description, category_id = category_id, user_id = login_session['user_id'])
        #actually, item should be unique and I do not check that here
        session.add(newItem)
        session.commit()
        return respondToClient('Add item successsful',200)

@app.route('/catalog/<string:item>/edit/', methods = ['POST', 'GET'])
def editItem(item):
  if request.method == 'GET':
        isLogin = False
        if 'user_id' in login_session:
            isLogin = True
        categories_all = session.query(Category).all()
        editItem = session.query(Item).filter_by(name = item).one()
        return render_template('item_edit.html', cates = categories_all, STATE = login_session['state'], isLogin = isLogin, item = editItem)
  else:
        if request.args.get('state') != login_session['state']:
            return respondToClient("Invaild State.", 401) 
        if 'user_id' not in login_session:
            return respondToClient("Please login first.", 401) 
        #login and state is correct      
        name = request.form['title']
        description = request.form['description']
        category_id = request.form['category_id']
        if not name or not description or not category_id:
            return respondToClient("Failed to get required input", 400)
        editItem = session.query(Item).filter_by(name = item).one()
        editItem.name = name
        editItem.description = description
        editItem.category_id = category_id
        #actually, item should be unique and I do not check that here
        session.add(editItem)
        session.commit()
        return respondToClient('Edit item successsful',200)    

@app.route('/catalog/<string:item>/delete/', methods = ['POST', 'GET'])
def deleteItem(item):
  if request.method == 'GET':
        isLogin = False
        if 'user_id' in login_session:
            isLogin = True
        deleteItem = session.query(Item).filter_by(name = item).one()
        return render_template('item_edit.html', STATE = login_session['state'], isLogin = isLogin, item = deleteItem)
  else:
        if request.args.get('state') != login_session['state']:
            return respondToClient("Invaild State.", 401) 
        if 'user_id' not in login_session:
            return respondToClient("Please login first.", 401) 
        #login and state is correct      
        deleteItem = session.query(Item).filter_by(name = item).one()
        session.delete(deleteItem)
        session.commit()
        return respondToClient('Delete item successsful',200)    

@app.route('/login', methods = ['POST'])
def login():
    if request.args.get('state') != login_session['state']:
        return respondToClient("Invaild State.", 401)
    email = request.form['email']
    raw_password = request.form['password']
    if not email or not raw_password:
        return respondToClient("Failed to get required input", 400)
    result = user_auth(email, raw_password)
    if result == 0:
        return respondToClient("User do not exist. Please try again", 404)
    elif result == 1:
        user = session.query(User).filter_by(email = email).one()
        login_session['provider'] = 'local'
        login_session['name'] = user.name
        login_session['email'] = user.email
        login_session['user_id'] = user.id
        login_session['picture'] = user.picture
        return respondToClient(user.name, 200)
    elif result == 2:
        return respondToClient("Wrong password", 400)
    else:
        return respondToClient("Server Error", 500)

@app.route('/register/', methods = ['POST', 'GET'])
def register(): 
    if request.method == 'POST':
        if request.args.get('state') != login_session['state']:
            return respondToClient("Invaild State.", 401)
        email = request.form['email']
        raw_password = request.form['password']
        if not email or not raw_password:
            return respondToClient("Failed to get required input", 400)
        if getUserId(email):
            return respondToClient("User already exists", 400)
        user_id = createLocalUser(email, raw_password)
        user = session.query(User).filter_by(id = user_id).one()
        login_session['provider'] = 'local'
        login_session['name'] = user.name
        login_session['email'] = user.email
        login_session['user_id'] = user.id
        return respondToClient(user.name, 200)
    else:
        return render_template('signup.html', STATE = login_session['state'])

def localLogOut():
    del login_session['provider']
    del login_session['name']
    del login_session['email']
    del login_session['user_id']
    return redirect(url_for('index'))

def fbdisconnect():
     facebook_id = login_session['facebook_id']
     url = 'https://graph.facebook.com/%s/permissions' % facebook_id
     h = httplib2.Http()
     result = h.request(url, 'DELETE')[1]
     #no error handler
     del login_session['provider'] 
     del login_session['name'] 
     del login_session['email'] 
     del login_session['facebook_id'] 
     del login_session['user_id']
     return redirect(url_for('index'))
@app.route('/logout/')
def logOut():
    if login_session['provider'] == 'local':
        return localLogOut()
    elif login_session['provider'] == 'facebook':
        return fbdisconnect()
    else:
        return respondToClient("Logout Error", 500)


@app.route('/fbconnect', methods = ['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
       return respondToClient("Invalid State.", 401)
    #fbconnect
    #load app configurations
    access_token = request.data
    app_id = json.loads(open('fb_client_secret.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secret.json', 'r').read())['web']['app_secret']

    #exchange short token for long-lived token
    url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    long_live_token = result.split("&")[0]

    #use long-lived token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me?%s&fields=name,id,email" % long_live_token
    result = h.request(userinfo_url, 'GET')[1]
    data = json.loads(result)
    if data['name'] and data['email'] and data['id']:
        login_session['provider'] = 'facebook'
        login_session['name'] = data['name']
        login_session['email'] = data['email']
        login_session['facebook_id'] = data['id']
    else:
        return respondToClient("Can't get userinfo from Facebook", 500)
    #get user picture
    url = "https://graph.facebook.com/%s/picture?&redirect=0&height=200&width=200" % login_session['facebook_id']
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    if data['data']['url']:
        login_session['picture'] = data["data"]["url"]
    else:
        return respondToClient("Can't get user picutre", 500)

    #store third-party user into database
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    return respondToClient(login_session['name'], 200)
    
def respondToClient(description, status_code):
    response = make_response(json.dumps(description), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response

#User operation functions       
def createUser(login_session):
    newUser = User(name = login_session['name'], email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def createLocalUser(email, raw_password):
    hashed_pw = pw_hash(raw_password)
    newUser = User(email = email, password = hashed_pw)
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = email).one()
    return user.id

def getUserId(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

#Password encrytion and authentication
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def pw_hash(raw_password, salt = None):
    if not salt:
        salt = make_salt()
    pw = hashlib.sha256(raw_password + salt).hexdigest()
    return "%s,%s" % (salt, pw)

# 0 -> user not exists
# 1 -> user exists and password right
# 2 -> user exists but password wrong
def user_auth(email, raw_password):
    user_id = getUserId(email)
    if user_id:
        user = session.query(User).filter_by(id = user_id).one()
        hashed_pw = user.password
        salt = hashed_pw.split(',')[0]
        if pw_hash(raw_password, salt) == hashed_pw:
            return 1
        else:
            return 2
    else:
        return 0

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)