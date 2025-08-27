# Project: Cage - Multi-Agent Locking Mechanism

## Project Overview

Cage is a robust, repo-local multi-agent locking mechanism designed to enable multiple autonomous agents to work concurrently on the same codebase without conflicts. It provides a serverless, file-based coordination system to manage work claims, prevent overlapping edits, and maintain an auditable state.

### Key Features
- **Concurrent Work Claims**: Agents can claim exclusive access to specific files, directories, or conceptual topics
- **Conflict Prevention**: Automatic detection of overlapping claims prevents conflicting modifications
- **Auditable State**: All active claims and completed work are logged in JSON registries for transparency
- **Crash Safety**: Atomic file operations ensure data integrity even in event of agent crashes
- **Stale Lock Management**: Mechanisms to detect and automatically reap stale (expired) claims
- **CLI Utilities**: Easy-to-use command-line tools for claiming, releasing, renewing, and monitoring locks
- **Agent Integration Guidelines**: Comprehensive documentation on agent interaction patterns

### Tech Stack
- **Core Language**: Python 3.10+
- **Development Environment**: Devbox with Python 3.10
- **Lock Management**: Custom Python-based lock manager with atomic file operations
- **Agent Framework**: CrewAI with LangChain integration
- **Process Management**: Supervisor for container orchestration
- **Testing**: pytest with comprehensive testing suite
- **Logging**: Loguru for structured logging
- **Async Support**: uvloop for enhanced async performance
- **Container Support**: Docker/Podman with Fly.io deployment ready

## General Instructions for AI Agents

### Memory-Bank System (CRITICAL - Always Start Here)
This project uses a comprehensive memory-bank system for context management. **ALWAYS start by reading the entrypoint file** at `memory-bank/context/entrypoint.md` to understand the project structure and navigation patterns.

**Why This Matters**: The entrypoint provides the foundation for understanding how to work in this repository. It contains navigation patterns, context hierarchy, and decision-making frameworks that are essential for effective work.

### Task Orchestration
- All work must be orchestrated through `memory-bank/tasks/[current-date]-[taskname].json` files
- Follow the task orchestration rules defined in the memory-bank system
- Update task files with progress, decisions, and lessons learned
- Use the established JSON task format for consistency

### Development Environment
- Use `devbox run` for all commands (never use `devbox shell`)
- The project includes comprehensive development tooling with concurrent processes
- Support both local development and containerized deployment

## Coding Standards

### Python
- Follow PEP 8 coding standards
- Use type hints for function parameters and return values
- Implement proper error handling and logging
- Use async/await patterns where appropriate
- Follow the established patterns in the existing codebase

### Testing
- Use pytest for all testing (not unittest)
- Write comprehensive unit and integration tests
- Maintain high test coverage for critical business logic
- Use the established testing patterns in the project

### Code Quality
- Use established linting and formatting tools
- Follow the project's existing code organization patterns
- Document complex logic and business rules
- Use consistent naming conventions

## Project-Specific Rules

### Multi-Agent Coordination
- Always use the locking mechanism before making changes
- Follow the established claim/release workflow
- Respect existing claims and avoid conflicts
- Use the CLI tools for all coordination operations

### Lock Management
- Claim locks for the specific scope you're working on
- Renew locks if work takes longer than expected
- Release locks immediately when work is complete
- Use descriptive intent messages for all claims

### File Operations
- Use atomic file operations where possible
- Follow the established file organization patterns
- Maintain consistency with existing code structure
- Update documentation when making architectural changes

## File Organization

### Core Structure
- `./coordination/`: Contains all coordination files, including active claims, completed work logs, individual lock files, and configuration
- `./tools/locking/`: Houses the Python-based CLI utilities (`lock-claim`, `lock-release`, `lock-status`, etc.)
- `./memory-bank/`: Context management and task orchestration system
- `./scrapbook/`: Development artifacts and experimental code

### Key Components
- **Lock Manager**: Core locking logic and coordination
- **Agent Daemon**: Consolidated agent service for task execution
- **CLI Tools**: Command-line interface for lock management
- **Task System**: JSON-based task orchestration and tracking

## Development Workflow

### Before Starting Work
1. **ALWAYS read `memory-bank/context/entrypoint.md` first** - This is mandatory
2. Create or update task file in `memory-bank/tasks/`
3. Claim appropriate locks for your work scope
4. Understand the specific area you're working on
5. Review existing patterns and implementations

### During Development
1. Follow established coding patterns
2. Write tests as you develop
3. Update task file with progress and decisions
4. Use proper Git commit messages (conventional commits, no scope)
5. Maintain locks appropriately

### Code Quality
- Run `devbox run pytest` for Python tests
- Use established linting and formatting tools
- Follow the project's code organization patterns
- Maintain consistency with existing implementations

## Dependencies

### Adding New Dependencies
- **Avoid introducing new external dependencies unless absolutely necessary**
- If a new dependency is required, state the reason clearly
- Consider if existing Python ecosystem packages can solve the problem
- Ensure compatibility with the current tech stack versions
- Update `requirements.txt` as needed

### Dependency Management
- Use pip for Python dependencies
- Keep dependencies up to date and secure
- Document any breaking changes or migration requirements
- Follow the established dependency patterns

## Memory-Bank Integration

### Context Files
- Use `memory-bank/context/` for project-specific information
- Follow the selective retrieval principle - only read what you need
- Update context files when you discover new patterns or information
- Use the INDEX.md file for navigation

### Task Management
- All work must be tracked in JSON task files
- Update progress, decisions, and lessons learned
- Follow the task orchestration workflow
- Maintain proper task file hygiene

## Getting Help

### When You Need Context
1. **START with `memory-bank/context/entrypoint.md`** - This is your foundation
2. Use the INDEX.md file for navigation
3. Check relevant context files in `memory-bank/context/`
4. Review existing implementations for patterns

### When You're Stuck
1. Check the task file for context and decisions
2. Review the memory-bank system for guidance
3. Look at existing code for similar patterns
4. Update the task file with blockers and proposed solutions

## Success Metrics

You're working effectively when:
- ✅ You **ALWAYS start with the memory-bank entrypoint**
- ✅ You follow the memory-bank system and task orchestration
- ✅ Your code follows Python best practices
- ✅ You write comprehensive pytest tests
- ✅ You maintain proper lock management
- ✅ You update task files with progress and decisions
- ✅ Your implementations align with existing patterns

## Autonomous Operation Guidelines

### For Gemini CLI Users
**IMPORTANT**: This project is designed for autonomous operation. The gemini-cli should:

1. **Always start by reading `memory-bank/context/entrypoint.md`** - This provides the foundation for understanding the project
2. **Use the memory-bank system** to find answers to questions rather than asking the user
3. **Follow the established patterns** documented in the context files
4. **Make decisions autonomously** based on the documented rules and patterns
5. **Only ask questions when the context is genuinely unclear** and cannot be resolved through the memory-bank system

### What This Means
- **Don't ask for clarification** on things that are documented in the memory-bank
- **Don't ask for guidance** on established patterns or workflows
- **Do read the context files** to understand requirements and constraints
- **Do follow the documented procedures** for task orchestration and development
- **Do make autonomous decisions** based on the established rules

### Example Autonomous Behavior
Instead of asking: "What testing framework should I use?"
- **Read the context files** to find the established testing patterns
- **Follow the documented procedures** for running tests
- **Use the established tools** (pytest) as documented

Instead of asking: "How should I organize this code?"
- **Check the existing codebase** for established patterns
- **Follow the documented file organization** rules
- **Maintain consistency** with existing implementations

## Remember

This is a sophisticated multi-agent coordination system. Always consider:
- **Scalability**: How will this work with multiple concurrent agents?
- **Reliability**: How will this handle failures and edge cases?
- **Maintainability**: How will this integrate with existing patterns?
- **Autonomy**: How can this be implemented without requiring user intervention?

The better you understand and follow the memory-bank system, the more effectively you can work autonomously on this project.