# Research Note: Why Agent Performance Degrades Over Long Runs

Date: 2025-08-28  
Author: Codex CLI  
Status: Draft  
Tags: degradation, long-run, memory, retrieval, reflection, error-propagation

## Abstract

LLM-based agents often show a gradual performance decline as their
trajectories grow longer. This research note synthesizes known mechanisms
behind long-run degradation, drawing from published findings on long-context
behavior, memory management, trajectory-level error dynamics, and tool-use
feedback loops. Key drivers include: compounding errors and path dependence;
context drift and “lost in the middle” effects; noisy or poisoned memory
accumulation; instruction and goal drift during iterative re-writing;
overuse or mis-calibrated reflection; retrieval saturation and stale state;
and planner–executor decoherence. We connect these mechanisms to empirical
observations and prior work, and outline concrete mitigations: memory hygiene
and eviction policies, constraint pinning, periodic re-planning, bounded and
validated reflection, retrieval diversification, step budgets with early
stopping, and watchdogs to trigger resets. This note complements internal
experiments on failure modes and performance benchmarks and motivates a
rigorous, metric-driven approach to sustaining agent quality over extended
runs.

## Background

### Problem Statement
Why do autonomous LLM agents tend to perform worse—their outputs become less
accurate, efficient, or aligned—the longer they run within a single task
trajectory?

### Context
- Long-horizon tasks accumulate intermediate thoughts, tool outputs, and
  memory entries that shape subsequent decisions.
- Known model behaviors at long contexts (e.g., recency/primacy biases and
  “lost in the middle”) can distort retrieval and attention.
- Naive memory strategies (append-only, no quality control) amplify noise and
  propagate earlier mistakes.
- Reflection loops, while helpful in moderation, can overfit to incorrect
  rationales or inflate verbosity without adding information.

### Research Questions
1. What mechanisms make performance degrade as step count increases?
2. How do memory and retrieval policies influence degradation?
3. Which mitigations provide the best cost–benefit for long-running agents?

## Methods

### Approach
Synthesis of published research and internal observations; taxonomy of
mechanisms; mapping mitigations to failure modes.

### Data Sources
- Internal documents and experiments: failure-mode analyses and benchmarks.
- Public literature on long-context behavior, memory management, and agents.

### Analysis Methods
Categorize degradation mechanisms; align each with empirical phenomena and
candidate mitigations. Highlight links to existing repository docs/experiments.

### Limitations
- No new controlled experiments in this note; relies on prior studies and
  qualitative evidence.
- Model- and domain-specific factors may change prevalence of mechanisms.

## Results

### Key Findings
- Error accumulation and path dependence: Early mistakes seed later actions,
  especially when written into memory or plans.
- Context drift and long-context weaknesses: Relevant constraints fall out of
  focus (“lost in the middle”); recency/primacy bias skews attention.
- Memory noise and poisoning: Append-only memories accumulate stale or
  incorrect entries; naive retrieval surfaces misleading items.
- Instruction and goal drift: Iterative re-prompting/reflection subtly removes
  guardrails or mutates objectives.
- Reflection overuse/overfitting: Self-critique can reinforce wrong rationales
  or expand tokens without improving factuality.
- Retrieval saturation and stale state: As the state grows, top-k concentrates
  on generic cues; environment shifts invalidate cached knowledge.
- Planner–executor decoherence: Plans and working state diverge; execution no
  longer tracks the intended strategy.
- Tool feedback loops: Mis-calibrated tool use (e.g., searching, editing) can
  amplify minor errors into major drifts.

### Data Analysis
Empirically, long trajectories often show:
- Rising step counts with diminishing marginal gains (“overthinking”).
- Increased repetition and cyclic tool calls (looping patterns).
- Declining retrieval precision and hit-rate for truly relevant memories.
- Higher variance in outcomes as trajectories lengthen (more stochastic forks).

### Patterns and Trends
- U-shaped curves: light reflection helps early, heavy reflection harms late.
- Quality cliffs: once key constraints fall out of context, recovery is rare
  without a reset/replan.
- Memory debt: uncurated stores raise the chance of retrieving misleading items
  over time.

## Discussion

### Interpretation
Performance degradation stems from interaction effects between model limits
(attention allocation over long contexts), state growth (memory and scratchpad
inflation), and control policies (reflection, retrieval, and planning). The
agent’s internal loop amplifies small missteps unless checked by hygiene and
reset mechanisms.

### Implications
- Long-running success depends as much on state management as on raw model
  capability.
- Memory must be curated; retrieval must be selective and diversified.
- Reflection should be bounded and validated, not unconditionally amplified.

### Future Research
- Controlled ablations: vary memory policies, reflection budgets, and
  retrieval diversification to measure degradation slopes.
- Detect-and-reset policies: learn triggers for re-planning or hard resets.
- Planner–executor coherence checks: lightweight validators to realign state.

### Connections
- See `docs/30-experiments/failure-mode-analysis.md` for concrete failure
  patterns and `docs/30-experiments/performance-benchmarks.md` for trajectory
  metrics. Memory lifecycle strategies in
  `docs/20-research/memory-lifecycle-management.md` mitigate several risks.

## Mitigations

- Constraint pinning: keep immutable requirements and safety rules in a fixed,
  always-visible header; periodically restate them.
- Periodic re-planning: summarize progress into a compact plan; drop verbose
  scratchpad content; realign goals and subgoals.
- Memory hygiene: deduplicate, score confidence, quarantine low-confidence
  or self-generated facts; add eviction policies (TTL, recency+usefulness).
- Retrieval diversification: mix semantic, structured (graph), and recency
  signals; enforce diversity in top-k to avoid echoing generic cues.
- Bounded reflection: cap reflection turns; insert external or off-policy
  critique for claims verification; avoid self-justification spirals.
- Temperature and verbosity control: keep key decisions low-temperature;
  prevent runaway token growth in thoughts.
- Watchdogs and early stopping: detect loops, repeated tool calls, or falling
  confidence; trigger reset or ask for clarification.
- Planner–executor coherence: lightweight checkers to ensure steps follow the
  plan; auto-repair when deviations accumulate.

## References

### Academic Sources
- [Liu et al. (2023). Lost in the Middle: How Language Models Use Long
  Contexts. arXiv:2307.03172](https://arxiv.org/pdf/2307.03172).
- Shinn et al. (2023). Reflexion: Language Agents with Verbal Reinforcement
  Learning. arXiv:2303.11366.
- Shumailov et al. (2023). The Curse of Recursion: Training on Generated Data
  Makes Models Forget. arXiv:2305.17493. (a.k.a. self-consuming model collapse)
- Xiong et al. (2025). How Memory Management Impacts LLM Agents: Empirical
  Study of Experience-Following. arXiv:2505.16067.

### Technical Documentation
- Internal: `docs/20-research/memory-lifecycle-management.md`.
- Internal: `docs/30-experiments/failure-mode-analysis.md`.
- Internal: `docs/30-experiments/performance-benchmarks.md`.

### Related Research
- Li et al. (2025). Memory OS of AI Agent. arXiv:2506.06326.
- Wu (2025). Git-Context-Controller: Manage the Context of LLM-based Agents
  like Git. arXiv:2508.00031.

## Appendices

### Quick Diagnostic Checklist
- Are key constraints pinned and visible? If not, pin them.
- Is the agent repeating tool calls? Add loop detection and stop.
- Is memory curated? Run dedup/evict and quarantine dubious facts.
- Is reflection helping? Cap or switch to external validation.
- Has the plan drifted? Trigger replan with concise state summary.

---

## Metadata

- Research Area: External Context Management; Agent Control
- Difficulty Level: Intermediate
- Time Required: 10–15 minutes
- Prerequisites: Familiarity with LLM agent loops and retrieval
- Related Work: memory architectures; lifecycle management; failure analysis

## Change Log

- 2025-08-28: Initial creation

---

This research note follows the standard template for knowledge-share repository
content and connects to existing experiments and research docs in this repo.

