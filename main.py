import flask
import requests
from six.moves import urllib
import ssl

app = flask.Flask('app')

# Load config object from config.py
app.config.from_object('config.Config')


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/authorize')
def authorize():
    ADOBE_AUTH_URL = 'https://ims-na1.adobelogin.com/ims/authorize?'

    params = {
        'client_id': app.config['ADOBE_API_ID'],
        'scope': 'openid',
        'response_type': 'code',
        'redirect_uri': flask.url_for('callback', _external=True)
    }

    return flask.redirect(ADOBE_AUTH_URL + urllib.parse.urlencode(params))


@app.route('/callback')
def callback():
  authorization_code = flask.request.args.get('code')

  ADOBE_TOKEN_URL = 'https://ims-na1.adobelogin.com/ims/token'

  params = {
    'grant_type': 'authorization_code',
    'client_id': app.config['ADOBE_API_ID'],
    'client_secret': app.config['ADOBE_API_SECRET'],
    'code': authorization_code
  }

  response = requests.post(ADOBE_TOKEN_URL,
    params = params,
    headers = {'content-type': 'application/x-www-form-urlencoded'})

  if response.status_code == 200:
    flask.session['credentials'] = response.json()
    return flask.render_template('index.html', response='login success')
  else:
    return flask.render_template('index.html', response='login failed')

# app.run(host='0.0.0.0', port=8080)

app.run(host='0.0.0.0', port=8080)

# app.run(host='0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'))


# Make sure the hostname and port you provide match the valid redirect URI
# specified in your project in the Adobe developer Console. 
# Also, make sure to have `cert.pem` and `key.pem` in your directory
# app.run(host='0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'))