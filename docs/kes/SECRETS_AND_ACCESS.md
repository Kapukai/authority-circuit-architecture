# Secrets and Access

This package neither requires nor stores API keys or passwords.

Use environment variables or an approved secret manager. Never commit `.env`,
private keys, passwords, access tokens, session cookies, database credentials, or
production patient data. The access preflight reports only whether selected
variables are present; it never prints values.

GitHub authentication is separate from repository code. A successful connector,
credential-manager, or `gh auth status` check proves access without exposing a token.
