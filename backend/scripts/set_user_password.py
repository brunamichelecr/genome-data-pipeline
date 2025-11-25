"""Set or update a user's password (hashing with backend auth settings).
Usage: python set_user_password.py --email <email> --senha <password>
"""
import argparse
import os
from sqlmodel import Session, create_engine, select
from dotenv import load_dotenv

load_dotenv()

# allow running from backend/ directory
from backend.models import User
from backend.auth import get_password_hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', required=True)
    parser.add_argument('--senha', required=True)
    args = parser.parse_args()

    DATABASE_URL = os.getenv('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/postgres'
    engine = create_engine(DATABASE_URL)

    with Session(engine) as session:
        stmt = select(User).where(User.email == args.email)
        user = session.exec(stmt).first()
        if not user:
            print('User not found:', args.email)
            return
        hashed = get_password_hash(args.senha)
        user.hashed_password = hashed
        session.add(user)
        session.commit()
        print('Password updated for', args.email)


if __name__ == '__main__':
    main()
