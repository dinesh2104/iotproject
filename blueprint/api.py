from flask import Blueprint,render_template,redirect,url_for,request,session
from src import get_config
from src.User import User

bp=Blueprint("api",__name__,url_prefix="/api/v1")

@bp.route("/auth",methods=['POST'])
def authenticate():
   if session.get('authenticated'): #TODO: Need more validattion like login expiry
      return {
         "message": "Already Authenticated",
         "authenticated": True
      }, 202
   else:
      if 'username' in request.form and 'password' in request.form:
         username = request.form['username']
         password = request.form['password']
         try:
            sessid=User.login(username, password)
            session['authenticated'] = True
            session['username']=username
            session['sessid']=sessid
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