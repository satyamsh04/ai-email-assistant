# System Architecture

## Overview

The AI Email Assistant uses a multi-agent architecture built on the OpenClaw framework. Each agent is a specialised unit with a defined role, tool access, and output schema.

## Agent Roles

### 1. Orchestrator Agent
- Receives raw incoming email
- Determines pipeline routing (which sub-agents to invoke and in what order)
- Aggregates outputs from sub-agents into a final structured result

### 2. Classifier Agent
- Input: Raw email text
- Task: Classify email by intent (e.g. inquiry, complaint, booking, support), urgency (high/medium/low), and topic category
- Output: Structured classification object (JSON)

### 3. Context Retrieval Agent
- Input: Classification + email metadata
- Task: Query relevant history, FAQs, or knowledge base to gather context for response
- Tools: Knowledge base lookup, email history retrieval
- Output: Context summary relevant to this email thread

### 4. Response Agent
- Input: Original email + classification + retrieved context
- Task: Draft a professional, contextually appropriate reply
- Prompt style: System prompt defines tone, formatting, and constraints
- Output: Draft email response (plain text or HTML)

## Data Flow

```
Email Input → Orchestrator → Classifier → Context Agent → Response Agent → Output
```

## Key Design Decisions

- **Modular agents**: Each agent is independently testable and swappable
- **Structured outputs**: All inter-agent communication uses typed JSON schemas
- **Prompt versioning**: Prompts are stored as templates with version tracking
- **Fallback handling**: If classification confidence is low, the system flags for human review
