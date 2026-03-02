"""
Direct database test - bypass SQLAlchemy to check SQLite connection
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("backend/lifeos.db")

print(f"Testing direct SQLite connection...")
print(f"Database path: {DB_PATH}")
print(f"Database exists: {DB_PATH.exists()}")

try:
    # Test direct SQLite connection
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nTables in database:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Test inserting a user
    print(f"\nTesting user insertion...")
    cursor.execute("""
        INSERT INTO users (email, hashed_password, is_active)
        VALUES (?, ?, ?)
    """, ('testdirect@example.com', 'hashed_pwd_123', True))
    
    conn.commit()
    print(f"✓ User inserted successfully!")
    
    # Verify insertion
    cursor.execute("SELECT COUNT(*) FROM users;")
    count = cursor.fetchone()[0]
    print(f"✓ Total users in database: {count}")
    
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
