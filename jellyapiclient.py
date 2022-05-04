import json
import requests

API_KEY = '48ed9a373062474a8ed04a4a8602b600'
header = {'X-Emby-Token':API_KEY}
response = requests.get('http://192.168.1.3:8096/Items',headers=header, params={'userId':'e726513ac7224e8895ea76e5d5028aa1','parentId':'f137a2dd21bbc1b99aa5c0f6bf02a805'})
print(response.status_code)
print(response.url)
print(response.headers)
print(response.content)