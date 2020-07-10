# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

main_link = 'https://api.github.com/'

user = input('Введите имя пользователя: ')

link = f'{main_link}users/{user}/repos'

response = requests.get(link)
res = json.loads(response.text)

if response.ok:
    for n in res:
        print('Список репозиториев:')
        print(n['name'])


# Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

client_id = 'd566b5c67a9b0ee61ccb'
client_secret = 'bb02b4b58b6101780fcf72a06e9cc7f6'

r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                  data={
                      "client_id": client_id,
                      "client_secret": client_secret
                  })

j = json.loads(r.text)
token = j["token"]

headers = {"X-Xapp-Token" : token}

art = dict()
url = 'https://api.artsy.net/api/artists/{}'

id = ['4ff369de1083d40001002e2d', '506255b93111cc0002000986', '516cc8a89ad2d32bec000538', '524c6fbe8b3b811f42000421',
      '53393f7a275b2458b10004a9', '511294005c85615a61000082', '4d8b92a44eb68a1b2c000328', '4e96f7705554c900010027db',
      '4e96f6e23e43de00010050cb', '4e2ed576477cc70001006f99', '5524173772616947559b0200', '52840714275b2442c8000150',
      '54521f9d7261691cea0f0300', '535842f6c9dc246615000165', '542e86e47261695773da1700']

for i in id:
    r = requests.get(url.format(i), headers=headers)
    data = r.json()
    print('Имя: ', data['sortable_name'], '\nГоды жизни: ', data['birthday'], '-', data['deathday'], '\n')