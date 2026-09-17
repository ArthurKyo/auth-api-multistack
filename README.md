# 🔐 auth-api-multistack — Autenticação comparada em 3 Back-ends

> **PT:** Mesma API de auth (register/login/refresh/RBAC) implementada em **NestJS + Java Spring Boot + Python FastAPI**. Perfeito para provar domínio de back-end e banco de dados.
> **EN:** Same auth API implemented in 3 stacks to prove back-end mastery.

## Estrutura
```
/apps
  /node-nest   → NestJS + Prisma + PostgreSQL + JWT + Passport
  /java-spring → Spring Boot + Spring Security + JPA + Flyway
  /python-fast → FastAPI + SQLAlchemy + Alembic + PyJWT
/docker-compose.yml → postgres + redis para os 3
/docs → comparativo performance, DX, decisão
```

## Endpoints (iguais nos 3)
`POST /auth/register` • `POST /auth/login` • `POST /auth/refresh` • `GET /users/me` • `GET /admin/users (RBAC)`

## Como rodar (ex. Node)
```bash
cd apps/node-nest
cp .env.example .env
docker compose up -d db redis
npx prisma migrate dev
npm run start:dev
# docs: http://localhost:3000/docs
```

## O que recrutador vê aqui
Modelagem User/Session/Role, hash bcrypt/argon2, refresh rotation, blacklist Redis, testes, migrations em 3 ORMs, Swagger em 3 linguagens.

## Roadmap
- [ ] OAuth2 Google/GitHub
- [ ] 2FA TOTP
- [ ] Benchmark k6 entre stacks
