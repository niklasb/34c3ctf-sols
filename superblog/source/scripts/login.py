import requests
import re

def login(username, pw, url):
    s = requests.Session()
    s.get(url + '/login/')
    tok = s.cookies['csrftoken']
    s.post(url + '/login/', data=dict(
        username=username,
        password=pw,
        csrfmiddlewaretoken=tok))
    return s.cookies['sessionid']

if __name__ == '__main__':
    print login('admin', 'eevii0et8em7wei9Tahw', 'http://localhost:1342')
