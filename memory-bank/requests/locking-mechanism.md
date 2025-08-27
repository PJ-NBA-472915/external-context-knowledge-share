You are an expert systems engineer and repo architect. Design and create a robust, repo-local locking mechanism that enables multiple autonomous agents to work concurrently on the SAME repository without stepping on each other’s work.

## Prior Art to Emulate
Model the coordination approach on the lock-based, file-claimed workflow described for the 'Claude Code Agent Farm' (lock files under a coordination directory, active work registry, completed work log, stale-lock handling, per-agent identity and heartbeats). Do not copy text verbatim; design an equivalent, repo-agnostic solution suitable for ANY agent framework (Claude Code, Gemini CLI, MCP agents, etc.). [Reference context only; reimplement cleanly.]

## High-Level Goals
- Allow N concurrent agents to claim work (files/paths/topics) via lock claims.
- Prevent conflicting edits and duplicated effort.
- Provide discoverable, auditable state so agents can coordinate without a server.
- Be simple to adopt: pure files + optional helper scripts; no external DB required.

## Deliverables (create these in the repo)
1) ./coordination/ directory structure:
   - ./coordination/active_work_registry.json          # current claims/status
   - ./coordination/completed_work_log.json            # append-only completion log
   - ./coordination/agent_locks/                       # one lock file per active claim
   - ./coordination/heartbeats/                        # per-agent heartbeat files
   - ./coordination/planned_work_queue.json            # optional queue of candidate tasks

2) CLI utilities (POSIX-friendly, no heavy deps) under ./tools/locking/:
   - lock-claim: claim one or more paths/topics with metadata (agent_id, reason, scope)
   - lock-release: release a claim atomically and update registries
   - lock-renew: refresh TTL to avoid stale-claim reaping
   - lock-status: pretty-print registries (who holds which locks; stale candidates)
   - lock-reap-stale: detect and clean up stale locks (configurable TTL)
   - lock-validate: preflight checks (writable, atomic fs ops available, git clean state)
   - Optional: lock-flock-wrapper: use flock(1) when available for extra safety

   Implementation constraints:
   - Write these in portable Bash with tiny helpers (awk/jq) OR Python with zero non-stdlib deps (argparse, json, pathlib).
   - All file writes must be atomic (write to temp + fsync + mv).
   - Use monotonic timestamps where possible; include agent_pid and host hints in metadata.

3) Agent integration docs:
   - ./docs/multi-agent-locking.md explaining:
     * How agents must: (a) check registries, (b) claim, (c) renew, (d) release
     * Conflict rules: no agent may modify a path while another holds an overlapping claim
     * Required git etiquette: small atomic commits, descriptive messages, lock scope in commit body, and pre-commit guard that fails if claims are missing or stale
     * Recovery: how to reap stale locks safely; manual override procedure

4) Git hooks (optional but recommended):
   - .git/hooks/pre-commit: refuse commit if modifying files outside agent’s current claims
   - .git/hooks/prepare-commit-msg: inject claim summary into commit template
   - All hooks should be idempotent and easy to bypass with an env var (e.g., LOCK_BYPASS=1)

5) Configuration file:
   - ./coordination/config.json with defaults:
     {
       \"lock_ttl_minutes\": 90,
       \"stale_grace_minutes\": 30,
       \"max_paths_per_claim\": 25,
       \"allow_topic_claims\": true,
       \"advisory_only\": false,
       \"use_flock_when_available\": true
     }

## Functional Requirements
- Unique agent identity: agent_<timestamp>_<4char>
- A claim records: agent_id, created_at, expires_at, paths/topics, intent/plan, related issue/PR, host, pid
- Overlap detection: two claims conflict if any path overlaps (exact file, or directory prefix)
- Stale detection: if now > expires_at + grace => eligible for reap (record reaper_id & reason)
- Crash safety: locks are never partially written; registries remain valid JSON
- Read concurrency: many agents can read registries concurrently
- Write serialisation: ensure single-writer semantics via atomic rename and (when available) flock(1)
- No global daemon required; shell-only usage MUST work

## Non-Functional Requirements
- Portable across macOS/Linux; Windows via WSL acceptable
- Minimal dependencies; document required tools
- Works offline; no network calls required
- Clear logs to stdout/stderr; exit codes meaningful for CI

## Acceptance Tests (implement as ./tools/locking/tests/*.sh or Python unittest)
- test_claim_and_release_single_file
- test_conflict_detection_overlap
- test_directory_scope_claims
- test_stale_reap_and_audit_trail
- test_concurrent_claims_no_corruption (spawn multiple background claimers)
- test_git_hooks_block_unclaimed_changes
- test_resume_after_crash (simulated kill between temp write and mv)

## Developer Experience
- One-liners:
  - ./tools/locking/lock-claim --agent \"AGENT_A\" --paths src/foo.py,src/bar.py --intent \"Refactor utils\"
  - ./tools/locking/lock-status --format table
  - ./tools/locking/lock-reap-stale
- Pretty printing for humans; JSON for machines (–-json flag)

## Security & Integrity
- Validate agent-provided fields; normalise paths; ban path traversal
- Deny claims that exceed configured scope/limits
- Document how to sign commits and relate claims to commits/PRs

## Documentation & Examples
- Provide ./docs/multi-agent-locking.md with step-by-step usage and failure modes
- Provide sample CI job that runs lock-validate and ensures all modified files were claimed

## Output Required
- Create all files, scripts, and documentation above with working code
- Add a short README section to the repo root explaining the locking subsystem
- Print a final checklist showing each deliverable created and where

Begin now. When choosing between Bash and Python, prefer Python if jq isn’t guaranteed. Keep UK English in docs.
