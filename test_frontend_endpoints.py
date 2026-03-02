import requests
from datetime import datetime

BASE = 'http://127.0.0.1:8000'

def login_or_register(email, password):
    r = requests.post(BASE + '/auth/register', json={'email': email, 'password': password})
    if r.status_code != 200:
        r = requests.post(BASE + '/auth/login', json={'email': email, 'password': password})
    return r.json().get('access_token')

email = f'test_{int(datetime.now().timestamp())}@example.com'
token = login_or_register(email, 'Password123')
headers = {'Authorization': f'Bearer {token}'}

print('token', token[:40])

# memory add/search
mem = requests.post(BASE + '/memory/add', json={'text':'hello','memory_type':'episodic','emotion':'neutral','importance':0.5}, headers=headers)
print('mem add',mem.status_code, mem.json())
search = requests.get(BASE + '/memory/search', params={'query':'hello'}, headers=headers)
print('mem search',search.status_code, search.json())

# email sync/list
print('sync email', requests.post(BASE + '/emails/sync', headers=headers).status_code)
print('list email', requests.get(BASE + '/emails/', headers=headers).status_code)

# dashboard
db = requests.get(BASE + '/dashboard/overview', headers=headers)
print('dashboard', db.status_code, db.text[:100])

# agents
print('run email agent', requests.post(BASE + '/agents/run-email-agent', headers=headers).status_code)
print('run monitoring agent', requests.post(BASE + '/agents/run-monitoring', headers=headers).status_code)

# reasoning
rs = requests.get(BASE + '/reasoning/analyze', params={'query':'test'}, headers=headers)
print('reasoning', rs.status_code, rs.text[:100])

# document upload test
with open('c:\LifeOS\test_comprehensive.py','rb') as f:
    resp=requests.post(BASE + '/documents/upload', headers=headers, files={'file':f})
    print('doc upload', resp.status_code, resp.text)
