# Architecture

## Request flow

```text
Client
  |
  v
FastAPI
  |
  +-- middleware: request id, logs, security headers
  |
  +-- /auth
  |     +-- register
  |     +-- login
  |     +-- refresh
  |     +-- logout
  |
  +-- /users
        +-- me
        +-- admin (RBAC + pagination)

FastAPI -> SQLAlchemy -> PostgreSQL
```

## Authentication

Passwords are never stored directly. Registration hashes passwords before persistence.

Login returns:

1. a short-lived signed JWT access token;
2. a random opaque refresh token.

Only the SHA-256 hash of the refresh token is stored. When a refresh token is used, it is revoked and replaced by a new one. This demonstrates refresh-token rotation and prevents the same persisted token from being accepted twice.

## Authorization

Protected routes decode the access token and load the current user from the database. Administrative routes require the `admin` role.

## Persistence

SQLAlchemy models represent users and refresh tokens. Alembic owns the PostgreSQL schema migration history.

## Rate limiting

The current implementation intentionally uses an in-memory limiter to keep the project easy to run. In a horizontally scaled production system, the limiter would move to Redis or another shared store.

## Observability

Every response receives an `X-Request-Id`. Request method, route, status and duration are logged. Unexpected failures receive an error ID that can be correlated with server logs.

## Testing

Tests replace the database dependency with an isolated in-memory SQLite engine using FastAPI dependency overrides. This keeps tests deterministic and avoids requiring PostgreSQL in CI.
