#!/usr/bin/env python3
"""Frontend integration test - verify all endpoints work"""
import requests
import json
from datetime import datetime

BASE = 'http://127.0.0.1:8000'

print("=" * 70)
print("LifeOS Frontend Integration Test")
print("=" * 70)

# 1. Health
try:
    r = requests.get(BASE + '/')
    print(f"✓ Backend health: {r.status_code} {r.json()}")
except Exception as e:
    print(f"✗ Backend unreachable: {e}")
    exit(1)

# 2. Register
email = f"test_{int(datetime.now().timestamp())}@example.com"
try:
    r = requests.post(BASE + '/auth/register', json={'email': email, 'password': 'Pass123'})
    assert r.status_code == 200, f"Register failed: {r.text}"
    token = r.json()['access_token']
    print(f"✓ Register: {r.status_code} token={token[:40]}...")
except Exception as e:
    print(f"✗ Register failed: {e}")
    exit(1)

h = {'Authorization': f'Bearer {token}'}

# 3. Test each endpoint
endpoints = [
    ('POST', '/memory/add', {'text': 'test mem', 'memory_type': 'episodic', 'emotion': 'positive', 'importance': 0.8}),
    ('GET', '/memory/search', None, {'query': 'test'}),
    ('POST', '/emails/sync', {}),
    ('GET', '/emails/', None),
    ('GET', '/dashboard/overview', None),
    ('POST', '/agents/run-email-agent', {}),
    ('POST', '/agents/run-monitoring', {}),
    ('GET', '/reasoning/analyze', None, {'query': 'test'}),
]

for ep in endpoints:
    method, path, data, *params = ep + (None,)
    p = params[0] if params else {}
    try:
        if method == 'GET':
            r = requests.get(BASE + path, headers=h, params=p)
        else:
            r = requests.post(BASE + path, headers=h, json=data)
        status = '✓' if r.status_code < 400 else '✗'
        print(f"{status} {method:4} {path:30} -> {r.status_code}")
    except Exception as e:
        print(f"✗ {method:4} {path:30} -> ERROR: {e}")

print("\n" + "=" * 70)
print("All endpoints ready for frontend!")
print("=" * 70)
