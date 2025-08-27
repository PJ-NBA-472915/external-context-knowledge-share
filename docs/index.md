# Knowledge Share: External Context Management

*A Markdown book and research repository for knowledge-share sessions*

## Project Purpose

This repository serves as a **Markdown book** designed for live presentation during knowledge-share sessions, with a long-lived store of research notes and experiments. It's built for technical peers to consume both synchronously (during live sessions) and asynchronously (for self-study and reference).

**Core Intent**: Provide a comprehensive, navigable knowledge base that can be presented from directly, with clickable links, embedded images, and reproducible research that others can build upon.

## How to Use This Book

### For Live Sessions
- Navigate directly to relevant sections using the table of contents
- Use embedded images and diagrams for visual explanations
- Follow clickable links to related concepts and research
- Reference experiment results and findings in real-time

### For Self-Study
- Start with the introduction and work through concepts systematically
- Review research notes for deeper understanding
- Replicate experiments using provided data and methodologies
- Use session guides to understand how concepts were presented

## Table of Contents

### [00 - Introduction](00-introduction/)
- [Repository Overview](00-introduction/README.md)
- [Getting Started](00-introduction/getting-started.md)
- [Conventions & Standards](00-introduction/conventions.md)

### [10 - Core Concepts](10-concepts/)
- [External Context Management](10-concepts/external-context-management.md)
- [Multi-Agent Workflows](10-concepts/multi-agent-workflows.md)
- [Knowledge Sharing Patterns](10-concepts/knowledge-sharing-patterns.md)

### [20 - Research](20-research/)
- [State Management Approaches](20-research/state-management-approaches.md)
- [Distributed System Patterns](20-research/distributed-system-patterns.md)
- [Agent Communication Protocols](20-research/agent-communication-protocols.md)

### [30 - Experiments](30-experiments/)
- [Locking Mechanism Tests](30-experiments/locking-mechanism-tests.md)
- [Performance Benchmarks](30-experiments/performance-benchmarks.md)
- [Failure Mode Analysis](30-experiments/failure-mode-analysis.md)

### [40 - Session Guides](40-session-guides/)
- [Session 1: Introduction to External Context](40-session-guides/session-01-introduction.md)
- [Session 2: Advanced Patterns](40-session-guides/session-02-advanced-patterns.md)
- [Session 3: Practical Implementation](40-session-guides/session-03-implementation.md)

### [90 - Appendix](90-appendix/)
- [Glossary](90-appendix/glossary.md)
- [References](90-appendix/references.md)
- [Change Log](90-appendix/changelog.md)

## Research & Experiments Protocol

### Research Notes
- **Location**: `20-research/` directory
- **Format**: Markdown with clear problem statement, methodology, and findings
- **Required Sections**: Abstract, Background, Methods, Results, Discussion, References
- **Template**: Use `_templates/research/research-note-template.md`

### Experiments
- **Location**: `30-experiments/` directory
- **Format**: Reproducible experiments with clear setup and results
- **Required Sections**: Hypothesis, Setup, Procedure, Results, Analysis, Conclusions
- **Template**: Use `_templates/experiments/experiment-template.md`
- **Data**: Store raw data in `assets/data/` with clear README documentation

### Session Guides
- **Location**: `40-session-guides/` directory
- **Format**: Step-by-step presentation guides with timing and interaction points
- **Required Sections**: Objectives, Agenda, Key Points, Interactive Elements, Q&A Preparation
- **Template**: Use `_templates/session-guides/session-guide-template.md`

## Contribution & Update Workflow

### Adding New Content
1. **Choose appropriate directory** based on content type
2. **Use relevant template** from `_templates/` directory
3. **Follow naming conventions**: lowercase with hyphens, descriptive names
4. **Update this index** with new section links
5. **Ensure all links resolve** and images are properly referenced

### Content Standards
- **Language**: UK English throughout
- **Format**: Markdown-first, compatible with static site generators
- **Links**: All internal links must resolve; external links must be traceable
- **Images**: Store in `assets/images/` with descriptive filenames
- **Data**: Store in `assets/data/` with clear documentation

### Review Process
1. **Self-review**: Check all links and references
2. **Peer review**: Have another contributor review for clarity and accuracy
3. **Update index**: Ensure new content is properly linked in table of contents

## Repository Setup

To set up this repository structure on your local machine, run the following commands:

```bash
# 1. Create main documentation structure
mkdir -p docs/{00-introduction,10-concepts,20-research,30-experiments,40-session-guides,90-appendix}

# 2. Create assets directories
mkdir -p assets/{images,diagrams,data}

# 3. Create template directories
mkdir -p _templates/{research,experiments,session-guides}

# 4. Verify docs/index.md exists (this file)
# If missing, copy the entrypoint template here

# 5. Update root README.md to point to docs/index.md
```

### Directory Structure
```
docs/
├── index.md                    # This file - main entrypoint
├── 00-introduction/           # Getting started and conventions
├── 10-concepts/              # Core concepts and theory
├── 20-research/              # Research notes and findings
├── 30-experiments/           # Reproducible experiments
├── 40-session-guides/        # Presentation and session guides
└── 90-appendix/              # Reference materials

assets/
├── images/                    # Visual content and screenshots
├── diagrams/                  # Technical diagrams and flowcharts
└── data/                     # Datasets and research data

_templates/
├── research/                 # Research note templates
├── experiments/              # Experiment templates
└── session-guides/           # Session guide templates
```

## Licence & Attribution

This repository is licensed under the [LICENSE](LICENSE) file in the root directory. When contributing:

- **Cite sources**: Always attribute external research and ideas
- **Respect licences**: Ensure all content complies with its source licence
- **Give credit**: Acknowledge contributors and sources appropriately

## Change Log

### [2025-08-27] - Repository Restructure
- Created new directory structure for knowledge-share sessions
- Established clear content taxonomy and conventions
- Added comprehensive navigation and setup instructions
- Created template system for consistent content creation

---

## Quick Start for Contributors

1. **Read this index** to understand the repository structure
2. **Choose a template** from `_templates/` for your content type
3. **Create content** in the appropriate directory
4. **Update this index** with new section links
5. **Ensure all links resolve** and content is properly formatted

## Quality Gates

### Content Validation
- [ ] All internal links resolve correctly
- [ ] External links are traceable and accessible
- [ ] Images are properly stored and referenced
- [ ] Data files have clear documentation
- [ ] Content follows UK English conventions
- [ ] Templates are used consistently

### Technical Requirements
- [ ] Markdown syntax is valid
- [ ] Compatible with static site generators (MkDocs, mdBook)
- [ ] No tool-specific lock-in
- [ ] Directory structure matches documented layout
- [ ] All required directories exist and are properly named

---

*This repository is designed to be a living document that grows with your knowledge and research. Keep it current, well-organised, and accessible to your peers.*
