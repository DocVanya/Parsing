import requests
import json
from pprint import pprint

headers = {'authorization': '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',
           'accept': 'application/vnd.github.v3+json'}
username = 'DocVanya'
url = f'https://api.github.com/users/{username}/repos'

response = requests.get(url, headers=headers)
j_data = response.json()

# pprint(j_data)

repo = []
for i in j_data:
    repo.append(i['name'])

print(repo)

with open('github_groups.json', 'w') as f:
    json.dump(repo, f)
