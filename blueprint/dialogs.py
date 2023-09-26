from flask import Blueprint,render_template,redirect,url_for,request,session
from src import get_config
from src.User import User
from src.Session import Session
from src.Group import Group

bp=Blueprint("dialog",__name__,url_prefix="/api/dialogs")

@bp.route('/api_keys')
def showApiKey():
    groups=Group.get_groups()
    return render_template('dialogs/api_key.html', session=session, groups=groups)
