# Git Workflow Standards

## Branching Strategy

### Main Branches
- `main` - Production-ready code
- `develop` - Integration branch for features

### Feature Branches
- Naming: `feature/feature-name` or `feat/feature-name`
- Created from: `develop`
- Merged to: `develop` via pull request

### Release Branches
- Naming: `release/v1.2.3`
- Created from: `develop`
- Merged to: `main` and `develop`

### Hotfix Branches
- Naming: `hotfix/critical-bug-fix`
- Created from: `main`
- Merged to: `main` and `develop`

## Commit Conventions

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(auth): add OAuth2 login support

fix(api): resolve null pointer exception in user service

docs(readme): update installation instructions

test(auth): add unit tests for login validation
```

## Pull Request Process

### PR Requirements
- Descriptive title following commit conventions
- Detailed description of changes
- Link to related issues or specifications
- Screenshots for UI changes
- Test coverage for new features

### Code Review Checklist
- [ ] Code follows project standards
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact assessed

### Review Process
- At least one approved review required
- CI/CD checks must pass
- Automated tests must pass
- Manual testing completed if applicable

## Release Process

### Version Numbering
- Semantic versioning: MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Steps
1. Create release branch from develop
2. Update version numbers
3. Update changelog
4. Run full test suite
5. Create pull request to main
6. Tag release after merge
7. Deploy to production

## Git Best Practices

### General Rules
- Never commit directly to main
- Keep commits small and focused
- Write clear commit messages
- Use rebase for clean history
- Delete merged branches

### Code Quality
- Run tests before committing
- Use pre-commit hooks
- Follow code formatting standards
- Address linter warnings

### Collaboration
- Communicate with team about large changes
- Use feature flags for risky changes
- Document breaking changes
- Provide migration guides when needed