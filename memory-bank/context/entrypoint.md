# memory-bank/context Directory Guide for AI Agents

This directory contains contextual information and documentation that helps AI agents understand the project structure, requirements, and conventions. This guide provides detailed instructions on how to navigate, interpret, and utilize this context effectively.

## Directory Structure

```
memory-bank/context/
├── entrypoint.md                    # This file - the main navigation guide
├── INDEX.md                         # Main index for all context files
├── .gemini/                         # Gemini-specific configuration and context
├── guides/                          # How-to guides and procedures
│   └── local-testing.md            # Local development and testing procedures
└── spec/                           # Specification files and documentation
    ├── 000_MASTER/                 # Original specification content
    ├── 100_SPLIT/                  # Split specification sections
    ├── 200_INDEX/                  # Indexed and searchable content
    └── GUIDE.md                    # Specification navigation guide
```

## Quicklinks

- Main Index: [INDEX.md](INDEX.md)
- Spec index manifest: [spec/200_INDEX/MANIFEST.yaml](spec/200_INDEX/MANIFEST.yaml)
- Spec headings: [spec/200_INDEX/HEADINGS.json](spec/200_INDEX/HEADINGS.json)
- Spec keywords: [spec/200_INDEX/KEYWORDS.json](spec/200_INDEX/KEYWORDS.json)
- Spec cross-references: [spec/200_INDEX/XREF.json](spec/200_INDEX/XREF.json)
- Spec navigation guide: [spec/GUIDE.md](spec/GUIDE.md)
- Local testing guide: [guides/local-testing.md](guides/local-testing.md)
- External Context Management Rule: [../rules/external-context-management.md](../rules/external-context-management.md)

## Start Here (for Agents)

1. Skim the Spec manifest for structure: [spec/200_INDEX/MANIFEST.yaml](spec/200_INDEX/MANIFEST.yaml)
2. If needed, search by concept via keywords: [spec/200_INDEX/KEYWORDS.json](spec/200_INDEX/KEYWORDS.json)
3. Retrieve only the files relevant to your task (see rule above)
4. When testing with Docker, use: [guides/local-testing.md](guides/local-testing.md)
5. For local, non-containerized development, see the "Local Development" section below.

## Local Development (Non-Containerized)

The current development focus is on a local, non-containerized setup. The main application script is `agent_daemon_consolidated.py`.

**Important:** This script may contain hardcoded paths that assume a containerized environment (e.g., `/origin`, `/app/workspace`). Be prepared to modify these paths for your local setup.

## Agent Navigation Patterns

### 1. **Initial Context Gathering**
When starting work on this project, agents should:

1. **Read this entrypoint first** - Understand the overall structure
2. **Consult the Main Index (INDEX.md)** - For a comprehensive overview of all context files
3. **Check the spec directory** - Understand the current state of specifications
4. **Review relevant guides** - Learn procedures and conventions

### 2. **Context Hierarchy for Decision Making**
Use this priority order when making decisions:

1. **Current Specifications** (`spec/200_INDEX/`) - How it's currently defined
2. **Implementation Guides** (`guides/`) - How to implement
3. **Code Structure** (root directory) - Where to implement

### 3. **Context Search Patterns**
When looking for specific information:

- **Implementation details**: Check `spec/200_INDEX/` for indexed content
- **Procedures**: Look in `guides/` directory
- **Current state**: Review `spec/` directory structure

## Detailed Context Categories

### Specification Context (`spec/`)
The `spec/` directory contains the current state of specifications:

- **`000_MASTER/`**: Original, unprocessed specification content
- **`100_SPLIT/`**: Specification broken into logical sections
- **`200_INDEX/`**: Processed, searchable, and cross-referenced content
- **`GUIDE.md`**: Navigation guide for the specification structure

**Key Files in `200_INDEX/`**:
- `MANIFEST.yaml`: Overview of all specification sections
- `HEADINGS.json`: Hierarchical structure of content
- `KEYWORDS.json`: Searchable terms and concepts
- `XREF.json`: Cross-references between sections

### Implementation Guides (`guides/`)
The `guides/` directory contains procedural information:

- **`local-testing.md`**: How to set up and test locally with Docker.
- **Future guides**: Deployment, testing, debugging procedures

## Agent Decision-Making Framework

### 1. **Requirement Analysis**
When given a task:

1. **Identify the scope**: What part of the system is affected?
2. **Review current specifications**: How is this currently defined?
3. **Identify gaps**: What's missing or unclear?

### 2. **Implementation Planning**
Before writing code:

1. **Check existing patterns**: Look for similar implementations
2. **Review constraints**: Performance, reliability, scalability requirements
3. **Plan testing**: How will this be validated?

### 3. **Code Quality Assurance**
During implementation:

1. **Follow documented patterns**: Use established conventions
2. **Meet requirements**: Ensure functional and non-functional requirements are met
3. **Consider observability**: How will this be monitored and debugged?
4. **Document decisions**: Update context if new patterns emerge

## Context Navigation Commands

### For File System Navigation
```bash
# View directory structure
ls -la context/

# Read specific files (from repo root)
rg -n "^" context/spec/200_INDEX/MANIFEST.yaml | sed -n '1,80p'

# Search for content (prefer ripgrep)
rg -n "keyword" context/
```

### For Content Understanding
```bash
# Get overview of specifications
rg -n "^" context/spec/200_INDEX/MANIFEST.yaml | sed -n '1,120p'

# Find specific concepts
rg -n "Redis" context/spec/200_INDEX/

# Check cross-references
rg -n "^" context/spec/200_INDEX/XREF.json | sed -n '1,80p'
```

## Alignment with External Context Rule (must follow)

- Start with this entrypoint, then fetch only what you need next
- Prefer targeted retrieval over bulk loading; revisit Quicklinks when topics shift
- When you create or learn something valuable, add or update the appropriate file and then link it here

## Context Update Procedures

### When Adding New Context
1. **Choose appropriate category**: Guides or spec
2. **Follow naming conventions**: Use descriptive, lowercase filenames with hyphens
3. **Update this entrypoint**: Add new files to the directory structure
4. **Cross-reference**: Link to related existing context

### When Updating Existing Context
1. **Maintain consistency**: Ensure changes align with other documents
2. **Update references**: Fix any broken cross-references
3. **Version appropriately**: Note significant changes
4. **Notify stakeholders**: if changes affect implementation

## Current Project Context

Based on the existing specification, this project is building:

- A **distributed task processing system** with Coordinator and Agent components
- **Redis-based task queueing** for reliable job distribution
- **Postgres persistence** for task lifecycle management
- **Observability stack** (Prometheus, Loki, Grafana) for monitoring
- **Containerised deployment** with Docker and Fly.io is an option, but local development is also supported.

**Key Requirements**:
- Handle 1000+ tasks per minute reliably
- Provide end-to-end visibility and fault tolerance
- Support multiple agent types and task types
- Maintain data consistency across distributed components

## Agent Workflow Examples

### Example 1: Implementing a New Feature
1. **Check**: `spec/200_INDEX/MANIFEST.yaml` for current state
2. **Review**: `guides/local-testing.md` for testing procedures if using Docker.
3. **Implement**: Following documented patterns
4. **Test**: Using established testing procedures
5. **Update**: Context if new patterns emerge

### Example 2: Debugging an Issue
1. **Identify**: Which component is affected
2. **Check**: `spec/200_INDEX/` for component specifications
3. **Review**: `guides/` for debugging procedures
4. **Investigate**: Using observability tools mentioned in specs
5. **Document**: Any new debugging patterns discovered

### Example 3: Making Architectural Decisions
1. **Check**: `spec/200_INDEX/` for current implementation
2. **Evaluate**: Against documented requirements and constraints
3. **Document**: Decision rationale and trade-offs
4. **Update**: Relevant context files

## Context Quality Indicators

### Good Context Should:
- **Be current**: Reflect the actual state of the system
- **Be clear**: Unambiguous and easy to understand
- **Be complete**: Cover all necessary aspects
- **Be consistent**: Align across different documents
- **Be actionable**: Provide clear guidance for implementation

### Red Flags to Watch For:
- **Outdated information**: Specifications that don't match implementation
- **Conflicting guidance**: Different documents saying different things
- **Missing context**: Important decisions not documented
- **Unclear requirements**: Vague or ambiguous specifications

## Getting Help and Support

### When Context is Unclear:
1. **Check multiple sources**: Don't rely on single documents
2. **Look for patterns**: How are similar issues handled?
3. **Review implementation**: Check actual code for guidance
4. **Ask for clarification**: Request more specific requirements

### When Context is Missing:
1. **Document what you learn**: Create new context as you work
2. **Follow established patterns**: Use similar existing context as templates
3. **Update this entrypoint**: Keep the navigation guide current
4. **Share knowledge**: Help other agents by improving context

## Best Practices for Agents

### 1. **Always Start with Context**
- Read relevant documentation before coding
- Understand requirements and constraints
- Check for existing patterns and solutions

### 2. **Keep Context Current**
- Update documentation when you discover new information
- Document decisions and trade-offs
- Maintain consistency across all context files

### 3. **Use Context for Validation**
- Validate implementations against documented requirements
- Use specifications as acceptance criteria
- Flag deviations from established patterns

### 4. **Improve Context Quality**
- Make context more clear and actionable
- Add examples and use cases
- Organize information logically

## Maintainers: Keep This Entrypoint Current

When adding or changing context:

1. Place files in the correct subdirectory (spec, guides)
2. Use descriptive, lowercase, hyphenated filenames
3. Add/update a Quicklink when the file is generally useful
4. Update the directory diagram if structure changes
5. Validate links to: MANIFEST.yaml, HEADINGS.json, KEYWORDS.json, XREF.json
6. Cross-reference related files where helpful
7. Keep this section short and practical

## Remember

This context directory is a living document that should grow and improve with the project. As an AI agent:

- **Read context first** before starting work
- **Update context** when you discover new information
- **Maintain consistency** across all documentation
- **Help other agents** by improving context quality
- **Use context as your guide** for all decisions and implementations

The better the context, the more effectively agents can work on this project. Your contributions to improving this context are valuable and help the entire team succeed.