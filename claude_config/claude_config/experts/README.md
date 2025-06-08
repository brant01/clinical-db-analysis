# Expert Agent System

## Purpose
Expert agents provide specialized knowledge and guidance for specific domains or technical areas. Consult them when facing challenges in their area of expertise.

## How to Use Experts

### When to Consult
- Domain-specific challenges
- Best practices verification
- Architecture decisions
- Code review for critical sections
- Compliance/safety checks

### How to Consult
1. Identify relevant expert(s)
2. Read their guidance
3. Apply to your context
4. Document consultation

Example:
"Consulting medical_research expert about cohort selection..."

### Expert Types

#### Core Experts (All Projects)
- **software_engineer.md** - Code quality, patterns
- **data_compliance.md** - Privacy, security
- **claude_expert.md** - Claude usage optimization

#### Domain Experts (Specialized)
- **medical_research.md** - Clinical trials, IRB
- **ml_ai_expert.md** - Machine learning, AI

#### Proposed Experts
New expert proposals go in `proposed/`

## Creating New Experts

### Template
```markdown
# [Expert Name] Expert

## Identity
I am a [role] specializing in [domain].

## Core Principles
1. **[Principle]**: [Explanation]

## Key Questions I Ask
- [Questions that guide thinking]

## Red Flags I Watch For
- [Common mistakes to avoid]

## Best Practices
[Domain-specific guidance]

## When to Escalate
Contact humans when:
- [Scenarios requiring oversight]
```

## Expert Interaction
- Single expert: Apply directly
- Multiple experts: Synthesize views
- Conflicts: Document tradeoffs