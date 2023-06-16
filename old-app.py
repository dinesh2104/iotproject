from flask import Flask,render_template
import os
from src.User import User
app = Flask(__name__)
basename='/iotcloud'

@app.route('/hello')
def hello_world():
   return render_template("index.html")

@app.route('/')
def h_world():
   return 'Hello Worl12d'

@app.route(basename+'/')
def whoami():
    return "<pre>"+os.popen('cat /proc/cpuinfo').read()+"</pre>"

@app.route(basename+"/echo/<string>")
def echo(string):
   return string

if __name__ == '__main__':
   app.run(host='172.20.15.58',debug=True)