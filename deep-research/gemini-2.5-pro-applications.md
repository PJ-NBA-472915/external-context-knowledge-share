
AI Code Context: From Theory to Application

The theoretical frameworks that underpin memory-augmented AI agents are not merely academic exercises; they are being actively implemented in a growing ecosystem of research projects, open-source tools, and commercial platforms. These applications provide tangible evidence of how advanced memory architectures, retrieval strategies, and lifecycle management techniques are being used to build more capable and context-aware AI development partners. This document provides concrete examples of these approaches in action.

Memory Architectures in Practice

Different tasks require different ways of thinking and remembering. The same is true for AI agents. The abstract architectural metaphors discussed previously have given rise to distinct, practical implementations, each tailored for specific use cases, from long-term conversational agents to complex, goal-oriented software engineering.

Hierarchical (OS-Inspired) Systems: MemoryOS

The operating system-inspired hierarchical memory model is best exemplified by MemoryOS, an open-source framework from researchers at Beijing University of Posts and Telecommunications and Tencent AI Lab.1 Its implementation directly mirrors the theoretical model:
Short-Term Memory (STM): Functions as a conversational cache, using a First-In-First-Out (FIFO) policy to manage recent exchanges.1
Mid-Term Memory (MTM): Consolidates recurring topics from the STM into summaries.1
Long-Term Personal Memory (LPM): Stores persistent user and agent personas.1
A key practical feature is its heat-based replacement policy. Information in the mid-term memory is assigned a "heat" score based on recency and frequency of access. "Hot" information is promoted to long-term storage, while "cold" information is pruned, mimicking human-like prioritization.3 This isn't just theoretical; when tested on the
LoCoMo benchmark for long-term dialogue, MemoryOS improved the F1 score of the underlying model by 49.11% while reducing token consumption and API calls, demonstrating its real-world efficiency.1

Version Control Systems: The Git-Context-Controller (GCC)

For structured, long-horizon tasks like software development, the version control metaphor has been implemented in the Git-Context-Controller (GCC) framework.4 This system treats an agent's memory as a versioned file system, creating a
.GCC/ directory in the project workspace.6
The agent interacts with this memory using explicit, Git-like commands 7:
COMMIT: Creates a checkpoint to save a meaningful milestone.
BRANCH: Creates an isolated workspace to explore an alternative solution without affecting the main line of reasoning.
MERGE: Integrates a completed branch back into the main context.
This structured approach provides exceptional traceability and control. In practice, agents equipped with GCC have achieved a 48.00% resolution rate on the SWE-Bench-Lite benchmark for software bug fixing, outperforming other systems by providing a robust way to manage complex, multi-step reasoning.5 A simpler, manual version of this approach is also used by developers who create a
project-context.md file to provide a "single source of truth" for AI assistants like GitHub Copilot, defining the project's architecture, tech stack, and development practices.8

Graph-Based Systems: LocAgent and GraphRAG

Graph-based memory excels at representing the complex web of relationships within a codebase. A prime example is the LocAgent framework, which is designed for code localization (i.e., finding the right place to make a change).9
LocAgent works by:
Parsing the Codebase: It constructs a directed graph where nodes represent entities like files, classes, and functions, and edges represent their relationships, such as imports, invokes, and inherits.9
Providing Agent Tools: The agent is given tools to navigate this graph, including:
SearchEntity: To find initial code entities based on keywords.
TraverseGraph: To explore the relationships of an entity (e.g., find all functions that call it) in a multi-hop fashion.10
RetrieveEntity: To get the full code content of a specific entity.9
This allows the agent to trace dependencies and build a comprehensive understanding of the code's structure, mirroring a human developer's investigative process.11 This approach is part of a broader trend known as
GraphRAG, where developers use tools like Neo4j or FalkorDB to build knowledge graphs from various data sources (including code) and then use a hybrid of vector search and graph traversal to provide rich, relational context to an LLM.12

Code-Aware Retrieval and Context Engineering in Practice

Providing high-quality context is more of an engineering discipline than an art. The industry is moving away from simple prompt tweaking toward a more systematic approach of "context engineering," which involves building robust data pipelines to feed the AI agent the right information at the right time.15

AST-Aware Chunking: The cAST Method

A key challenge in preparing a codebase for retrieval is "chunking"—breaking the code into smaller pieces. Traditional methods that split by line or character count often break syntactic units, destroying context.17
The cAST (chunking via Abstract Syntax Trees) method is a practical solution to this problem.18 It works by:
Parsing Code: Using a language-agnostic parser like tree-sitter, it converts source code into an AST, a hierarchical tree that represents the code's syntactic structure.18
Applying a "Split-then-Merge" Algorithm: It traverses the tree, trying to fit entire syntactic nodes (like a whole function or class) into a single chunk. If a node is too large, it's recursively split. To avoid creating too many tiny chunks, adjacent small nodes are then merged.18
This structure-aware approach has a measurable impact. On the SWE-bench code generation benchmark, using cAST improved the Pass@1 rate by 2.67 points, and on the RepoEval retrieval benchmark, it boosted Recall@5 by 4.3 points.20

Context Engineering: The Dual-Context Approach

A powerful example of context engineering in practice is the dual-context approach for AI coding assistants.8 Instead of relying on the AI to infer everything from the code, developers provide two explicit context files:
project-context.md: A Markdown file that acts as a project blueprint, detailing the overall architecture, tech stack (e.g., Java, Spring Boot, AWS), folder structure, and development practices (e.g., API design, security protocols).8
Role-Based System Prompt: A separate file (e.g., software-engineer.md) that defines the "persona" for the AI. It specifies the user's role (e.g., "Senior Software Engineer"), coding style preferences (e.g., kebab-case for routes), and constraints (e.g., only use approved libraries like Spring Security).8
By feeding both documents to an agent like the GitHub Copilot Agent, developers can significantly reduce context misalignment and iterative overhead, ensuring the generated code aligns with professional standards from the start.8

Memory Lifecycle Management in Practice

For an agent to learn and adapt, its memory must be dynamic. Practical implementations of memory lifecycle management focus on consolidating knowledge and strategically forgetting outdated information.

Workflow Induction: Agent Workflow Memory (AWM)

Instead of just remembering facts, agents can learn processes. The Agent Workflow Memory (AWM) framework is a method that allows an agent to learn reusable routines, or "workflows," from its past experiences.22
The AWM process involves:
Analyzing Successful Trajectories: The system observes the sequence of actions an agent takes to successfully complete a task (e.g., booking a flight online).22
Inducing a Workflow: It extracts a generalized "task recipe" from these successful examples, summarizing the key steps and decisions.22
Storing the Workflow: This abstracted workflow is stored in the agent's memory.
When the agent encounters a similar task in the future, it can retrieve and follow this learned workflow, guiding its actions. This technique has proven highly effective, improving the success rate of agents on the WebArena web navigation benchmark by 51.1%.22

Selective Forgetting and Machine Unlearning

Forgetting is a feature, not a bug. In practice, strategic forgetting is crucial for an agent's adaptability and for legal compliance with regulations like GDPR's "right to be forgotten".23 Implementations of this concept include:
Soft Forgetting: Instead of abruptly deleting information, its relevance is gradually phased out over time.24
Contextual Forgetting: Information is forgotten in one context where it is no longer relevant but retained in others where it might still be useful.24
On a more technical level, the field of Machine Unlearning is developing methods to remove specific data from a trained model without the need for complete retraining.25 One such method is
SEUL, which enables selective, fine-grained unlearning for language models by focusing on removing specific spans of text rather than entire data instances. This is critical for scenarios where a user requests their personal data to be deleted from an AI system.26

Industry Adoption and Tooling Examples

The concepts of agent memory and context management are rapidly moving from research to production, enabled by standardized protocols and a new generation of infrastructure platforms.

Production-Ready Memory Platforms

Building a stateful AI agent from scratch is complex, but several platforms now provide the necessary infrastructure. A leading example is the MongoDB Store for LangGraph, LangChain's framework for building stateful, multi-actor applications.27 This integration provides a scalable backend for an agent's long-term memory, with explicit support for different memory types 27:
Episodic Memory: For conversation history.
Procedural Memory: For learned instructions or workflows.
Semantic Memory: For factual knowledge, often implemented with RAG.
In addition to general frameworks, specialized memory-as-a-service platforms like Mem0, Zep, and Cognee are emerging to provide a dedicated, persistent memory layer for AI agents.28

The MCP Ecosystem and Local-First Memory

The Model Context Protocol (MCP), an open standard introduced by Anthropic, has been a major catalyst for interoperability.29 It acts as a universal language for AI agents to communicate with tools and data sources.
A powerful application built on this standard is OpenMemory MCP, an open-source, local-first memory server.30 It runs entirely on a user's local machine, typically using Docker with
Qdrant for vector search and PostgreSQL for structured storage.31 This "local-first by default" design addresses major privacy concerns by ensuring no proprietary code or sensitive data is sent to the cloud.30
A user can connect any MCP-compatible tool to their local OpenMemory server. This creates a shared, private context layer across their entire workflow. The ecosystem of MCP-compatible clients is growing rapidly and includes major developer tools like:
Cursor 32
Zed 32
VS Code (via GitHub Copilot) 32
JetBrains AI Assistant 32
Claude Desktop App 32
This allows for powerful cross-tool workflows. For example, a developer can define project requirements in a conversation with the Claude Desktop app, and that context will be automatically available when they start generating code in Cursor, all without the data ever leaving their machine.30
Works cited
Memory OS of AI Agent - alphaXiv, accessed on August 26, 2025, https://www.alphaxiv.org/overview/2506.06326v1
MemoryOS is designed to provide a memory operating system for personalized AI agents. - GitHub, accessed on August 26, 2025, https://github.com/BAI-LAB/MemoryOS
Open-source "MemoryOS" - a memory OS for AI agents : r/LLMDevs - Reddit, accessed on August 26, 2025, https://www.reddit.com/r/LLMDevs/comments/1luo81v/opensource_memoryos_a_memory_os_for_ai_agents/
arxiv.org, accessed on August 26, 2025, https://arxiv.org/html/2508.00031v1
[2508.00031] Git Context Controller: Manage the Context of LLM-based Agents like Git - arXiv, accessed on August 26, 2025, https://arxiv.org/abs/2508.00031
Git Context Controller: Manage the Context of LLM-based Agents ..., accessed on August 26, 2025, https://arxiv.org/pdf/2508.00031
Git-Context-Controller (GCC) - Emergent Mind, accessed on August 26, 2025, https://www.emergentmind.com/topics/git-context-controller-gcc
Supercharging AI Coding Agents with Dual-Context Approach | by Sajesh Nair - Medium, accessed on August 26, 2025, https://medium.com/@sajesh/supercharging-ai-coding-agents-with-dual-context-approach-e7f8f51f93c0
LocAgent: Graph-Guided LLM Agents for Code Localization, accessed on August 26, 2025, https://arxiv.org/pdf/2503.09089
LocAgent: Graph-Guided LLM Agents for Code Localization - arXiv, accessed on August 26, 2025, https://arxiv.org/html/2503.09089v1
Tool-integrated Reinforcement Learning for Repo Deep Search - arXiv, accessed on August 26, 2025, https://arxiv.org/pdf/2508.03012
GraphRAG is fixing a real problem with AI agents : r/AI_Agents - Reddit, accessed on August 26, 2025, https://www.reddit.com/r/AI_Agents/comments/1m4rmlz/graphrag_is_fixing_a_real_problem_with_ai_agents/
Data Retrieval & GraphRAG for Smarter AI Agents - FalkorDB, accessed on August 26, 2025, https://www.falkordb.com/news-updates/data-retrieval-graphrag-ai-agents/
Building AI Agents with Knowledge Graphs vs. Retrieval Augmented Generation - Medium, accessed on August 26, 2025, https://medium.com/@senpubali7/building-ai-agents-with-knowledge-graphs-vs-retrieval-augmented-generation-a2730ec1915a
Context Engineering: Bringing Engineering Discipline to Prompts—Part 3 - O'Reilly Media, accessed on August 26, 2025, https://www.oreilly.com/radar/context-engineering-bringing-engineering-discipline-to-prompts-part-3/
Context Engineering is the New Vibe Coding (Learn this Now) - YouTube, accessed on August 26, 2025, https://www.youtube.com/watch?v=Egeuql3Lrzg
AST Enables Code RAG Models to Overcome Traditional Chunking Limitations - Medium, accessed on August 26, 2025, https://medium.com/@jouryjc0409/ast-enables-code-rag-models-to-overcome-traditional-chunking-limitations-b0bc1e61bdab
cAST: Enhancing Code Retrieval-Augmented Generation with Structural Chunking via Abstract Syntax Tree - arXiv, accessed on August 26, 2025, https://arxiv.org/html/2506.15655v1
Enhancing LLM Code Generation with RAG and AST-Based Chunking | by VXRL | Medium, accessed on August 26, 2025, https://vxrl.medium.com/enhancing-llm-code-generation-with-rag-and-ast-based-chunking-5b81902ae9fc
cAST: Enhancing Code Retrieval-Augmented Generation ... - arXiv, accessed on August 26, 2025, https://arxiv.org/pdf/2506.15655
[2506.15655] cAST: Enhancing Code Retrieval-Augmented Generation with Structural Chunking via Abstract Syntax Tree - arXiv, accessed on August 26, 2025, https://arxiv.org/abs/2506.15655
ICML Poster Agent Workflow Memory - ICML 2025, accessed on August 26, 2025, https://icml.cc/virtual/2025/poster/45496
Forgetting” in Machine Learning and Beyond: A Survey - arXiv, accessed on August 26, 2025, https://arxiv.org/html/2405.20620v1
Embracing Selective Forgetting: A New Frontier in Machine Learning - Indika AI, accessed on August 26, 2025, https://www.indikaai.com/blog/embracing-selective-forgetting-a-new-frontier-in-machine-learning
Training AI to Forget: The Next Frontier in Trustworthy AI | by Jerry Cuomo | Medium, accessed on August 26, 2025, https://medium.com/@JerryCuomo/training-ai-to-forget-the-next-frontier-in-trustworthy-ai-1088ada924de
Selective Forgetting: Advancing Machine Unlearning Techniques and Evaluation in Language Models, accessed on August 26, 2025, https://ojs.aaai.org/index.php/AAAI/article/view/32068/34223
Powering Long-Term Memory for Agents With LangGraph and ..., accessed on August 26, 2025, https://www.mongodb.com/company/blog/product-release-announcements/powering-long-term-memory-for-agents-langgraph
MIRIX: Multi-Agent Memory System for LLM-Based Agents - arXiv, accessed on August 26, 2025, https://arxiv.org/html/2507.07957v1
en.wikipedia.org, accessed on August 26, 2025, https://en.wikipedia.org/wiki/Model_Context_Protocol
Introducing OpenMemory MCP - Mem0 - The Memory Layer for your ..., accessed on August 26, 2025, https://mem0.ai/blog/introducing-openmemory-mcp
How to make your clients more context-aware with OpenMemory MCP - DEV Community, accessed on August 26, 2025, https://dev.to/anmolbaranwal/how-to-make-your-clients-more-context-aware-with-openmemory-mcp-4h71
Example Clients - Model Context Protocol, accessed on August 26, 2025, https://modelcontextprotocol.io/clients
