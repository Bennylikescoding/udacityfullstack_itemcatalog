
#===================
# Imports
#===================

from flask import Flask, render_template, request, redirect,jsonify, url_for, flash


from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
#-----user local permission
from database_setup import Base, Category, ListItem, User
#-----user local permission

from database_setup import Base, Category, ListItem

#login session, import modules:
from flask import session as login_session
import random, string

#login session, import GConnect:
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

#===================
# Flask instance
#===================

app = Flask(__name__)

#===================
# GConnect CLIENT_ID
#===================


CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']

#===================
# DataBase connection
#===================

#Connect to Database and create database session
#engine = create_engine('sqlite:///analysislists.db')

#------user local permission
engine = create_engine('sqlite:///analysislists_withusers.db')
#---------
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#==================
# User functions:
#==================

def createUser(login_session):
    newUser = User(email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


#===================
# Login Routing
#===================


#login session, create a state token to prevent request forgery
#store it in the session for later validation
@app.route('/login')
def showLogin():
  state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
  login_session['state'] = state
  #return "The current session state is %s" % login_session['state']
  return render_template('login.html', STATE=state)

#login session, write function that accepts post requests
@app.route('/gconnect', methods=['POST'])
def gconnect():
  if request.args.get('state')!=login_session['state']:
    response = make_response(json.dumps('Invalid state parameter'), 401)
    response.headers['Content-Type'] = 'application'
    return response
  code = request.data
  try:
    #upgrade the authorization code into a credentials object
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)
  except FlowExchangeError:
    response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  #check that the access token is valid.
  access_token = credentials.access_token
  url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'% access_token)
  h = httplib2.Http()
  result = json.loads(h.request(url, 'GET')[1])
  #if there was an error in the accesss token info, abort
  if request.args.get('error') is not None:
    response = make_response(json.dumps(result.get('error')), 500)
    response.headers['Content-Type'] = 'application/json'
    return response
  # Verify that the access token is used for the intended user.
  #gplus_id = credentials.id_token['sub']
  #if result['user_id'] != gplus_id:
  #    response = make_response(
  #        json.dumps("Token's user ID doesn't match given user ID."), 401)
  #    response.headers['Content-Type'] = 'application/json'
  #    return response
  # Verify that the access token is valid for this app.
  if result['issued_to'] != CLIENT_ID:
      response = make_response(
          json.dumps("Token's client ID does not match app's."), 401)
      print "Token's client ID does not match app's."
      response.headers['Content-Type'] = 'application/json'
      return response
  stored_access_token = login_session.get('access_token')
  #stored_gplus_id = login_session.get('gplus_id')
  #if stored_access_token is not None and gplus_id == stored_gplus_id:
  #    response = make_response(
  #        json.dumps('Current user is already connected.'), 200)
  #    response.headers['Content-Type'] = 'application/json'
   #   return response
  # Store the access token in the session for later use.
  login_session['access_token'] = credentials.access_token
  #login_session['gplus_id'] = gplus_id

  # Get user info
  userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
  params = {'access_token': credentials.access_token, 'alt': 'json'}
  answer = requests.get(userinfo_url, params=params)

  data = answer.json()

  #login_session['username'] = data['email']
  login_session['picture'] = data['picture']
  login_session['email'] = data['email']

  #-----user permission system
  # see if user exists, if it doesn't, make a new one:
  user_id = getUserID(login_session['email'])
  if not user_id:
    user_id = createUser(login_session)
  login_session['user_id'] = user_id

  #-----user permission system


  output = ''
  output += '<h1>Welcome, '
  #output += login_session['username']
  output += login_session['email']
  output += '!</h1>'
  output += '<img src="'
  output += login_session['picture']
  output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
  flash("you are now logged in as %s" % login_session['email'])
  print "done!"
  return output


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    #print 'User name is: '
    #print login_session['username']
    print 'Email is: '
    print login_session['email']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']

        #https://github.com/udacity/ud330/issues/53:
        #del login_session['gplus_id']
        #del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


#===================
# Flask Routing
#===================

#-----------
# JSON APIs:
#-----------

#JSON APIs to view Category Information
@app.route('/category/<int:category_id>/list/JSON')
def categoryListJSON(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(ListItem).filter_by(category_id = category_id).all()
    return jsonify(ListItems=[i.serialize for i in items])


@app.route('/category/<int:category_id>/list/<int:list_id>/JSON')
def listItemJSON(category_id, list_id):
    List_Item = session.query(ListItem).filter_by(id = list_id).one()
    return jsonify(List_Item = List_Item.serialize)

@app.route('/category/JSON')
def categorysJSON():
    categorys = session.query(Category).all()
    return jsonify(categorys= [r.serialize for r in categorys])

#===================
# Main Html pages:
#===================

#Show all categorys, login controlled
@app.route('/')
@app.route('/category')
def showCategorys():
  categorys = session.query(Category).order_by(asc(Category.name))
  if 'email' not in login_session:
    return render_template('categorys_public.html', categorys = categorys)
  else:
    return render_template('categorys.html', categorys = categorys)

#Create a new category
@app.route('/cagetory/new/', methods=['GET','POST'])
def newCategory():

  #---User local permission:
  if 'email' not in login_session:
      return redirect('/login')
  #-------
  if request.method == 'POST':
      newCategory = Category(name = request.form['name'], user_id=login_session['user_id'])
      #newCategory = Category(name = request.form['name'])
      session.add(newCategory)
      flash('New Category %s Successfully Created' % newCategory.name)
      session.commit()
      return redirect(url_for('showCategorys'))
  else:
      return render_template('newCategory.html')

#Edit a category
@app.route('/category/<int:category_id>/edit/', methods = ['GET', 'POST'])
def editCategory(category_id):
  editedCategory = session.query(Category).filter_by(id = category_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedCategory.name = request.form['name']
        flash('Category Successfully Edited %s' % editedCategory.name)
        return redirect(url_for('showCategorys'))
  else:
    return render_template('editCategory.html', category = editedCategory)

#Delete a category
@app.route('/category/<int:category_id>/delete/', methods = ['GET','POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id = category_id).one()

  #------user local permission system
    if categoryToDelete.user_id != login_session['user_id']:
      return "<script>function myFunction(){alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()''>"
  #------user local permission system

    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategorys', category_id = category_id))
    else:
        return render_template('deleteCategory.html',category = categoryToDelete)

#Show a category list, login controlled
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/list/')
def showList(category_id):
    category = session.query(Category).filter_by(id = category_id).one()

    #-------user local permission system
    creator = getUserInfo(category.user_id)
    #-------user local permission    

    items = session.query(ListItem).filter_by(category_id = category_id).all()

    if 'email' not in login_session or creator.id != login_session['user_id']:
        return render_template('list_public.html', items = items, category = category, creator= creator)
    else:
        return render_template('list.html', items = items, category = category, creator= creator)
    #-------user local permission system
    #if 'email' not in login_session:
    #    return render_template('list_public.html', items = items, category = category)
    #else:
    #    return render_template('list.html', items = items, category = category)


#Create a new list item
@app.route('/category/<int:category_id>/list/new/',methods=['GET','POST'])
def newListItem(category_id):
  category = session.query(Category).filter_by(id = category_id).one()
  if request.method == 'POST':
      newItem = ListItem(name = request.form['name'], description = request.form['description'], category_id = category_id, user_id=category.user_id)
      #newItem = ListItem(name = request.form['name'], description = request.form['description'], category_id = category_id)
      session.add(newItem)
      session.commit()
      flash('New List %s Item Successfully Created' % (newItem.name))
      return redirect(url_for('showList', category_id = category_id))
  else:
      return render_template('newlistitem.html', category_id = category_id)


#Edit a list item,login controlled
@app.route('/category/<int:category_id>/list/<int:list_id>/edit', methods=['GET','POST'])
def editListItem(category_id, list_id):

    editedItem = session.query(ListItem).filter_by(id = list_id).one()
    category = session.query(Category).filter_by(id = category_id).one()

    if 'email' not in login_session:
        return render_template('editlistitem_public.html', category_id = category_id, list_id = list_id, item = editedItem)

    else:
        if request.method == 'POST':
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['description']:
                editedItem.description = request.form['description']
            session.add(editedItem)
            session.commit() 
            flash('List Item Successfully Edited')
            return redirect(url_for('showList', category_id = category_id))
        else:
            return render_template('editlistitem.html', category_id = category_id, list_id = list_id, item = editedItem)

#Delete a list item
@app.route('/category/<int:category_id>/list/<int:list_id>/delete', methods = ['GET','POST'])
def deleteListItem(category_id,list_id):
    category = session.query(Category).filter_by(id = category_id).one()
    itemToDelete = session.query(ListItem).filter_by(id = list_id).one() 
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('List Item Successfully Deleted')
        return redirect(url_for('showList', category_id = category_id))
    else:
        return render_template('deletelistitem.html', item = itemToDelete)




if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8080)












