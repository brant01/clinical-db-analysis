# Repository Maintenance Guidelines

## Adding Collaborators

### GitHub Process
1. Go to Settings → Manage access → Add people
2. Send invitation to collaborator's GitHub username or email
3. Update README if adding new research groups
4. Ensure new collaborators run `quickstart.py` for initial setup

### Onboarding Checklist
- [ ] GitHub access granted
- [ ] Provided link to git-basics-guide.md
- [ ] Confirmed they have data access at their institution
- [ ] Walked through quickstart.py process
- [ ] Showed example projects folder

## Reviewing Contributions

### Code Review Checklist
- [ ] **PHI Protection**: No patient identifiers or data files
- [ ] **Polars Usage**: Verify polars used (not pandas)
- [ ] **Documentation**: Beginner-friendly comments and docs
- [ ] **Data Paths**: Ensure paths are not hardcoded
- [ ] **Testing**: Works with both NSQIP and NCDB if applicable
- [ ] **Helper Scripts**: Uses clinical-db script for notebooks

### Common Issues to Check
1. **Data Security**
   - No actual data files committed
   - No hardcoded paths to network drives
   - No patient identifiers in code

2. **Code Quality**
   - Uses polars DataFrames/LazyFrames
   - Follows project structure (own folder in projects/)
   - Imports from shared utilities correctly

3. **Documentation**
   - README updated with research question
   - Code has clear comments
   - Methods are documented

## Version Control Standards

### Commit Guidelines
- Descriptive commit messages
- No "Co-authored-by" tags
- Small, focused commits preferred
- Use conventional commit format when possible:
  - `feat:` New feature
  - `fix:` Bug fix
  - `docs:` Documentation
  - `refactor:` Code restructure

### What Not to Commit
- Data files (any format)
- Personal configuration files
- Temporary files or caches
- API keys or credentials
- Large binary files

## Repository Structure Management

### Protected Areas
Only repository maintainers should modify:
- `/shared/utils/` - Common utilities
- `/shared/templates/` - Analysis templates
- `/claude_config/` - AI assistant configuration
- Root configuration files (pyproject.toml, etc.)

### Researcher Areas
Researchers have full control over:
- `/projects/[their-name-project]/` - Their analysis folder
- Their own README files
- Their analysis notebooks

## Maintenance Tasks

### Regular Tasks
- Review and merge pull requests
- Update dependencies in pyproject.toml
- Check for security updates
- Archive completed projects
- Update documentation as needed

### Quarterly Reviews
- [ ] Review all active projects
- [ ] Update templates with new patterns
- [ ] Check helper utilities for improvements
- [ ] Update documentation based on user feedback
- [ ] Clean up abandoned project folders

## Handling Issues

### Common Problems
1. **Merge Conflicts**
   - Usually in shared areas
   - Resolve favoring working code
   - Communicate with both parties

2. **Large Files Accidentally Committed**
   - Use git filter-branch to remove
   - Update .gitignore
   - Educate user on data handling

3. **Dependencies Conflicts**
   - Test in fresh environment
   - Pin versions if needed
   - Document any constraints

## Communication

### With Researchers
- Be supportive and educational
- Remember many are coding beginners
- Provide examples when explaining issues
- Focus on learning opportunities

### Documentation Updates
- Keep README current
- Update guides based on common questions
- Add new examples as needed
- Maintain beginner-friendly tone