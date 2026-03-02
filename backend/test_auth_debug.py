"""
Debug auth service directly to see actual error
"""

import asyncio
import sqlite3
from pathlib import Path

async def test_auth():
    # Patch the database to use sync instead of async
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Create a sync engine instead
    engine = create_engine("sqlite:///backend/lifeos.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        from app.schemas.user_schema import UserCreate
        from app.services.auth_service import AuthService
        
        user_data = UserCreate(email="debug@test.com", password="Test@1234")
        
        print(f"Attempting to register user: {user_data.email}")
        
        # Call register synchronously
        result = AuthService.register(db, user_data)
        print(f"Registration result: {result}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_auth())
