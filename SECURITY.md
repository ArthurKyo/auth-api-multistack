# Security

## Scope

This repository is a portfolio/study project. It demonstrates authentication and authorization concepts but is not presented as a production-ready identity provider.

## Implemented controls

- Password hashing with bcrypt
- Short-lived JWT access tokens
- Opaque refresh tokens stored as SHA-256 hashes
- Refresh-token rotation and revocation
- RBAC for administrative routes
- Login and registration rate limiting
- Environment-based secrets
- Security response headers
- Request correlation IDs
- Centralized unexpected-error handling
- Automated tests and CI

## Production hardening still recommended

For a real production deployment, use a distributed rate-limit store such as Redis, secret management, HTTPS/TLS, key rotation, monitoring/alerting, secure cookie-based token delivery where appropriate, CSRF protections for cookie-based flows, account recovery, MFA, audit persistence, dependency scanning and a managed database with backup/restore procedures.

## Reporting

Do not include passwords, tokens, private keys or personal data in issues.
