import requests
from datetime import datetime

BASE = 'http://127.0.0.1:8000'
email = f'test_{int(datetime.now().timestamp())}@example.com'

# register
r = requests.post(BASE + '/auth/register', json={'email': email, 'password': 'Password123'})
token = r.json().get('access_token')
h = {'Authorization': f'Bearer {token}'}

# test all endpoints
tests = [
    ('POST', '/memory/add', {'text':'test','memory_type':'episodic','emotion':'neutral','importance':0.5}),
    ('GET', '/memory/search', None, {'query': 'test'}),
    ('POST', '/emails/sync', {}),
    ('GET', '/emails/', None, {}),
    ('GET', '/dashboard/overview', None, {}),
    ('POST', '/agents/run-email-agent', {}),
    ('POST', '/agents/run-monitoring', {}),
    ('GET', '/reasoning/analyze', None, {'query': 'test'}),
]

for test in tests:
    method = test[0]
    path = test[1]
    body = test[2] if len(test) > 2 else None
    params = test[3] if len(test) > 3 else {}
    
    if method == 'GET':
        r = requests.get(BASE + path, headers=h, params=params)
    else:
        r = requests.post(BASE + path, headers=h, json=body)
    
    print(f'{method:4} {path:30} -> {r.status_code}')
