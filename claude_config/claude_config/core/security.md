# Security Requirements - PROTECTED

## Non-Negotiable Security Rules

### 1. Credentials & Secrets
- **NEVER** store credentials in code
- **NEVER** commit secrets to version control
- **ALWAYS** use environment variables
- **ALWAYS** use `.env` files (git-ignored)
- **VALIDATE** `.gitignore` includes sensitive patterns

### 2. Data Security
- **NEVER** log PHI/PII
- **ALWAYS** validate input
- **ALWAYS** sanitize file paths
- **ALWAYS** use parameterized queries
- **NEVER** construct SQL from user input

### 3. Medical Data Specific
- **FOLLOW** HIPAA requirements
- **DE-IDENTIFY** data per Safe Harbor
- **ENCRYPT** data at rest and in transit
- **AUDIT** all data access
- **LIMIT** access to minimum necessary

### 4. Code Security Patterns
- Use environment variables for all configuration
- Validate and sanitize all user input
- Use parameterized queries for databases
- Implement path traversal protection
- Never log sensitive information

### 5. Security Checklist
- [ ] No hardcoded credentials
- [ ] All user input validated
- [ ] SQL injection prevented
- [ ] Path traversal prevented
- [ ] PHI/PII not logged
- [ ] Encryption implemented
- [ ] Access controls verified
- [ ] Dependencies reviewed for vulnerabilities