import time
import random
import string
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from backend.main import app
from backend.database import engine
from backend import crud


def random_email():
    return f"test+{int(time.time())}{random.randint(0,9999)}@example.com"


def test_forgot_and_reset_flow():
    client = TestClient(app)

    email = random_email()
    password = 'Initial1'
    new_password = 'Newpass1'

    # create test user in DB
    with Session(engine) as session:
        user = crud.create_user(session, nome='Test User', email=email, senha=password, genero='F')

    try:
        # Request reset code
        resp = client.post('/api/auth/forgot-password', json={'email': email})
        assert resp.status_code == 200
        body = resp.json()

        # In development mode the endpoint may return 'reset_code'
        reset_code = body.get('reset_code')

        if not reset_code:
            # If not returned, assume email was sent externally; we cannot proceed further in test
            # but endpoint should still respond 200
            return

        # Now call reset-password with the code
        resp2 = client.post('/api/auth/reset-password', json={'email': email, 'code': reset_code, 'senha': new_password})
        assert resp2.status_code == 200

        # Try to login with the new password
        resp3 = client.post('/api/auth/login', json={'email': email, 'senha': new_password})
        assert resp3.status_code == 200
        data = resp3.json()
        assert 'access_token' in data

    finally:
        # cleanup: remove user and any password reset rows
        with Session(engine) as session:
            stmt = select(crud.User).where(crud.User.email == email) if hasattr(crud, 'User') else None
            # Directly query model from backend.models to remove
            try:
                from backend.models import User, PasswordReset
                u = session.exec(select(User).where(User.email == email)).first()
                if u:
                    session.delete(u)
                # remove any password reset rows
                prs = session.exec(select(PasswordReset).where(PasswordReset.email == email)).all()
                for pr in prs:
                    session.delete(pr)
                session.commit()
            except Exception:
                session.rollback()
