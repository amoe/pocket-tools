import requests
from credentials import access_token, consumer_key

BATCH_SIZE = 1000

resp = requests.post(
    'https://getpocket.com/v3/get',
    json={
        'consumer_key': consumer_key,
        'access_token': access_token,
        'state': 'unread',
        'sort': 'oldest',
        'detailType': 'simple',
        'count': BATCH_SIZE,
    }
)
x = resp.json()

itemids = sorted(list(x['list'].keys()), reverse=True)
print("max itemid is", itemids[0])

#993768474


actions = []
for y in x['list'].keys():
    actions.append({'action': 'archive', 'item_id': y})

print("Sending", len(actions), "actions")

resp = requests.post(
    'https://getpocket.com/v3/send',
    json={
        'actions': actions,
        'access_token': access_token,
        'consumer_key': consumer_key
    }
)
print(resp.text)
