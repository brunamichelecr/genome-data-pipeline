"""Utility to create an admin user in the configured DATABASE_URL.
Usage: python create_admin.py --email admin@local --senha secret123 --nome Admin
"""
import argparse
import os
from sqlmodel import Session, create_engine
from dotenv import load_dotenv

load_dotenv()

from backend.models import User
from backend.auth import get_password_hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', required=True)
    parser.add_argument('--senha', required=True)
    parser.add_argument('--nome', default='Admin')
    args = parser.parse_args()

    DATABASE_URL = os.getenv('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/postgres'
    engine = create_engine(DATABASE_URL)

    with Session(engine) as session:
        existing = session.query(User).filter(User.email == args.email).first()
        if existing:
            print('User already exists')
            # ensure email is in ADMIN_EMAILS
            add_admin_email_to_env(args.email)
            return
        user = User(nome=args.nome, email=args.email, hashed_password=get_password_hash(args.senha))
        session.add(user)
        session.commit()
        print('User created:', args.email)
        add_admin_email_to_env(args.email)


def add_admin_email_to_env(email: str):
    # Ensure backend/.env contains ADMIN_EMAILS with the given email appended
    env_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(env_dir, '.env')
    try:
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
        else:
            lines = []

        found = False
        new_lines = []
        email_lower = email.strip().lower()
        for ln in lines:
            if ln.strip().startswith('ADMIN_EMAILS='):
                found = True
                existing = ln.split('=', 1)[1].strip()
                items = [x.strip().lower() for x in existing.split(',') if x.strip()]
                if email_lower not in items:
                    items.append(email_lower)
                new_lines.append('ADMIN_EMAILS=' + ','.join(items))
            else:
                new_lines.append(ln)

        if not found:
            new_lines.append('ADMIN_EMAILS=' + email_lower)

        with open(env_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines) + '\n')
        print('Updated .env with ADMIN_EMAILS:', email_lower)
    except Exception as e:
        print('Could not update .env:', e)


if __name__ == '__main__':
    main()
