---
name: deploy-check
description: Use before publishing the project to hosting, VPS, shared hosting, or production.
---

# Deploy Check

Before deployment, verify:
- Environment variables are configured
- Database credentials are not committed
- Debug mode is disabled
- Error display is disabled
- Logs are protected
- Admin area is protected
- HTTPS is enabled
- File permissions are safe
- Database backup exists
- Public folder does not expose private files

Return:
1. Blockers before deploy
2. Recommended fixes
3. Final deploy checklist
