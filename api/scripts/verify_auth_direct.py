from app.services import AuthService, jwt
from app.db import SessionLocal
from app.models import User, SessionToken
from app.schemas import UserCreate
from datetime import datetime, timedelta

db = SessionLocal()

def test_stateful_auth():
    email = f"test_direct_{datetime.now().timestamp()}@example.com"
    password = "password"
    
    # 1. Create user
    user_in = UserCreate(email=email, password=password)
    user = AuthService.create_user(db, user_in)
    
    # 2. Create token
    token = AuthService.create_access_token(db, data={"sub": user.id})
    print(f"Token created: {token[:20]}...")
    
    # 3. Validate (should work)
    user_id = AuthService.validate_session(db, token)
    assert user_id == user.id
    print("✓ Validation works")
    
    # 4. Logout (delete from DB)
    AuthService.logout(db, token)
    print("✓ Logged out (deleted from DB)")
    
    # 5. Validate again (should FAIL)
    user_id = AuthService.validate_session(db, token)
    assert user_id is None
    print("✓ Validation REJECTED after logout as expected")

if __name__ == "__main__":
    try:
        test_stateful_auth()
        print("\nDIRECT AUTH SERVICE VERIFIED")
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
