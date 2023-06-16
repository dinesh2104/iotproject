import sys
sys.path.append("/home/dineshsdk21/Example/iotweb/")

from flask import Flask,render_template,session,request,redirect,url_for
from src import get_config
from src.User import User
from blueprint import home,api,files

application=app = Flask(__name__,static_folder="assets",static_url_path="/")
app.secret_key=get_config('secret_key') 
app.register_blueprint(home.bp)
app.register_blueprint(api.bp)
app.register_blueprint(files.bp)


@app.route("/error")
def error():
   return render_template("error.html")

@app.route("/test")
def test():
   return render_template("test.html")

@app.route("/reset-password")
def resetPassword():
   return render_template("reset-password.html")

@app.route("/settings")
def setting():
   return render_template("setting.html")

@app.route("/notification")
def notification():
   return render_template("notification.html")

@app.route("/account")
def account():
   return render_template("accountDetail.html")



@app.route('/signup')
def signup():
   return render_template("signup.html",session=session)

   

if __name__ == '__main__':
   app.run(host='172.20.15.58',debug=True)