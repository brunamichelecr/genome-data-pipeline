from sqlmodel import Session, select
from .models import User, Disease
from .auth import get_password_hash, verify_password as _verify_password
from datetime import datetime


def get_user_by_email(session: Session, email: str):
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def create_user(session: Session, nome: str, email: str, senha: str, genero: str = None):
    # `User` model does not include an `is_admin` column. Do not pass unknown kwargs.
    # Normalize `genero` to a single-character code to match existing DB schema.
    genero_code = None
    if genero:
        genero_map = {
            'Feminino': 'F',
            'Masculino': 'M',
            'Outro': 'O',
            'NaoInformar': 'N',
            'Não Informar': 'N',
            'Nao Informar': 'N',
        }
        if len(genero) == 1:
            genero_code = genero
        else:
            genero_code = genero_map.get(genero, genero[0] if genero else None)

    user = User(
        nome=nome,
        email=email,
        genero=genero_code,
        hashed_password=get_password_hash(senha),
        created_at=datetime.utcnow(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def create_disease(session: Session, disease_data: dict, created_by: int = None):
    allowed = {"disease_name", "disease_name_pt", "medgen_uid", "breve_desc", "disease_desc_pt", "disease_desc", "disease_synonym"}
    filtered = {k: v for k, v in disease_data.items() if k in allowed}
    disease = Disease(**filtered)
    session.add(disease)
    session.commit()
    session.refresh(disease)
    return disease

def list_diseases(session: Session, skip: int = 0, limit: int = 100):
    statement = select(Disease).offset(skip).limit(limit)
    return session.exec(statement).all()


def update_user_password(session: Session, user, new_password: str):
    """Set a new password hash for an existing user instance or ORM row.

    `user` may be a User instance from the ORM or a simple object with an `email`.
    """
    # If a full User instance is provided, update directly.
    if hasattr(user, 'hashed_password'):
        user.hashed_password = get_password_hash(new_password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    # Otherwise try to look up by email
    existing = get_user_by_email(session, getattr(user, 'email', user))
    if not existing:
        return None
    existing.hashed_password = get_password_hash(new_password)
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing


def create_password_reset(session: Session, email: str, code: str, expires_at: datetime):
    from .models import PasswordReset
    # Store a hash of the reset code, not the plaintext
    hashed = get_password_hash(code)
    pr = PasswordReset(email=email, code=hashed, expires_at=expires_at)
    session.add(pr)
    session.commit()
    session.refresh(pr)
    return pr


def verify_and_consume_reset_code(session: Session, email: str, code: str):
    from .models import PasswordReset
    from datetime import datetime
    # We must find any password reset row for the email, then verify hashed code
    statement = select(PasswordReset).where(PasswordReset.email == email)
    pr = session.exec(statement).first()
    if not pr:
        return False
    # Check expiry
    if pr.expires_at and pr.expires_at < datetime.utcnow():
        session.delete(pr)
        session.commit()
        return False
    # Verify provided code against stored hash
    try:
        ok = _verify_password(code, pr.code)
    except Exception:
        ok = False
    # consume the record regardless (single-use)
    session.delete(pr)
    session.commit()
    return ok
