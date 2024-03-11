import requests
from flask import Flask, redirect, session
import pdb
from credentials import access_token, consumer_key

app = Flask(__name__)
app.secret_key = 'nonesuch'

REDIRECT_URI = 'http://localhost:5000/callback'
BATCH_SIZE = 1000    # max 5000

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    print("foo")


    resp = requests.post('https://getpocket.com/v3/oauth/request', json={
        'consumer_key': consumer_key,
        'redirect_uri': REDIRECT_URI,
        'state': 'nonesuch',
    }, headers={'X-Accept': 'application/json'})
    data = resp.json()
    request_token = data['code']
    session['request_token'] = request_token


    uri = f'https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri={REDIRECT_URI}'
    
    return redirect(uri)



@app.route("/callback")
def callback():
    print("using request token", session['request_token'])
    resp = requests.post(
        'https://getpocket.com/v3/oauth/authorize',
        json={
            'consumer_key': consumer_key,
            'code': session['request_token']
        },
        headers={'X-Accept': 'application/json'}
    )

    print("Status code for authorize was", resp.status_code)
    print(resp.headers)
    
    result = resp.json()
    print(result)
    access_token = result['access_token']
    print("Access token is", access_token)

    # resp = requests.post(
    #     'https://getpocket.com/v3/get',
    #     json={
    #         'consumer_key': consumer_key,
    #         'access_token': access_token,
    #         'state': 'unread',
    #         'sort': 'oldest',
    #         'detailType': 'simple',
    #         'count': BATCH_SIZE,
    #     }
    # )
    # x = resp.json()
    # actions = []
    # for y in x['list'].keys():
    #     actions.append({'action': 'archive', 'item_id': y})

    # print("Sending", len(actions), "actions")

    # resp = requests.post(
    #     'https://getpocket.com/v3/send',
    #     json={
    #         'actions': actions,
    #         'access_token': access_token,
    #         'consumer_key': consumer_key
    #     }
    # )
    # print(resp.text)
                  
    
    return f"<p>Access token is {access_token}</p>"
    
