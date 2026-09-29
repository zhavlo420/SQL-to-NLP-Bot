# Security checklist

Implemented in MVP:
- SELECT-only policy
- SQL parsing with SQLGlot
- single statement restriction
- dedicated read-only PostgreSQL role

Production:
- RBAC
- tenant isolation
- row-level security
- PII classification
- statement timeout
- query cost limits
- audit logging
- secrets manager
- prompt injection regression tests
- human approval for sensitive actions

Never place database credentials in prompts, model context, frontend code, or logs.
