"""
Test script to add and fetch data from LifeOS backend
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Test user credentials
TEST_USER_EMAIL = f"testuser_{int(datetime.now().timestamp())}@example.com"
TEST_USER_PASSWORD = "Test@123456"

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def print_response(label, response):
    print(f"\n[{label}]")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

# ============= TEST 1: REGISTER USER =============
print_section("TEST 1: Register User")
print(f"Email: {TEST_USER_EMAIL}")
print(f"Password: {TEST_USER_PASSWORD}")

register_response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
)
print_response("Register", register_response)

if register_response.status_code != 200:
    print("\n❌ Registration failed!")
    exit(1)

access_token = register_response.json().get("access_token")
print(f"\n✅ User registered successfully!")
print(f"Access Token: {access_token[:50]}...")

# ============= TEST 2: LOGIN USER =============
print_section("TEST 2: Login User")

login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
)
print_response("Login", login_response)

if login_response.status_code != 200:
    print("\n❌ Login failed!")
    exit(1)

access_token = login_response.json().get("access_token")
print(f"\n✅ User logged in successfully!")

# ============= TEST 3: ADD MEMORY DATA =============
print_section("TEST 3: Add Memory Data")

headers = {"Authorization": f"Bearer {access_token}"}

test_memories = [
    {
        "text": "Had a great meeting with the team about Q2 roadmap",
        "memory_type": "episodic",
        "emotion": "positive",
        "importance": 0.8
    },
    {
        "text": "Learned about new Python async patterns for backend optimization",
        "memory_type": "semantic",
        "emotion": "neutral",
        "importance": 0.7
    },
    {
        "text": "Completed the LifeOS API refactor to remove dependency conflicts",
        "memory_type": "episodic",
        "emotion": "positive",
        "importance": 0.9
    }
]

memory_ids = []

for i, memory_data in enumerate(test_memories, 1):
    print(f"\n--- Adding Memory {i} ---")
    print(f"Text: {memory_data['text'][:60]}...")
    
    add_response = requests.post(
        f"{BASE_URL}/memory/add",
        json=memory_data,
        headers=headers
    )
    print_response(f"Add Memory {i}", add_response)
    
    if add_response.status_code == 200:
        memory_id = add_response.json().get("id")
        memory_ids.append(memory_id)
        print(f"✅ Memory added successfully! ID: {memory_id}")
    else:
        print(f"❌ Failed to add memory {i}")

# ============= TEST 4: SEARCH MEMORIES =============
print_section("TEST 4: Search Memories")

search_queries = [
    "meeting and roadmap",
    "Python async",
    "API refactor"
]

for query in search_queries:
    print(f"\n--- Searching for: '{query}' ---")
    
    search_response = requests.get(
        f"{BASE_URL}/memory/search",
        params={"query": query},
        headers=headers
    )
    print_response(f"Search Results for '{query}'", search_response)
    
    if search_response.status_code == 200:
        results = search_response.json()
        print(f"✅ Search returned {len(results)} result(s)")
        for result in results:
            print(f"   - {result.get('text', 'N/A')[:60]}... (Similarity: {result.get('similarity_score', 'N/A')})")
    else:
        print(f"❌ Search failed!")

# ============= SUMMARY =============
print_section("TEST SUMMARY")
print(f"✅ Successfully registered and logged in user: {TEST_USER_EMAIL}")
print(f"✅ Added {len(memory_ids)} memory records")
print(f"✅ Searched and retrieved memory records")
print(f"\n🎉 All tests completed!")
