# "Hello World" Python Sample

Demo application to get started with Tetra Pak APIs

In particular the script uses two important libraries

- Flask - a simple API/Web development framework
- WebApplicationClient - lib to perform oAuth authentication

## Prerequisites

- Python installed
- Pip installed

## To Use

1. To install dependencies run: `pip install -r requirements.txt`
2. Go to developer.tetrapak.com and register an account
3. In the portal. Create a new application.

    3.1. Store Client ID and Client Secret in environment variable; TP_HELLO_WORLD_APP_DEV_CLIENT_ID,       TP_HELLO_WORLD_APP_DEV_CLIENT_SECRET

    3.2. Configure the callback URL for the application to <https://127.0.0.1:5000/login/callback>

4. Run this demo application: `python appTPauth.py`
5. Access using your browser <https://127.0.0.1:5000>

To read more about OAuth visit
<https://developer.tetrapak.com/products/tetra-pak-enterprise-security/introduction-oauth>

The script is inspired by the following blog post
<https://realpython.com/flask-google-login/>
