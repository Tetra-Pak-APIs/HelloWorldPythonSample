# Demo application to get started with Tetra Pak APIs 
#
# In particular the script uses two importana libraries
# - Flask - a simple API/Web development frameword
# - WebApplicationClient - lib to performe oAuth authentication
#
# To Use:
# 0. To install dependencies run: pip install -r requirements.txt
# 1. Go to developer.tetrapak.com and register an account
# 2. In the portal. Create a new application.
# 2.1 Store Client ID and Client Secret in environmet variable; TP_HELLO_WORLD_APP_DEV_CLIENT_ID, 
#       TP_HELLO_WORLD_APP_DEV_CLIENT_SECRET
# 2.2 Configure the callback URL for the application to https://127.0.0.1:5000/login/callback
# 3 Run this demo application: python appTPauth.py
# 4 Access using your browser https://127.0.0.1:5000
#
# To read more about oAuth visit 
# https://developer.tetrapak.com/documentation/introduction-oauth
#
# The script is inspired by the following blog post
# https://realpython.com/flask-google-login/
# -----------------------------------------------------------------------------------------------------------


# Python standard libraries
import json
import os

# Third-party libraries
from flask import Flask, redirect, request, url_for, jsonify
from oauthlib.oauth2 import WebApplicationClient
import requests

# Configuration
TP_CLIENT_ID = os.environ.get("TP_HELLO_WORLD_APP_DEV_CLIENT_ID", None)
TP_CLIENT_SECRET = os.environ.get("TP_HELLO_WORLD_APP_DEV_CLIENT_SECRET", None)

if TP_CLIENT_ID == None:
    print("ERROR - Env variable TP_HELLO_WORLD_APP_DEV_CLIENT_ID not set")
if TP_CLIENT_SECRET == None:
    print("ERROR - Env variable TP_HELLO_WORLD_APP_DEV_CLIENT_SECRET not set")

TP_AUTHORIZATION_EDNPOINT = "https://api.tetrapak.com/oauth2/authorize"
TP_TOKEN_ENDPOINT = "https://api.tetrapak.com/oauth2/token"
TP_HELLOWORLD_ENDPOINT_URL= "https://api.tetrapak.com/samples/helloworld"

# Flask setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# OAuth 2 client setup
client = WebApplicationClient(TP_CLIENT_ID)

# Routes
# Start the flow by accessing this endpoint
@app.route("/")
def index():
    return '<a class="button" href="/login">Authenticate and send request to Tetra Pak HelloWorld API</a>'


# login - endpoint
## Redirect the browser to the Auth-server Authorize endpoint.
### Redirect URL - auth server will redirect browser to this (local) URL when auth is done. 
### Scope "openid" (only supported currently)
@app.route("/login")
def login():
    # Use library to construct the request for Tetra Pak login and provide
    request_uri = client.prepare_request_uri(
        TP_AUTHORIZATION_EDNPOINT,
        redirect_uri=request.base_url + "/callback",
        scope=["openid"]
    )
    return redirect(request_uri)

# login/callback - endpoint
## Recieve call on the callback. Redirect from Auth-server. Parse out the code argument.
## Call TokenExchange endpoint
## Call the HelloWorld endpoint using obtained credentials
## Render the result
@app.route("/login/callback")
def callback():
    # Get authorization code
    code = request.args.get("code")

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        TP_TOKEN_ENDPOINT,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(TP_CLIENT_ID, TP_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Make request to the HelloWorld API
    uri, headers, body = client.add_token(TP_HELLOWORLD_ENDPOINT_URL)
    helloworld_response = requests.get(uri, headers=headers, data=body)

    t = helloworld_response.text
    return t

@app.route("/test")
def test():
    n = {"FirstName": "Fredrik", "LastName": "Lofgren"}
    o = {"Name": n, "Say": 'Hello World!'}
    return jsonify(o)

if __name__ == "__main__":
    app.run(ssl_context="adhoc")