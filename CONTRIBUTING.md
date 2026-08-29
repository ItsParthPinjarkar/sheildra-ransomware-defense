# Contributing to AutoVault

Thank you for contributing to AutoVault! This document describes our development workflow and code quality standards.

## Development Workflow

### Branch Strategy

- `main` — Production-ready code, protected by Qodo reviews
- `develop` — Integration branch for features
- `feat/*` — Feature branches
- `fix/*` — Bug fix branches
- `refactor/*` — Refactoring branches

### Making Changes

1. **Create a feature branch** from `main` or `develop`:
   ```bash
   git checkout -b feat/my-new-feature
   ```

2. **Make your changes** with clear, focused commits:
   ```bash
   git add .
   git commit -m "feat: add neuromorphic threat detection"
   ```

3. **Push and create a Pull Request**:
   ```bash
   git push origin feat/my-new-feature
   ```
   Then create a PR on GitHub with a descriptive title and description.

4. **Wait for Qodo review** — the AI reviewer will analyze your changes automatically.

5. **Address review findings**:
   - **HIGH severity**: Must fix or dismiss with explanation
   - **MEDIUM severity**: Review and decide
   - **LOW severity**: Engineering judgment

6. **Get approval** and merge.

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `docs`: Documentation
- `test`: Tests
- `chore`: Maintenance
- `security`: Security fix

**Examples:**
```
feat(mcp): add predictive ransomware defense tool
fix(agent): handle race condition in process monitor
refactor(sandbox): extract entropy calculation into utility
docs(readme): add TrueForge integration guide
security(mcp): validate all tool input parameters
```

### PR Title Format

```
<type>: <concise description>
```

**Good examples:**
- `feat: add neuromorphic security processing engine`
- `fix: handle empty directory in threat scanner`
- `refactor: extract MCP tool registration into decorators`

**Bad examples:**
- `update code` ❌
- `fix bug` ❌
- `changes` ❌

### PR Description Template

```markdown
## What
Brief description of what this PR does.

## Why
Why this change is needed. Link to issue if applicable.

## How
How the change was implemented. Key design decisions.

## Testing
How to verify the change works:
- [ ] Unit tests pass
- [ ] Manual testing performed
- [ ] Edge cases considered

## TrueForge Features Used
- [ ] MCP Tools
- [ ] Sandbox execution
- [ ] Human approval
- [ ] Subagents
- [ ] Skills

## Qodo Review
- [ ] Qodo review completed
- [ ] HIGH findings addressed
- [ ] MEDIUM findings reviewed
- [ ] LOW findings noted
```

## Code Quality Standards

### Python Code
- Use type hints for all function signatures
- Write docstrings for public functions
- Follow PEP 8 style
- Maximum line length: 120 characters
- Use `ruff` for linting

### MCP Tools
- All tool parameters must be validated
- Return JSON responses with consistent structure
- Handle errors gracefully with meaningful messages
- Include input validation for security

### Security
- Never hardcode credentials or API keys
- Validate all external inputs
- Use parameterized queries where applicable
- Follow least-privilege principle

### Testing
- Write tests for new features
- Aim for >80% code coverage on critical paths
- Test error conditions and edge cases
- Use `pytest` for test framework

## Qodo Integration

Every PR is automatically reviewed by Qodo (AI code review). The review checks:

1. **Correctness** — Logic errors, edge cases
2. **Security** — Vulnerabilities, injection risks
3. **Performance** — Inefficiencies, resource leaks
4. **Maintainability** — Code clarity, documentation
5. **Testing** — Coverage, test quality

### Responding to Qodo Findings

**Fixing a finding:**
```bash
# Make the fix
git add .
git commit -m "fix: address Qodo finding about input validation"
git push
```

**Dismissing a finding:**
Leave a comment explaining why:
> Dismissed: This is intentional — the input is already validated upstream by the MCP tool decorator.

## Getting Help

- Check existing issues and PRs
- Read the [TrueForge documentation](https://truefoundry.com)
- Ask in team channels

## License

By contributing, you agree that your contributions will be licensed under the project's open-source license.
