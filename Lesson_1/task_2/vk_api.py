import requests
import json

response = requests.get('https://api.vk.com/method/groups.get?user_id=21709724&v=5.131\
            &access_token=6e57becf832cadd4d9e21b57f7c348cb57ce29539428a381c106b761105fe000b5c22f314e7a4a9bef67d')

j_data = response.json()

with open("vk_groups.json", 'w') as f:
    json.dump(j_data, f)

print(j_data['response']['items'])
