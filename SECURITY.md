# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 4.0.x   | ✅ Active |
| < 4.0   | ❌ Not supported |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not open a public issue**. Instead, send a private report to the repository maintainer via GitHub's private vulnerability reporting feature.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Security Best Practices

- All passwords are SHA-256 hashed (not stored in plaintext)
- Session state is managed server-side via Streamlit's session state
- JWT-based token validation for API endpoints
- No secrets or API keys are committed to the repository
- Use environment variables (`.env`) for production deployments
- The auto-generated dataset contains **no real customer information**
