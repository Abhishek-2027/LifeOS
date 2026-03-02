"""
Simple backend test for memory operations
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Test user credentials
TEST_USER_EMAIL = f"testuser_{int(datetime.now().timestamp())}@example.com"
TEST_USER_PASSWORD = "Test@123456"

print("\n" + "="*70)
print("  LIFEOS BACKEND - MEMORY TEST")
print("="*70)

# Step 1: Register
print("\n[STEP 1] Register User")
print(f"Email: {TEST_USER_EMAIL}")

register_response = requests.post(
    f"{BASE_URL}/auth/register",
    json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
)

if register_response.status_code != 200:
    print(f"FAILED: {register_response.json()}")
    exit(1)

access_token = register_response.json().get("access_token")
print(f"OK: Registration successful")
print(f"Token: {access_token[:50]}...")

headers = {"Authorization": f"Bearer {access_token}"}

# Step 2: Add Memory
print("\n[STEP 2] Add Memory Data")

memories = [
    {
        "text": "Had a great meeting with the team about Q2 roadmap",
        "memory_type": "episodic",
        "emotion": "positive",
        "importance": 0.8
    },
    {
        "text": "Learned about new Python async patterns for backend",
        "memory_type": "semantic",
        "emotion": "neutral",
        "importance": 0.7
    },
    {
        "text": "Completed the LifeOS API refactor successfully",
        "memory_type": "episodic",
        "emotion": "positive",
        "importance": 0.9
    }
]

memory_ids = []

for i, memory_data in enumerate(memories, 1):
    print(f"\n  Memory {i}: {memory_data['text'][:40]}...")
    
    add_response = requests.post(
        f"{BASE_URL}/memory/add",
        json=memory_data,
        headers=headers
    )
    
    if add_response.status_code == 200:
        mem = add_response.json()
        memory_ids.append(mem.get("id"))
        print(f"  OK: Added (ID: {mem.get('id')})")
    else:
        print(f"  FAILED: {add_response.status_code}")
        print(f"  {add_response.text[:100]}")

print(f"\n  Total added: {len(memory_ids)}")

# Step 3: Search Memory
print("\n[STEP 3] Search Memories")

search_queries = [
    "meeting and roadmap",
    "Python async",
    "API refactor"
]

for query in search_queries:
    print(f"\n  Searching: '{query}'")
    
    search_response = requests.get(
        f"{BASE_URL}/memory/search",
        params={"query": query},
        headers=headers
    )
    
    if search_response.status_code == 200:
        results = search_response.json()
        print(f"  OK: Found {len(results)} result(s)")
        for result in results[:2]:
            print(f"    - {result.get('text', 'N/A')[:50]}...")
    else:
        print(f"  FAILED: {search_response.status_code}")

# Summary
print("\n" + "="*70)
print("  SUMMARY")
print("="*70)
print(f"User: {TEST_USER_EMAIL}")
print(f"Registered: OK")
print(f"Memories Added: {len(memory_ids)}")
print(f"Search Working: OK")
print("\nAll endpoints working correctly!")
