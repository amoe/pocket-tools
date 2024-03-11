import sys
import requests
from credentials import access_token, consumer_key

# This script batch-adds a list of URLs to a Pocket account.  It's mostly used
# for taking advantage of the Kobo integration.

with open(sys.argv[1]) as f:
    urls = [x.rstrip() for x in f.readlines()]

# for url
# resp = requests.post(
#     'https://getpocket.com/v3/add',
#     json={
#         'consumer_key': CONSUMER_KEY,
#         'access_token': access_token,
#         'url': url,
#     },
#     headers={'X-Accept': 'application/json'}
# )
# x = resp.json()

# print(x)

actions = []
for y in urls:
    actions.append({'action': 'add', 'url': y})

print("Sending", len(actions), "actions")

resp = requests.post(
    'https://getpocket.com/v3/send',
    json={
        'actions': actions,
        'access_token': access_token,
        'consumer_key': consumer_key
    },
    headers={'X-Accept': 'application/json'}
)
print(resp.text)
