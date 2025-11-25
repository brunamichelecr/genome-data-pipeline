from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Boolean
from datetime import timedelta


class User(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True, sa_column=Column("id_usuario", Integer, primary_key=True))
    nome: str = Field(sa_column=Column("nome", String, nullable=False))
    genero: Optional[str] = Field(default=None, sa_column=Column("genero", String, nullable=True))
    email: str = Field(index=True, sa_column=Column("email", String, nullable=False))
    hashed_password: str = Field(sa_column=Column("senha_hash", String, nullable=False))
    created_at: Optional[datetime] = Field(default=None, sa_column=Column("criado_em", DateTime, nullable=True))


class Disease(SQLModel, table=True):
    __tablename__ = "diseases"
    id: Optional[int] = Field(default=None, primary_key=True, sa_column=Column("id_disease", Integer, primary_key=True))
    disease_name: str = Field(sa_column=Column("disease_name", String, nullable=False))
    disease_desc: Optional[str] = Field(default=None, sa_column=Column("disease_desc", String, nullable=True))
    disease_name_pt: Optional[str] = Field(default=None, sa_column=Column("disease_name_pt", String, nullable=True))
    disease_synonym: Optional[str] = Field(default=None, sa_column=Column("disease_synonym", String, nullable=True))
    medgen_uid: Optional[str] = Field(default=None, sa_column=Column("medgen_uid", String, nullable=True))
    disease_desc_pt: Optional[str] = Field(default=None, sa_column=Column("disease_desc_pt", String, nullable=True))
    breve_desc: Optional[str] = Field(default=None, sa_column=Column("breve_desc", String, nullable=True))


class PasswordReset(SQLModel, table=True):
    __tablename__ = "password_resets"
    id: Optional[int] = Field(default=None, primary_key=True, sa_column=Column("id", Integer, primary_key=True))
    email: str = Field(sa_column=Column("email", String, nullable=False))
    code: str = Field(sa_column=Column("code", String, nullable=False))
    expires_at: Optional[datetime] = Field(default=None, sa_column=Column("expires_at", DateTime, nullable=True))
