---
version: 1.1.0
version_type: minor
last_updated: 2025-08-29 09:35
change_log: Added version control metadata and automated version bumping tool
dependencies: []
breaking_changes: false
author: system
checksum: sha256:85205b01d9bc4439b462881f751688bc4e873159aeff7176ded0c1116d1d7817
---

# memory-bank/context Directory Guide for AI Agents

This directory contains contextual information and documentation that helps AI agents understand the project structure, requirements, and conventions. This guide provides detailed instructions on how to navigate, interpret, and utilize this context effectively.

## Directory Structure

```
.
├── .cursor/
├── .git/
├── .gitignore
├── .DS_Store
├── LICENSE
├── README.md
├── _templates/
├── assets/
├── deep-research/
├── docs/
├── memory-bank/
│   ├── .gitignore
│   ├── LICENSE
│   ├── README.md
│   ├── context/
│   │   ├── entrypoint.md                    # This file - the main navigation guide
│   │   └── spec/
│   ├── gemini/
│   │   ├── GEMINI.md                        # Gemini-specific project overview and instructions
│   │   └── settings.json
│   ├── requests/
│   ├── rules/
│   └── tasks/
└── presentation/
```

## Quicklinks

- Project Overview (for Gemini): [../gemini/GEMINI.md](../gemini/GEMINI.md)
- External Context Management Rule: [../rules/external-context-management.md](../rules/external-context-management.md)

## Start Here (for Agents)

1. **ALWAYS start by reading the project overview**: [../gemini/GEMINI.md](../gemini/GEMINI.md)
2. Consult the `memory-bank/context/` directory for additional context as needed.
3. Retrieve only the files relevant to your task (see rule above).

## Agent Navigation Patterns

### 1. **Initial Context Gathering**
When starting work on this project, agents should:

1. **Read the project overview (`memory-bank/gemini/GEMINI.md`) first** - Understand the overall structure and specific instructions for Gemini.
2. **Consult the `memory-bank/context/` directory** - For additional context and specific rules.
3. **Review relevant guides and rules** - Learn procedures and conventions.

### 2. **Context Hierarchy for Decision Making**
Use this priority order when making decisions:

1. **Project Overview (`memory-bank/gemini/GEMINI.md`)** - The primary source of truth for project-specific rules and guidelines.
2. **Relevant Context Files (`memory-bank/context/`)** - Specific documentation within this directory.
3. **Code Structure** (root directory) - Existing implementations and patterns.

### 3. **Context Search Patterns**
When looking for specific information:

- **Project-specific details**: Check `memory-bank/gemini/GEMINI.md`.
- **General procedures or rules**: Look in `memory-bank/rules/` and `memory-bank/context/` directories.
- **Current state**: Review the overall project structure and relevant documentation.

## Agent Decision-Making Framework

### 1. **Requirement Analysis**
When given a task:

1. **Identify the scope**: What part of the system is affected?
2. **Review current project documentation**: How is this currently defined in `memory-bank/gemini/GEMINI.md` and other relevant context files?
3. **Identify gaps**: What's missing or unclear?

### 2. **Implementation Planning**
Before writing code:

1. **Check existing patterns**: Look for similar implementations within the project.
2. **Review constraints**: Consider performance, reliability, and scalability requirements.
3. **Plan testing**: How will this be validated?

### 3. **Code Quality Assurance**
During implementation:

1. **Follow documented patterns**: Use established conventions from `memory-bank/gemini/GEMINI.md` and other rules.
2. **Meet requirements**: Ensure functional and non-functional requirements are met.
3. **Consider observability**: How will this be monitored and debugged?
4. **Document decisions**: Update context if new patterns emerge.

## Context Quality Indicators

### Good Context Should:
- **Be current**: Reflect the actual state of the project.
- **Be clear**: Unambiguous and easy to understand.
- **Be complete**: Cover all necessary aspects.
- **Be consistent**: Align across different documents.
- **Be actionable**: Provide clear guidance for implementation.

### Red Flags to Watch For:
- **Outdated information**: Documentation that doesn't match implementation.
- **Conflicting guidance**: Different documents saying different things.
- **Missing context**: Important decisions not documented.
- **Unclear requirements**: Vague or ambiguous specifications.

## Getting Help and Support

### When Context is Unclear:
1. **Check multiple sources**: Don't rely on single documents.
2. **Look for patterns**: How are similar issues handled in the existing codebase?
3. **Review implementation**: Check actual code for guidance.
4. **Ask for clarification**: Request more specific requirements from the user.

### When Context is Missing:
1. **Document what you learn**: Create new context as you work.
2. **Follow established patterns**: Use similar existing context as templates.
3. **Update this entrypoint**: Keep the navigation guide current.
4. **Share knowledge**: Help other agents by improving context.

## Best Practices for Agents

### 1. **Always Start with Context**
- Read relevant documentation (especially `memory-bank/gemini/GEMINI.md`) before coding.
- Understand requirements and constraints.
- Check for existing patterns and solutions.

### 2. **Keep Context Current**
- Update documentation when you discover new information.
- Document decisions and trade-offs.
- Maintain consistency across all context files.

### 3. **Use Context for Validation**
- Validate implementations against documented requirements.
- Use project guidelines as acceptance criteria.
- Flag deviations from established patterns.

### 4. **Improve Context Quality**
- Make context more clear and actionable.
- Add examples and use cases.
- Organize information logically.

## Maintainers: Keep This Entrypoint Current

When adding or changing context:

1. Place files in the correct subdirectory (e.g., `context/`, `rules/`, `gemini/`).
2. Use descriptive, lowercase, hyphenated filenames.
3. Add/update a Quicklink when the file is generally useful.
4. Update the directory diagram if structure changes.
5. Validate links to relevant files.
6. Cross-reference related files where helpful.
7. Keep this section short and practical.

## Remember

This context directory is a living document that should grow and improve with the project. As an AI agent:

- **Read context first** before starting work.
- **Update context** when you discover new information.
- **Maintain consistency** across all documentation.
- **Help other agents** by improving context quality.
- **Use context as your guide** for all decisions and implementations.

The better the context, the more effectively agents can work on this project. Your contributions to improving this context are valuable and help the entire team succeed.