# Qodo Code Review Setup Guide

## How AutoVault Uses Qodo

Every substantive change in AutoVault goes through a GitHub pull request reviewed by Qodo before merge. This ensures code quality and provides evidence for the **Best Code Quality** track.

## Option 1: Qodo GitHub App (Recommended)

### Step 1: Install Qodo on the Repository

1. Go to [Qodo on GitHub Marketplace](https://github.com/marketplace/qodo-merge-pro)
2. Click **"Install"** or **"Set up a plan"**
3. Select your organization/user and the `autovault` repository
4. Grant the requested permissions
5. Click **"Save"**

### Step 2: Verify Installation

1. Open any pull request in the repository
2. Qodo should automatically start reviewing within 1-2 minutes
3. You'll see a comment from Qodo with review findings

### Step 3: Configure Review Settings (Optional)

Create a `.qodo.yml` file in the repository root:

```yaml
# Qodo configuration for AutoVault
review:
  effort_mode: "extra_heavy"  # Maximum review depth for hackathon
  require_score_threshold: true
  
tools:
  review:
    enabled: true
    security_scanning: true
  improve:
    enabled: true
  describe:
    enabled: true
```

## Option 2: PR-Agent GitHub Action (Self-Hosted Fallback)

If the Qodo app isn't available, use the open-source PR-Agent via GitHub Actions:

### Already Configured

The repository already includes `.github/workflows/pr-agent.yml` which:
- Triggers on every PR open and push
- Runs Qodo review automatically
- Posts findings as PR comments

### Required Secret

1. Go to **Settings → Secrets and variables → Actions**
2. Add a new secret: `OPENAI_KEY` with your OpenAI API key
3. The workflow will use this to power the AI review

## PR Workflow (Required for Hackathon)

### For Every Substantive Change:

```bash
# 1. Create a feature branch
git checkout -b feat/your-feature-name

# 2. Make your changes
# ... code ...

# 3. Commit with a descriptive message
git add .
git commit -m "feat: add new feature description"

# 4. Push and create PR
git push origin feat/your-feature-name
# Create PR on GitHub

# 5. Wait for Qodo review
# Qodo will automatically review the PR

# 6. Address findings
# - Fix all HIGH severity findings
# - Review MEDIUM and LOW findings
# - Dismiss invalid findings with explanation

# 7. Get final approval
# Team member reviews and merges
```

### What Judges Will Check

1. **PR titles are descriptive** — "feat: add neural threat detection" not "update code"
2. **PR descriptions explain the why** — not just what changed
3. **Qodo reviewed the PR** — review comments exist and were addressed
4. **HIGH findings were fixed or dismissed with reason** — no unresolved HIGHs
5. **Clean merge history** — no direct pushes to main

## Creating Good Pull Requests

### PR Title Format
```
<type>: <short description>

Types: feat, fix, refactor, docs, test, chore
```

Examples:
- `feat: add neuromorphic security processing engine`
- `fix: handle empty directory in threat scanner`
- `refactor: extract MCP tool registration into decorators`
- `docs: update README with TrueForge integration guide`

### PR Description Template
```markdown
## What
Brief description of what this PR does.

## Why
Why this change is needed. Link to issue if applicable.

## How
How the change was implemented. Key design decisions.

## Testing
How to verify the change works.

## Qodo Review
- [ ] Qodo review completed
- [ ] HIGH findings addressed
- [ ] MEDIUM findings reviewed
- [ ] LOW findings noted
```

## Evidence for Hackathon Submission

The README must include a `## Qodo Code Review Evidence` section with:
1. A link to at least one representative merged PR
2. 1-2 sentences on what Qodo surfaced
3. What you changed or intentionally dismissed
4. PR history showing the review flow

See the main README for the template.
