import sys
sys.path.append("/home/dineshsdk21/Example/iotweb/")

from flask import Flask,render_template,session,request,redirect,url_for
from src import get_config
from src.User import User
from blueprint import home,api,files,motion,dialogs,oauth,profile_api
from src.Api import Api
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token


application=app = Flask(__name__,static_folder="assets",static_url_path="/")
app.secret_key=get_config('secret_key') 
app.register_blueprint(home.bp)
app.register_blueprint(api.bp)
app.register_blueprint(files.bp)
app.register_blueprint(motion.bp)
app.register_blueprint(dialogs.bp)
app.register_blueprint(oauth.bp)
app.register_blueprint(profile_api.bp);


@app.before_request
def before_request_hook():
   if session.get('type') == 'web':
      return
   
   if session.get('type')=='oauth':
      return
   
   auth_header = request.headers.get('Authorization')
   if auth_header:
      auth_token = auth_header.split(" ")[1]
      print(auth_token)
      try:
         api = Api(auth_token)
         session['authenticated'] = api.is_valid()
         session['username'] = api.collection.username
         session['type'] = 'api'
         session['sessid'] = None
      except Exception as e:
         return "Unauthorized: "+str(e), 401
   else:
      session['authenticated'] = False
      if 'username' in session:
         del session['username']



@app.route("/error")
def error():
   return render_template("error.html")

@app.route("/test")
def test():
   return render_template("test.html")
   

if __name__ == '__main__':
   app.run(host='172.20.15.58',debug=True)