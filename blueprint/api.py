from flask import Blueprint,render_template,redirect,url_for,request,session
from src import get_config
from src.User import User
from src.Session import Session
from src.Group import Group
from src.Api import Api
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
import hashlib


bp=Blueprint("api",__name__,url_prefix="/api/v1")

@bp.route("/register",methods=['POST'])
def register():
   if 'username' in request.form and 'password' in request.form and 'name' in request.form and 'email' in request.form:
      username = request.form['username']
      password = request.form['password']
      name = request.form['name']
      email = request.form['email']
      #Todo: To check whether user exisit with same name
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
   if session.get('type')=='oauth':
      session.clear()
      return redirect(url_for("home.dashboard"))

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
   
#Image Upload Api
UPLOAD_FOLDER = '/home/dineshsdk21/Example/iotweb/assets/images/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def md5_hash(input_string):
    # Create an MD5 hash object
   md5 = hashlib.md5()

    # Encode the input string as bytes and update the hash object
   md5.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the MD5 hash
   hashed_string = md5.hexdigest()

   return hashed_string

@bp.route('/upload', methods=['POST'])
def upload_file():
   username=session['username']
   if request.method == 'POST':
      if 'file' not in request.files:
         return {
         "message": "File Not provided"
         }, 200
      file = request.files['file']  
      if file.filename == '':
            return{
            "message": "No file Selected"
            }, 200
      if file and allowed_file(file.filename):
         filename = md5_hash(username);
         file.save(os.path.join(UPLOAD_FOLDER, filename))
         user=User(username)
         user.changeImageUrl("/images/profiles/"+filename)
         return {
         "message": "Profile Image Uploaded Successfully",
         "path":filename
         }, 200
      
@bp.route('/file/<filename>')
def uploaded_file(filename):
   filename = secure_filename(filename)
   return send_from_directory(UPLOAD_FOLDER,filename)