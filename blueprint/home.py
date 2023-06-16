from flask import Blueprint,render_template,redirect,url_for,request,session

bp=Blueprint("home",__name__,url_prefix="/")

@bp.route('/dashboard')
def dashboard():
   return render_template("dashboard.html",session=session)

@bp.route('/')
def index():
   return render_template("dashboard.html",session=session)
