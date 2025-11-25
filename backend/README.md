# Backend para Genome Data Pipeline (Auth + Doenças)

Este backend minimal implementa endpoints para registro/login de usuários e CRUD de doenças.

Requisitos
- Python 3.10+
- PostgreSQL

Instalação

1. Crie um virtualenv e instale dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copie `.env.example` para `.env` e ajuste `DATABASE_URL` e `SECRET_KEY`.

3. Rode a aplicação:

```powershell
uvicorn backend.main:app --reload --port 8000
```

Endpoints principais
- `POST /api/auth/register` — body: `{ nome, genero, email, senha }` → cria usuário
- `POST /api/auth/login` — body: `{ email, senha }` → retorna `{ access_token, token_type }`
- `GET /api/doencas` — requires Bearer token — lista doenças
- `POST /api/doencas` — requires Bearer token with admin privileges — cria doença

Notas
- As tabelas são criadas automaticamente no startup (SQLModel `create_all`).
- Senhas são armazenadas com `bcrypt` (via `passlib`).
- Para testar como admin, crie um usuário diretamente no Postgres com `is_admin = true` ou ajuste o código temporariamente.
