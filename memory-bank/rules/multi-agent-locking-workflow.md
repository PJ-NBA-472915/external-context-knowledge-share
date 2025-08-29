---
version: "1.0.0"
version_type: "patch"
last_updated: "2025-08-29 09:25"
change_log: "Initial version with multi-agent locking workflow and coordination guidelines"
dependencies: []
breaking_changes: false
author: "system"
checksum: "sha256:initial_checksum_placeholder"
description: Guidelines for autonomous agents to use the repo-local locking mechanism for concurrent work.
globs:
  - "**/*"
alwaysApply: true
---

# Multi-Agent Locking Workflow for Concurrent Development

To ensure safe and coordinated concurrent development, all autonomous agents **MUST** adhere to the following workflow when modifying the codebase. This system prevents conflicting edits and maintains an auditable record of work claims.

## Core Workflow

1.  **Check Registries:** Before initiating any work, always consult the `coordination/active_work_registry.json` to identify existing claims. Use `./tools/locking/lock-status` to get a human-readable overview or `./tools/locking/lock-status --json` for programmatic access.

2.  **Claim Work:** If your intended work (files, directories, or topics) is not currently claimed by another agent, you **MUST** acquire a lock using the `lock-claim` utility.
    *   **Command:** `./tools/locking/lock-claim --agent "YOUR_AGENT_ID" --paths "path/to/file.py,path/to/dir/" --topics "feature_name" --intent "Brief description of work"`
    *   If `lock-claim` reports a conflict, you **MUST NOT** proceed with the conflicting work. Re-evaluate your task, choose a non-conflicting scope, or coordinate with the agent holding the conflicting claim.

3.  **Renew Claim:** While actively working on a claimed scope, you **MUST** periodically renew your claim to prevent it from expiring and being reaped by other agents or automated processes. A good practice is to renew at least every half of the `lock_ttl_minutes` defined in `coordination/config.json`.
    *   **Command:** `./tools/locking/lock-renew --agent "YOUR_AGENT_ID" --claim-id "CLAIM_ID_FROM_CLAIM_COMMAND"`

4.  **Release Claim:** Upon successful completion of your work and after committing your changes, you **MUST** release your claim. This makes the resources available for other agents.
    *   **Command:** `./tools/locking/lock-release --agent "YOUR_AGENT_ID" --claim-id "CLAIM_ID_FROM_CLAIM_COMMAND"`

## Conflict Rules

-   **No Overlapping Claims:** An agent **MAY NOT** modify any file or path that is covered by an existing active claim. This includes:
    *   Exact file matches.
    *   Files or subdirectories within a claimed directory.
    *   Matching topic claims.
-   The `lock-claim` utility will automatically detect and prevent conflicting claims.

## Required Git Etiquette

-   **Commit Messages:** All commit messages for changes made under a claim **MUST** include the `claim_id` in the commit body. This links the changes to the authorization.
-   **Pre-commit Guard:** The `.git/hooks/pre-commit` hook (or an equivalent check in your workflow) **MUST** be active. It will prevent commits if modified files are not covered by your active, non-stale claims. Do not bypass this unless explicitly authorized for emergency fixes (`LOCK_BYPASS=1 git commit`).

## Further Details

For a comprehensive understanding of the locking mechanism, including configuration, recovery procedures, and detailed CLI usage, refer to the full documentation at `docs/multi-agent-locking.md`.
