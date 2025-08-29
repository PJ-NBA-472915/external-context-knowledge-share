# Context File Version Control Schema

## Overview
This document defines the version control schema for context files in the memory-bank system. The schema enables systematic versioning, change tracking, and rollback capabilities for external context management.

## Version Metadata Structure

### YAML Frontmatter
All context files must include YAML frontmatter at the beginning of the file with the following structure:

```yaml
---
version: "1.0.0"
version_type: "patch"
last_updated: "2025-08-29 09:25"
change_log: "Initial version with basic context structure"
dependencies: []
breaking_changes: false
author: "system"
checksum: "sha256:abc123..."
---
```

### Version Fields

#### `version` (Required)
- **Format**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Example**: "1.0.0", "2.1.3", "1.0.0-alpha.1"
- **Rules**: Must follow semver.org specification

#### `version_type` (Required)
- **Values**: "major", "minor", "patch", "pre-release"
- **Purpose**: Indicates the type of change made
- **Rules**: Must match the version increment type

#### `last_updated` (Required)
- **Format**: ISO 8601 timestamp (YYYY-MM-DD HH:MM)
- **Example**: "2025-08-29 09:25"
- **Purpose**: Tracks when the file was last modified

#### `change_log` (Required)
- **Format**: Human-readable description of changes
- **Example**: "Added new context categories for product specifications"
- **Purpose**: Documents what changed in this version

#### `dependencies` (Optional)
- **Format**: Array of context file paths
- **Example**: ["../rules/external-context-management.md"]
- **Purpose**: Tracks relationships between context files

#### `breaking_changes` (Required)
- **Format**: Boolean
- **Default**: false
- **Purpose**: Indicates if changes break existing functionality

#### `author` (Required)
- **Format**: String identifier
- **Example**: "system", "jaak", "agent-001"
- **Purpose**: Tracks who made the changes

#### `checksum` (Required)
- **Format**: SHA256 hash of file content (excluding frontmatter)
- **Example**: "sha256:abc123def456..."
- **Purpose**: Enables change detection and integrity verification

## Version Bumping Rules

### Patch Version (1.0.0 → 1.0.1)
- **Triggers**: 
  - Minor text corrections
  - Formatting improvements
  - Non-functional changes
  - Documentation updates
- **Examples**: Fix typos, improve readability, update examples

### Minor Version (1.0.0 → 1.1.0)
- **Triggers**:
  - New features or capabilities
  - Enhanced functionality
  - Additional context categories
  - Non-breaking improvements
- **Examples**: Add new context sections, enhance navigation, new examples

### Major Version (1.0.0 → 2.0.0)
- **Triggers**:
  - Breaking changes
  - Structural modifications
  - Incompatible updates
  - Major refactoring
- **Examples**: Restructure context hierarchy, change file formats, remove features

### Pre-release Versions
- **Format**: 1.0.0-alpha.1, 1.0.0-beta.2, 1.0.0-rc.1
- **Purpose**: Indicate work-in-progress or testing versions
- **Rules**: Must increment the appropriate version component

## File Organization

### Context Categories
```
memory-bank/context/
├── entrypoint.md                    # Main navigation (versioned)
├── spec/                           # Specifications (versioned)
│   ├── version-control-schema.md   # This document
│   └── context-structure.md        # Context organization rules
├── product/                        # Product context (versioned)
├── technical/                      # Technical context (versioned)
├── team/                          # Team context (versioned)
├── project/                       # Project context (versioned)
└── versions/                      # Version history (auto-generated)
    ├── entrypoint/
    │   ├── 1.0.0.md
    │   ├── 1.1.0.md
    │   └── 2.0.0.md
    └── rules/
        ├── external-context-management/
        │   ├── 1.0.0.md
        │   └── 1.1.0.md
        └── task-file-usage/
            ├── 1.0.0.md
            └── 1.0.1.md
```

### Version History Directory
- **Purpose**: Maintains complete history of all context file versions
- **Structure**: Organized by file path and version
- **Auto-generation**: Created automatically by version control system
- **Access**: Read-only for agents, write-only for system

## Validation Rules

### Required Fields
- All required fields must be present and valid
- Version format must match semantic versioning
- Timestamps must be valid ISO 8601 format
- Checksums must be valid SHA256 hashes

### Consistency Checks
- Version type must match version increment
- Dependencies must reference valid context files
- Breaking changes flag must align with version bump type
- File content checksum must match stored checksum

### Dependency Validation
- Circular dependencies are not allowed
- All referenced dependencies must exist
- Dependency versions must be compatible
- Breaking changes in dependencies must be handled

## Implementation Notes

### Frontmatter Parsing
- Use YAML frontmatter parser for metadata extraction
- Handle missing or malformed frontmatter gracefully
- Provide clear error messages for validation failures
- Support both YAML and JSON frontmatter formats

### Checksum Calculation
- Calculate SHA256 of file content excluding frontmatter
- Handle line ending normalization (CRLF vs LF)
- Ignore whitespace differences in validation
- Cache checksums for performance

### Version Comparison
- Implement semantic version comparison logic
- Handle pre-release version ordering correctly
- Support version range specifications
- Provide human-readable version differences

## Migration Strategy

### Phase 1: Schema Implementation
1. Create version control schema specification
2. Implement metadata validation system
3. Add version metadata to existing context files
4. Create version history directory structure

### Phase 2: Tooling Development
1. Build CLI tools for version management
2. Implement automated version bumping
3. Create rollback and restore functionality
4. Add Git integration for distributed version control

### Phase 3: System Integration
1. Integrate version control with existing workflows
2. Add automated validation and consistency checks
3. Implement dependency tracking and resolution
4. Create comprehensive testing suite

## Future Enhancements

### Advanced Features
- Semantic change detection using AI/ML
- Automated impact analysis for breaking changes
- Context file dependency graphs
- Version compatibility matrices
- Rollback impact assessment

### Integration Opportunities
- CI/CD pipeline integration
- Automated documentation generation
- Change notification systems
- Performance impact tracking
- Security vulnerability scanning
