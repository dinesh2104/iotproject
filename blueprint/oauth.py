from flask import Blueprint,render_template,redirect,url_for,request,session
from src import get_config
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from flask import current_app

bp=Blueprint("oauth",__name__,url_prefix="")

#Oauth
oauth=OAuth(current_app)

@bp.route("/google")
def google():
    GOOGLE_CLIENT_ID = get_config("client_id")
    GOOGLE_CLIENT_SECRET =get_config("client_secret")

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
     
    # Redirect to google_auth function
    redirect_uri = url_for('oauth.google_auth', _external=True)
    session['nonce'] = generate_token()
    return oauth.google.authorize_redirect(redirect_uri,nonce=session['nonce']) 

@bp.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token,nonce=session['nonce'])
    session['google_token']=token['access_token']
    session['username']=user['email']
    session['user']=user
    session['type']='oauth'
    session['authenticated']=True
    return redirect('/')

