from flask import Blueprint,render_template,redirect,url_for,request,session
from src.Api import Api
from src.User import User
from src.Group import Group
from src import md5_hash, time_ago, mask

bp=Blueprint("home",__name__,url_prefix="/")

@bp.route('/dashboard')
def dashboard():
   user=User(session['username']).collection
   return render_template("dashboard.html",session=session,user=user)

@bp.route('/')
def index():
   user=User(session['username']).collection
   return render_template("dashboard.html",session=session,user=user)

@bp.route("/reset-password")
def resetPassword():
   return render_template("reset-password.html")

# @bp.route("/settings")
# def setting():
#    return render_template("setting.html")

@bp.route("/notification")
def notification():
   user=User(session['username']).collection
   return render_template("notification.html",user=user)

@bp.route("/account")
def account():
   user=User(session['username']).collection
   return render_template("accountDetail.html",user=user)


@bp.route('/signup')
def signup():
   return render_template("signup.html",session=session)

#Email confirmation route
@bp.route("/confirm/<token>")
def confirm_email(token):
   email = User.confirm_token(token)
   try:
      currentUser=User(email).collection
      if currentUser['active'] and currentUser['activate_token']==token:
         return "Account already confirmed."
      elif currentUser['activate_token']!=token:
         return "The confirmation link is invalid or has expired."
      currentUser['active']=True
      print(currentUser)
      return ("You have confirmed your account. Thanks!")
   except Exception as e:
      return "The confirmation link is invalid or has expired."
   return redirect(url_for("home.dashborad"))

#Other Apis

@bp.route("/api_keys")
def api_keys():
   user=User(session['username']).collection
   groups = list(Group.get_groups())
   api_keys = Api.get_all_keys(session)
   return render_template('apikey.html', session=session, api_keys=api_keys, groups=groups, time_ago=time_ago, mask=mask,user=user)

@bp.route("/api_keys/row")
def api_keys_row():
   api_key_hash = request.args.get('hash')
   api = Api(api_key_hash)
   groups = Group.get_groups()
   return render_template('api_key/api_key_rows.html', key=api.collection._data, groups=groups, time_ago=time_ago, mask=mask)

@bp.route("/api_keys/row/delete_dialog")
def api_keys_delete_dialog():
   api_key_hash = request.args.get('hash')
   api = Api(api_key_hash)
   return render_template('dialogs/delete_api_key.html', key=api.collection._data, time_ago=time_ago, mask=mask)

# To fetch content for dialog to delete group 
@bp.route("/api_group/delete/dialog")
def api_group_delete_dialog():
   group = list(Group.get_groups())
   print(group)
   return render_template('dialogs/delete_group.html', groups=group)

# To delete the group
@bp.route("/api_group/delete")
def api_group_delete():
   grp_id = request.args.get('hash')
   grp=Group.deleteGroup(grp_id)
   return {
      'status': grp
   }, 200

@bp.route("/api_keys/row/delete")
def api_keys_delete():
   api_key_hash = request.args.get('hash')
   api = Api(api_key_hash)
   api.delete()
   return {
      'status': 'success'
   }, 200

@bp.route("/api_keys/enable", methods=['POST'])
def enable_api_key():
   api_key_hash = request.form['id']
   api_key_status = request.form['status']
   print(bool(api_key_status))
   api = Api(api_key_hash)
   api.collection.active = api_key_status == "true"
   return {
      'status': api.collection.active
   }, 200


@bp.route("/api_profile/update/<field>")
def showUpdateNameTemplate(field):
   return render_template('profile/profile_update.html',field=field)

@bp.route("/api_profile/update_password")
def showUpdatePasswordTemplate():
   return render_template('profile/profile_password.html');

@bp.route("/api_profile/update_image")
def showImageUploadTemplate():
   return render_template('profile/imageupload.html');