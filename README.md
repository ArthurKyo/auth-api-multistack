# 🔐 Auth API Multistack

Mesma ideia de autenticação implementada em diferentes stacks de back-end. A primeira versão funcional é em **Python + FastAPI**, construída para demonstrar fundamentos importantes de desenvolvimento back-end: API REST, autenticação, autorização, persistência, testes e documentação.

## ✅ Implementado: Python + FastAPI

**Stack**

- Python 3.12
- FastAPI
- SQLAlchemy 2
- PostgreSQL 16
- PyJWT
- bcrypt / Passlib
- Pytest
- Alembic
- Docker Compose
- GitHub Actions

### Endpoints

| Método | Endpoint | Acesso |
|---|---|---|
| GET | `/health` | Público |
| POST | `/auth/register` | Público |
| POST | `/auth/login` | Público |
| GET | `/users/me` | JWT |
| GET | `/users/admin-only` | JWT + role admin |
| GET | `/users/admin` | JWT + admin + paginação |
| POST | `/auth/refresh` | Refresh token com rotação |
| POST | `/auth/logout` | Revoga refresh token |

O FastAPI também disponibiliza documentação interativa automaticamente em `/docs`.

## Estrutura

```text
auth-api-multistack/
├── apps/
│   └── python-fast/
│       ├── app/
│       │   ├── api/
│       │   │   ├── auth.py
│       │   │   └── users.py
│       │   ├── core/
│       │   │   ├── config.py
│       │   │   └── security.py
│       │   ├── db/
│       │   │   ├── base.py
│       │   │   └── session.py
│       │   ├── models/
│       │   │   └── user.py
│       │   ├── schemas/
│       │   │   ├── auth.py
│       │   │   └── user.py
│       │   └── main.py
│       ├── tests/
│       │   └── test_health.py
│       ├── Dockerfile
│       ├── pytest.ini
│       └── requirements.txt
├── .github/workflows/python-ci.yml
├── docker-compose.yml
└── .env.example
```

## Como executar

Crie o arquivo de ambiente:

```bash
cp .env.example .env
```

Suba API + PostgreSQL. O container da API executa `alembic upgrade head` antes de iniciar:

```bash
docker compose up --build
```

Depois acesse:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Exemplo de uso

### Cadastro

```http
POST /auth/register
Content-Type: application/json

{
  "name": "Arthur",
  "email": "arthur@example.com",
  "password": "senha123"
}
```

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "arthur@example.com",
  "password": "senha123"
}
```

A resposta retorna um Bearer Token JWT. Use o token em:

```http
Authorization: Bearer <token>
```

para acessar `GET /users/me`.

## Conceitos demonstrados

- Separação entre rotas, schemas, models, configuração e persistência
- Modelagem de usuário em banco relacional
- Senhas armazenadas com hash
- JWT com expiração
- Autorização baseada em papel (RBAC)
- Validação automática com Pydantic
- Códigos HTTP adequados para conflito, autenticação e autorização
- Configuração via variáveis de ambiente
- Testes automatizados com banco isolado em memória
- Rate limiting de login e cadastro
- Logout e revogação de refresh token
- Request ID, logs e headers de segurança
- Tratamento centralizado de erros
- CI configurado com GitHub Actions + Ruff + Pytest
- Containerização com Docker

## Roadmap

### Python / FastAPI
- [x] Cadastro e login
- [x] Access token JWT
- [x] PostgreSQL + SQLAlchemy
- [x] RBAC básico
- [x] Docker Compose
- [x] Pytest
- [x] GitHub Actions
- [x] Alembic migrations
- [x] Refresh token com rotação
- [x] Testes de integração de auth
- [x] Rate limiting
- [x] Paginação e endpoint administrativo de usuários

### Outras implementações
- [ ] Java + Spring Boot
- [ ] Node.js + NestJS

## Por que este projeto existe?

Frameworks mudam, mas os fundamentos de back-end permanecem: modelagem de dados, regras de negócio, autenticação, autorização, HTTP, testes e segurança. Este repositório será usado para implementar o mesmo domínio em stacks diferentes e comparar as decisões de cada ecossistema.

---

Documentação adicional:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — decisões e fluxo da aplicação
- [`SECURITY.md`](SECURITY.md) — controles implementados e limitações de produção

Projeto em evolução para estudo e portfólio de desenvolvimento back-end.
