<!--
Sync Impact Report:
- Version change: N/A -> 1.0.0
- List of modified principles:
    - [PRINCIPLE_1_NAME] -> Digital FTE First
    - [PRINCIPLE_2_NAME] -> Strict Session Security
    - [PRINCIPLE_3_NAME] -> Professional Agency
    - [PRINCIPLE_4_NAME] -> High-Accuracy Task Extraction
    - [PRINCIPLE_5_NAME] -> SDD Discipline (Spec-Driven Development)
    - [PRINCIPLE_6_NAME] -> Independent Value (MVP)
- Added sections: Development Standards
- Removed sections: None
- Templates requiring updates:
    - .specify/templates/plan-template.md (✅ updated - reviewed for alignment)
    - .specify/templates/spec-template.md (✅ updated - reviewed for alignment)
    - .specify/templates/tasks-template.md (✅ updated - reviewed for alignment)
- Follow-up TODOs: None
-->

# THE-AI-AGENT-FACTORY Constitution

## Core Principles

### I. Digital FTE First
Agents are designed as functional Digital Full-Time Employees (FTEs). They MUST be capable of executing complex, end-to-end workflows with minimal supervision, demonstrating high autonomy and goal-alignment.

### II. Strict Session Security
Security for platform sessions (e.g., WhatsApp, Telegram) is non-negotiable. Authentication tokens, session states, and private keys MUST be handled with extreme care, never logged in plaintext, and persisted only via secure, encrypted storage.

### III. Professional Agency
Every agent MUST maintain a professional persona. Interactions must be goal-oriented, courteous, and aligned with the organization's brand and ethical guidelines. Ambiguity in user intent SHOULD be resolved through professional clarification rather than assumption.

### IV. High-Accuracy Task Extraction
Precision in extracting tasks and intents from unstructured inputs is a primary success metric. The system MUST prioritize high-confidence extractions; when confidence is low, the agent MUST flag the ambiguity or seek clarification rather than proceeding with potentially incorrect tasks.

### V. SDD Discipline (Spec-Driven Development)
The "Spec-Plan-Tasks-Implement" lifecycle is mandatory. No implementation work should begin without a reviewed specification and a detailed task list. This ensures traceability and architectural integrity.

### VI. Independent Value (MVP)
Features MUST be broken down into independent user stories. Each story MUST deliver a standalone slice of value and be independently testable. This enables incremental delivery and rapid feedback loops.

## Development Standards

### Technology Stack & Security
- **Security**: Zero-trust approach to session management. Use environment variables for all secrets.
- **Accuracy**: Implement validation layers for NLP/extraction tasks.
- **Testing**: TDD is mandatory for logic-heavy components and task extraction engines.

## Governance

### Amendment Procedure
1. Propose changes via an ADR or a constitution amendment request.
2. Review impact on existing templates and workflow commands.
3. Update versioning and propagate changes.

### Versioning Policy
- **MAJOR**: Backward incompatible governance/principle removals or redefinitions.
- **MINOR**: New principle/section added or materially expanded guidance.
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements.

**Version**: 1.0.0 | **Ratified**: 2026-05-05 | **Last Amended**: 2026-05-05
