from flask import Blueprint,render_template,redirect,url_for,request,session
from src import get_config
from src.User import User
from src.Session import Session
from src.Group import Group
from src.Api import Api

bp=Blueprint("profileapi",__name__,url_prefix="/api")

@bp.route("/profile_update/<field>",methods=['POST'])
def updateProfile(field):
    if 'name' in request.form:
        name=request.form['name']
        username=session['username']
        user=User(username)
        if(field=="Name"):
            user.changeName(name)
        return {
            "message": "Successfully Updated",
         }, 200

@bp.route("/profile_update_password",methods=['POST'])
def updateProfilePassword():
    if 'password' in request.form:
        password=request.form['password']
        username=session['username']
        user=User(username)    
        user.changePassword(password)
        return {
            "message": "Successfully Updated",
         }, 200