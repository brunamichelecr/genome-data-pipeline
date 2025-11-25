from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, SQLModel
from .database import engine, get_session
from . import models, crud, auth, schemas
from dotenv import load_dotenv
import os
import logging
from sqlalchemy.exc import IntegrityError, DataError

load_dotenv()

app = FastAPI(title='Genome Data Pipeline - Backend (Auth + Doenças)', debug=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# CORS: permitir chamadas do frontend em dev (Vite)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable CORS for local frontend dev server(s)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    from jose import JWTError
    try:
        payload = auth.decode_access_token(token)
        email: str = payload.get('sub')
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user = crud.get_user_by_email(session, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # compute admin flag from environment variable ADMIN_EMAILS (comma-separated)
    admin_emails = os.getenv('ADMIN_EMAILS', '')
    admin_list = [a.strip().lower() for a in admin_emails.split(',') if a.strip()]
    is_admin_flag = False
    try:
        is_admin_flag = user.email.lower() in admin_list
    except Exception:
        is_admin_flag = False

    # Return a lightweight object (not the ORM model) so we can attach runtime-only fields
    from types import SimpleNamespace
    user_obj = SimpleNamespace(
        id=getattr(user, 'id', None),
        nome=getattr(user, 'nome', None),
        genero=getattr(user, 'genero', None),
        email=getattr(user, 'email', None),
        is_admin=is_admin_flag,
        isAdmin=is_admin_flag,
        role='admin' if is_admin_flag else None,
    )
    return user_obj


def require_admin(user = Depends(get_current_user)):
    if not getattr(user, 'is_admin', False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin privileges required')
    return user


@app.post('/api/auth/register', response_model=schemas.LoginResponse)
def register(user_in: schemas.UserCreate, session: Session = Depends(get_session)):
    existing = crud.get_user_by_email(session, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    try:
        user = crud.create_user(session, nome=user_in.nome, email=user_in.email, senha=user_in.senha, genero=user_in.genero)
    except DataError:
        logging.exception('DataError when creating user (probably a field too long)')
        raise HTTPException(status_code=400, detail='Invalid data: one or more fields exceed allowed length')
    except IntegrityError:
        # Log the exception server-side and return a friendly 400 to the client.
        logging.exception('IntegrityError when creating user')
        raise HTTPException(status_code=400, detail='Email already registered or database constraint violated')
    except Exception:
        logging.exception('Unexpected error when creating user')
        raise HTTPException(status_code=500, detail='Internal server error')

    token = auth.create_access_token({'sub': user.email})
    # compute admin flag before returning and serialize user as plain dict to avoid ORM -> pydantic issues
    admin_emails = os.getenv('ADMIN_EMAILS', '')
    admin_list = [a.strip().lower() for a in admin_emails.split(',') if a.strip()]
    is_admin_flag = user.email.lower() in admin_list
    user_data = {
        'id': getattr(user, 'id', None),
        'nome': getattr(user, 'nome', None),
        'genero': getattr(user, 'genero', None),
        'email': getattr(user, 'email', None),
        'is_admin': is_admin_flag,
        'isAdmin': is_admin_flag,
        'role': 'admin' if is_admin_flag else None,
    }
    return {'access_token': token, 'token_type': 'bearer', 'user': user_data}


@app.post('/api/auth/forgot-password')
def forgot_password(payload: schemas.PasswordResetRequest, session: Session = Depends(get_session)):
    """Generate a short 6-character reset code and store it in DB.

    Development: the code is returned in the response for testing. In production send it by email.
    """
    from datetime import datetime, timedelta
    import random
    import string

    try:
        user = crud.get_user_by_email(session, payload.email)
        # Always respond with 200 to avoid leaking which emails exist
        if not user:
            return {'detail': 'If the email exists, a reset code was sent.'}

        # generate 6-char alphanumeric code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        expires_at = datetime.utcnow() + timedelta(minutes=30)
        crud.create_password_reset(session, user.email, code, expires_at)
        logging.info('Password reset code generated for %s', user.email)

        # Send via SMTP using helper; in dev also return the code in JSON for convenience
        try:
            from .email_utils import send_email
            subject = 'Seu código de redefinição de senha'
            body = f'Código: {code}\n\nUse este código para redefinir sua senha. Ele expira em 30 minutos.'
            # send in background would be ideal; keep synchronous for now
            send_email(subject, body, user.email)
        except Exception:
            logging.exception('Failed to send reset email; proceeding to return dev code')

        # If MAIL_DEV=1 or SMTP_HOST is localhost, return the code in response to help testing
        # Default to '0' to avoid returning codes in production-like setups
        mail_dev = os.getenv('MAIL_DEV', '0')
        host = os.getenv('SMTP_HOST', '127.0.0.1')
        if mail_dev == '1' or host.startswith('127') or host.startswith('localhost'):
            return {'detail': 'Password reset code generated (development only).', 'reset_code': code}

        return {'detail': 'If the email exists, a reset code was sent.'}
    except Exception:
        logging.exception('Failed to generate password reset code')
        raise HTTPException(status_code=500, detail='Internal server error')


@app.post('/api/auth/reset-password')
def reset_password(payload: schemas.PasswordResetConfirm, session: Session = Depends(get_session)):
    """Reset a user's password using an email + 6-char code and a new password."""
    try:
        # Verify code exists and consume it
        ok = crud.verify_and_consume_reset_code(session, payload.email, payload.code)
        if not ok:
            raise HTTPException(status_code=400, detail='Invalid or expired reset code')
        user = crud.get_user_by_email(session, payload.email)
        if not user:
            raise HTTPException(status_code=400, detail='User not found')
        updated = crud.update_user_password(session, user, payload.senha)
        if not updated:
            raise HTTPException(status_code=500, detail='Failed to update password')
        return {'detail': 'Password updated successfully'}
    except HTTPException:
        raise
    except Exception:
        logging.exception('Failed to reset password')
        raise HTTPException(status_code=500, detail='Internal server error')


@app.post('/api/auth/login', response_model=schemas.LoginResponse)
def login(form_data: schemas.UserLogin, session: Session = Depends(get_session)):
    # Expecting email and senha in body
    try:
        user = crud.get_user_by_email(session, form_data.email)
        if not user or not auth.verify_password(form_data.senha, user.hashed_password):
            raise HTTPException(status_code=401, detail='Incorrect email or password')
        token = auth.create_access_token({'sub': user.email})
        admin_emails = os.getenv('ADMIN_EMAILS', '')
        admin_list = [a.strip().lower() for a in admin_emails.split(',') if a.strip()]
        is_admin_flag = user.email.lower() in admin_list
        user_data = {
            'id': getattr(user, 'id', None),
            'nome': getattr(user, 'nome', None),
            'genero': getattr(user, 'genero', None),
            'email': getattr(user, 'email', None),
            'is_admin': is_admin_flag,
            'isAdmin': is_admin_flag,
            'role': 'admin' if is_admin_flag else None,
        }
        return {'access_token': token, 'token_type': 'bearer', 'user': user_data}
    except HTTPException:
        raise
    except Exception:
        # Generic internal error without leaking implementation details
        raise HTTPException(status_code=500, detail='Internal server error')


@app.get('/api/doencas', response_model=list[schemas.DiseaseRead])
def get_doencas(skip: int = 0, limit: int = 100, session: Session = Depends(get_session), user = Depends(get_current_user)):
    return crud.list_diseases(session, skip=skip, limit=limit)


@app.post('/api/doencas', response_model=schemas.DiseaseRead, status_code=201)
def post_doenca(payload: schemas.DiseaseCreate, session: Session = Depends(get_session), admin = Depends(require_admin)):
    disease = crud.create_disease(session, payload.dict(), created_by=admin.id)
    return disease


# Debug endpoints removed for production readiness. Use scripts under `backend/scripts/` during development instead.
