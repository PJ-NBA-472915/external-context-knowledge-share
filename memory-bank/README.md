# Memory Bank

A centralized repository for Cursor development rules, project context, and development tools.

## Overview

The Memory Bank is a centralized submodule that provides:
- **Rules**: Cursor rules for consistent development practices
- **Context**: Project context and specifications
- **Scripts**: Setup and utility scripts
- **Tasks**: Development task tracking

## Quick Start

### 1. Initialize the Submodule

If you're cloning this repository for the first time:

```bash
# Clone the main repository
git clone <your-repo-url>
cd <repo-name>

# Initialize and update submodules
git submodule update --init --recursive
```

### 2. Set Up Cursor Rules Link

Automatically link your `.cursor/rules` directory to the centralized rules:

```bash
# Run the setup script
./memory-bank/scripts/setup-cursor-rules.sh

# Or use the Makefile target (if available)
make setup-cursor-rules
```

## Directory Structure

```
memory-bank/
├── README.md           # This file
├── rules/              # Cursor rules
├── context/            # Project context and specifications
├── scripts/            # Setup and utility scripts
└── tasks/              # Development task tracking
```

After setup, your project structure will look like:

```
your-project/
├── .cursor/
│   └── rules -> memory-bank/rules (symlink)
├── memory-bank/        # This submodule
└── ... (other project files)
```

## Testing

The Memory Bank project uses pytest for comprehensive testing following established testing standards.

### Test Structure

Tests are organized into three categories:

```
tests/
├── unit/               # Unit tests for individual functions/classes
├── integration/        # Integration tests for component interactions
├── functional/         # End-to-end functional tests
└── data/               # Test data files
```

### Running Tests

#### Using Makefile (Recommended)

```bash
# Run all tests
make test

# Run specific test categories
make test-unit          # Unit tests only
make test-integration   # Integration tests only
make test-functional    # Functional tests only

# Run tests with coverage
make test-cov
```

#### Using pytest directly

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
python3 -m pytest tests/ -v

# Run specific test categories
python3 -m pytest tests/ -m unit -v
python3 -m pytest tests/ -m integration -v
python3 -m pytest tests/ -m functional -v

# Run with coverage
python3 -m pytest tests/ --cov=manager --cov-report=term-missing
```

### Test Categories

- **Unit Tests** (`@pytest.mark.unit`): Test individual functions and classes in isolation
- **Integration Tests** (`@pytest.mark.integration`): Test interactions between components
- **Functional Tests** (`@pytest.mark.functional`): Test complete workflows and end-to-end scenarios

### Test Coverage

Current test coverage: **94%**

- `manager/__init__.py`: 100%
- `manager/spec_manager.py`: 93%

### Test Configuration

The project includes:
- `pytest.ini`: Main pytest configuration with markers and options
- `conftest.py`: Shared fixtures for all tests
- Custom markers for test categorization
- Coverage reporting with pytest-cov

### Writing Tests

When adding new tests:

1. **Follow naming conventions**: Use `test_*.py` for test files
2. **Use appropriate markers**: Mark tests with `@pytest.mark.unit`, `@pytest.mark.integration`, or `@pytest.mark.functional`
3. **Leverage fixtures**: Use shared fixtures from `conftest.py` for common setup
4. **Follow AAA pattern**: Arrange, Act, Assert structure
5. **Test edge cases**: Include error handling and boundary condition tests

### Example Test

```python
@pytest.mark.unit
def test_spec_manager_initialization():
    """Test SpecManager initializes correctly."""
    manager = SpecManager()
            assert manager.spec_dir == Path("context/spec")
    assert "spec" in str(manager.base_path)
```

## Scripts

### setup-cursor-rules.sh

**Purpose**: Sets up a symbolic link from `.cursor/rules` to `memory-bank/rules` in the parent project.

**Usage**:
```bash
# From project root
./memory-bank/scripts/setup-cursor-rules.sh

# From within memory-bank directory
./scripts/setup-cursor-rules.sh

# Via Makefile (if available)
make setup-cursor-rules
```

**Features**:
- Automatic submodule validation
- Safe backup of existing rules
- Symlink creation and verification
- Colored output for clear status reporting

**Requirements**:
- Must be run from project root or from within memory-bank/
- Git must be available
- Memory-bank must be properly initialized as a submodule

## What the Setup Script Does

The `setup-cursor-rules.sh` script:

1. **Validates Submodule**: Ensures the memory-bank is properly initialized
2. **Creates Directories**: Sets up `.cursor` directory if needed
3. **Handles Existing Rules**: Safely backs up any existing `.cursor/rules` content
4. **Creates Symlink**: Links `.cursor/rules` → `memory-bank/rules`
5. **Verifies Setup**: Confirms the link works correctly

## Manual Setup (Alternative)

If you prefer to set up the link manually:

```bash
# Create .cursor directory if it doesn't exist
mkdir -p .cursor

# Remove existing rules directory/link if present
rm -rf .cursor/rules

# Create symbolic link
ln -sf "$(pwd)/memory-bank/rules" .cursor/rules
```

## Benefits

- **Centralized Rules**: All Cursor rules are stored in one place
- **Version Controlled**: Rules are tracked in the memory-bank repository
- **Team Consistency**: Everyone uses the same development rules
- **Easy Updates**: Changes automatically propagate to all linked projects
- **Backup Safety**: Existing rules are preserved during setup

## Updating Rules

To update the rules:

1. **Pull Latest Changes**:
   ```bash
   git submodule update --remote memory-bank
   ```

2. **Rules Automatically Update**: Since `.cursor/rules` is a symlink, changes are immediately available

## Integration

### Makefile Integration

Add this target to your project's Makefile:

```makefile
setup-cursor-rules:
	@echo "Setting up .cursor/rules link to memory-bank/rules..."
	@if [ -f "memory-bank/scripts/setup-cursor-rules.sh" ]; then \
		./memory-bank/scripts/setup-cursor-rules.sh; \
	else \
		echo "❌ Setup script not found"; \
		exit 1; \
	fi
```

### CI/CD Integration

These scripts are designed to integrate with:
- Project Makefiles
- CI/CD pipelines
- Development workflows
- Team onboarding processes

## Script Design Principles

All scripts in this directory follow these principles:

1. **Portable**: Scripts can run from multiple locations
2. **Safe**: Include validation and backup mechanisms
3. **Informative**: Provide clear, colored output
4. **Robust**: Handle edge cases and provide helpful error messages
5. **Self-contained**: Minimal external dependencies

## Contributing to Rules

To add or modify rules:

1. **Edit Rules**: Modify files in `memory-bank/rules/`
2. **Commit Changes**: Commit to the memory-bank repository
3. **Update Projects**: Run `git submodule update --remote memory-bank` in linked projects

## Troubleshooting

### Submodule Issues

If you encounter submodule problems:

```bash
# Reinitialize the submodule
git submodule deinit -f memory-bank
git submodule update --init --recursive
```

### Broken Symlink

If the symlink becomes broken:

```bash
# Remove broken link
rm .cursor/rules

# Recreate using the setup script
./memory-bank/scripts/setup-cursor-rules.sh
```

### Permission Issues

If you get permission errors:

```bash
# Make the script executable
chmod +x memory-bank/scripts/setup-cursor-rules.sh
```

## Adding New Scripts

When adding new scripts to the `scripts/` directory:

1. **Follow naming convention**: Use descriptive names with `.sh` extension
2. **Include shebang**: Start with `#!/bin/bash`
3. **Add error handling**: Use `set -e` and proper exit codes
4. **Document usage**: Include help text and examples
5. **Test thoroughly**: Verify from different working directories

## Support

For issues or questions:
- Check the script output for error messages
- Ensure you're running from the project root directory
- Verify git and submodule setup
- Check file permissions on the setup script
