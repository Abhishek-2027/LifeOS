"""
Initialize SQLite database for LifeOS backend testing
"""

import asyncio
import sqlite3
from pathlib import Path

DB_PATH = Path("backend/lifeos.db")

def init_database():
    """Create SQLite tables for testing"""
    
    # Connect to SQLite
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print(f"🔧 Initializing database at {DB_PATH}...")
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("✅ Created 'users' table")
    
    # Create memories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        text TEXT NOT NULL,
        memory_type VARCHAR(50) NOT NULL,
        emotion VARCHAR(50),
        importance REAL DEFAULT 0.5,
        embedding BLOB,
        meta_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    print("✅ Created 'memories' table")
    
    # Create documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename VARCHAR(255) NOT NULL,
        file_path VARCHAR(500),
        content TEXT,
        extracted_text TEXT,
        metadata TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    print("✅ Created 'documents' table")
    
    # Create emails table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        from_email VARCHAR(255),
        to_email VARCHAR(255),
        subject VARCHAR(500),
        body TEXT,
        snippet TEXT,
        gmail_id VARCHAR(255),
        labels TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    print("✅ Created 'emails' table")
    
    # Create agent_logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        agent_name VARCHAR(100),
        action VARCHAR(500),
        result TEXT,
        status VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    print("✅ Created 'agent_logs' table")
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"\n✅ Database initialized successfully at {DB_PATH}")
    print(f"\n📊 Database file size: {DB_PATH.stat().st_size} bytes")

if __name__ == "__main__":
    init_database()
