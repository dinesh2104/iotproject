from flask import Blueprint,render_template,redirect,url_for,request,session
from src import get_config
from src.User import User
from src.Session import Session
from src.Group import Group
from src.Api import Api

bp=Blueprint("api",__name__,url_prefix="/api/v1")

@bp.route("/register",methods=['POST'])
def register():
   if 'username' in request.form and 'password' in request.form and 'name' in request.form and 'email' in request.form:
      username = request.form['username']
      password = request.form['password']
      name = request.form['name']
      email = request.form['email']
      try:
         uid = User.register(username, password, password, name, email)
         return {
            "message": "Successfully Registered",
            "user_id": uid
         }, 200
      except Exception as e:
         return {
            "message": str(e),
         }, 400
   else:
      return {
         "message": "Not enough parameters",
      }, 400


@bp.route("/create/key", methods=['POST'])
def generate_api_key():
   name = request.form['name']
   group = request.form['group']
   remarks = request.form['remarks']
   
   if session.get('authenticated'): #TODO: Need more validattion like login expiry
      apikeyid = Api.register_apikey(session, name, group, remarks)
      h=Api(apikeyid).collection.hash
      return {
         "key": apikeyid,
         "hash":h,
         "message": "Success"
      }, 200
   else:
      return {
         "message": "Not Authenticated",
      }, 401
   
@bp.route("/create/group", methods=['POST'])
def create_group():
   name = request.form['name']
   description = request.form['description']
   if(len(name) < 3) or (len(description) < 3):
      return {
         "message": "Name and Description must be atleast 3 characters",
      }, 400
   if session.get('authenticated'): #TODO: Need more validattion like login expiry
      Group.register_group(name, description)
      return {
         "status": "success",
         "message": "Successfully created group " + name,
      }, 200
   else:
      return {
         "message": "Not Authenticated",
      }, 401


@bp.route("/auth",methods=['POST'])
def authenticate():
   if session.get('authenticated'): #TODO: Need more validattion like login expiryw
      sess_id=session['sessid'];
      user_session=Session(sess_id);
      if(user_session.isValid()):
         return {
            "message": "Already Authenticated",
            "authenticated": True
         }, 202
      else:
         session['authenticated']=False
         user_session.collection.active = False
         return {
            "message": "Session Expired",
            "authenticated": "False"
         }, 401
   else:
      if 'username' in request.form and 'password' in request.form:
         username = request.form['username']
         password = request.form['password']
         try:
            sessid=User.login(username, password,request)
            session['authenticated'] = True
            session['username']=username
            session['sessid']=sessid
            session['type']='web'
            # return {
            #    "message": "Successfully Authenticated",
            #    "authenticated": True
            # }, 200
            if 'redirect' in request.form and request.form['redirect']==True:
               return redirect(url_for('home.dashboard'))
            else:
               
               return {
                  "message": "Successfully Authenticated",
                  "authenticated": True
               }, 200

         except Exception as e:
            return {
               "message": str(e),
               "authenticated": False
            }, 401
      else:
         return {
            "message": "Not enough parameters",
            "authenticated": False
         }, 400

@bp.route("/deauth")
def deauth():
   if session.get('authenticated'): #TODO: Need more validattion like login expiry
      #Remove / invalidate session from database
      sid=session['sessid']
      Session(sid).collection.delete()
      session['authenticated'] = False
      
      
      # return {
      #    "message": "Successfully Deauthed",
      #    "authenticated": False
      # }, 200
      return redirect(url_for('home.dashboard'))
   else:
      return {
         "message": "Already deauthenticated",
         "authenticated": False
      }, 200