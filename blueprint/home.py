from flask import Blueprint,render_template,redirect,url_for,request,session
from src.Api import Api
from src.Group import Group
from src import md5_hash, time_ago, mask

bp=Blueprint("home",__name__,url_prefix="/")

@bp.route('/dashboard')
def dashboard():
   return render_template("dashboard.html",session=session)

@bp.route('/')
def index():
   return render_template("dashboard.html",session=session)

@bp.route("/api_keys")
def api_keys():
   groups = list(Group.get_groups())
   api_keys = Api.get_all_keys(session)
   return render_template('apikey.html', session=session, api_keys=api_keys, groups=groups, time_ago=time_ago, mask=mask)

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
