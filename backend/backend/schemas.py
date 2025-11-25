from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    nome: str
    genero: Optional[str] = None
    email: EmailStr
    senha: str


class UserLogin(BaseModel):
    email: EmailStr
    senha: str


class UserRead(BaseModel):
    id: int
    nome: str
    genero: Optional[str] = None
    email: EmailStr
    # is_admin is computed at runtime (not stored in DB). Make it optional with default False
    is_admin: Optional[bool] = False

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserRead


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    email: EmailStr
    code: str
    senha: str


class DiseaseCreate(BaseModel):
    disease_name: str
    disease_name_pt: str
    medgen_uid: Optional[str] = None
    breve_desc: Optional[str] = None
    disease_desc_pt: Optional[str] = None


class DiseaseRead(BaseModel):
    id: int
    disease_name: str
    disease_name_pt: str
    medgen_uid: Optional[str]
    breve_desc: Optional[str]
    disease_desc_pt: Optional[str]

    class Config:
        orm_mode = True
