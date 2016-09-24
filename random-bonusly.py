import json
from httplib2 import Http
from urllib import urlencode
import random
from subprocess import check_output


def read_config(file):
    with open(file) as data_file:
        return json.load(data_file)


def retrieve_users():
    resp, content = h.request(request_uri, "GET")

    users_json = json.loads(content)

    users = []
    for user in users_json['result']:
        users.append(user['username'])

    return users


def select_winner(users):
    return random.choice(users)


def get_quote():
    return check_output(["fortune", "startrek"])


def create_bonus(winner):
    quote = get_quote()
    return '+1 @%s %s #why-so-serious'%(winner, quote)


def post_bonus(bonus):
    uri = 'https://bonus.ly/api/v1/bonuses?access_token=%s'%_API_TOKEN
    data = dict(reason=bonus)
    return h.request(uri, "POST", urlencode(data))

h = Http()

data = read_config('config/secrets.json')

_API_TOKEN = data['token']

api_url = 'bonus.ly/api/v1/'
users_endpoint = 'users'
request_uri = 'https://%s%s?access_token=%s'%(api_url,users_endpoint,_API_TOKEN)

users = retrieve_users()


winner = select_winner(users)

bonus = create_bonus(winner)

print bonus

post_bonus(bonus)
