# Labs - Agent Skills Training

## Overview

This directory contains labs for learning and practicing agent skills and context engineering.

## Structure

```
labs/
├── lab1/          # First Contact - Vibe coding prototype
├── lab2/          # Context Engineering - AGENTS.md and Skills
└── README.md      # This file
```

## Lab 1 - First Contact (~1.5 h)

**Objective**: Vibe-code a small prototype from natural language using a coding agent, then locate it on the spectrum (vibe → structured → agentic).

**Deliverables**:
- Working prototype (Log Analyzer)
- REFLECTION.md with 5-question rubric

**Key Learning**: Feel the shift from writing syntax to stating intent, and see honestly where your process sits.

## Lab 2 - Context Engineering (~2 h)

**Objective**: Give your Lab 1 project a "brain," then prove it works.

**Deliverables**:
- AGENTS.md - Project README for agents
- Reusable Skill (log-pattern-matcher)
- Before/after comparison with metrics

**Key Learning**: Structure — not a smarter model — is what moves you rightward toward reliable agentic engineering.

## Prerequisites

### Setup Codex (Optional)

```bash
# Install Codex CLI
npm i -g @openai/codex

# Or on macOS
brew install codex

# Sign in
codex
```

### Read Standards

- Agent Skills / SKILL.md standard: https://github.com/agentskills/agentskills
- AGENTS.md standard: https://agents.md/

## Getting Started

1. **Complete Lab 1** first to understand your current workflow
2. **Read the standards** to understand best practices
3. **Complete Lab 2** to add structure and improve reliability
4. **Review the comparison** in Lab 2 to see the impact

## Resources

- **Codex CLI**: https://developers.openai.com/codex/cli
- **Free Tier Details**: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- **Agent Skills**: https://github.com/agentskills/agentskills
- **AGENTS.md**: https://agents.md/

## Learning Outcomes

After completing these labs, you will:

1. Understand where your current workflow sits on the spectrum
2. Know how to create effective AGENTS.md files
3. Be able to build reusable Skills
4. Measure the impact of context engineering
5. Apply these skills to production projects

## Applying to Main Project

The skills learned in these labs can be applied to the main telecom project:

1. Create an **AGENTS.md** for the telecom platform
2. Build **Skills** for common patterns (Kafka, Elasticsearch, Spark)
3. Use structured prompts for reliable agent interactions
4. Measure improvement in development velocity

## Next Steps

1. Complete both labs
2. Apply lessons to the main telecom project
3. Create AGENTS.md for the telecom platform
4. Build telecom-specific Skills
5. Share learnings with team
