# Data Handling Guidelines

## Data Classification

### Protected Health Information (PHI)
**MUST BE REMOVED OR PROTECTED:**
- Names, addresses, contact info
- Dates (except year)
- ID numbers (SSN, MRN, etc.)
- Biometric identifiers
- Photos, URLs, IP addresses
- Any unique identifier

### Safe to Retain
- Year only (for dates)
- Age (if <90)
- State/region
- De-identified study IDs

## De-identification Process
1. Apply Safe Harbor method
2. Shift dates consistently per patient
3. Hash identifiers (one-way)
4. Remove geographic detail
5. Suppress small cells (<10)
6. Document process

## Data Storage
```
project_data/
├── raw/              # Original (protected, gitignored)
├── interim/          # Processing (gitignored)
├── processed/        # Analysis-ready (gitignored)
├── external/         # Reference data
└── docs/            # Documentation
```

### Cross-Platform Path Support
For data on network drives, use `@REMOTE_DRIVE@` in .env files:
- Mac: `@REMOTE_DRIVE@` → `/Volumes`
- WSL: `@REMOTE_DRIVE@` → `/mnt/r`
- Linux: `@REMOTE_DRIVE@` → `/mnt`

Example .env:
```
DATA_PATH=@REMOTE_DRIVE@/your_username/project/data
MODEL_PATH=@REMOTE_DRIVE@/shared/models
```

## Security Requirements
- Encrypt at rest (AES-256)
- Encrypt in transit (TLS 1.2+)
- Access logging enabled
- Role-based access control
- Regular backups
- Secure deletion

## Data Quality
- Validate on input
- Check ranges and formats
- Handle missing data explicitly
- Document data lineage
- Version control schemas

## Compliance Checklist
- [ ] IRB approval obtained
- [ ] Data use agreement signed
- [ ] De-identification complete
- [ ] Encryption enabled
- [ ] Access controls set
- [ ] Audit logging active
- [ ] Retention policy defined
- [ ] Deletion procedures ready