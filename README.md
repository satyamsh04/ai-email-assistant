# 🤖 AI Email Assistant

A **multi-agent AI Email Assistant** built using the **OpenClaw** agent framework and large language model APIs. Developed as a Work Integrated Learning (WIL) industry placement project at **Griffith University**.

The system automates email triage, classification, and intelligent response drafting through an orchestrated pipeline of specialised AI agents.

---

## ✨ Key Features

- **Automated Email Triage** — Classifies incoming emails by intent, urgency, and category using LLM inference
- **Multi-Agent Orchestration** — Separate agents handle classification, context retrieval, and response generation
- **LLM-Powered Drafting** — Generates contextually appropriate reply drafts based on email content and history
- **Tool Calling** — Agents invoke external tools and APIs to gather context before generating responses
- **Prompt Engineering** — Carefully crafted system prompts and few-shot examples to control agent behaviour
- **Modular Pipeline** — Each agent in the pipeline is independently configurable and replaceable

---

## 🏗️ Architecture

```
Incoming Email
      ↓
┌────────────────────────────────┐
│       Orchestrator Agent         │  (OpenClaw)
│  Coordinates the agent pipeline  │
└────────────────────────────────┘
      ↓               ↓              ↓
┌─────────┐  ┌─────────┐  ┌─────────┐
│Classifier│  │ Context │  │Response │
│  Agent   │  │Retrieval│  │  Agent  │
│          │  │  Agent  │  │         │
└─────────┘  └─────────┘  └─────────┘
      ↓               ↓              ↓
  Category &      Context &       Draft Email
   Priority       History          Response
      ↓               ↓              ↓
┌────────────────────────────────┐
│       Output: Structured email          │
│  triage report + suggested response     │
└────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | OpenClaw |
| LLM Integration | Large Language Model APIs (OpenAI-compatible) |
| Language | Python 3.10+ |
| API Layer | REST API / FastAPI |
| Prompt Engineering | System prompts, few-shot examples, chain-of-thought |
| Dev Tools | VS Code, Cursor IDE, GitHub Copilot, Claude Code |

---

## 📁 Repository Structure

```
ai-email-assistant/
├── agents/                  # Individual agent definitions
│   ├── classifier_agent.py  # Email classification agent
│   ├── context_agent.py     # Context retrieval agent
│   └── response_agent.py    # Response drafting agent
├── orchestrator/            # Main pipeline orchestrator
├── prompts/                 # System prompt templates
├── tools/                   # External tool integrations
├── api/                     # FastAPI endpoint layer
├── tests/                   # Unit and integration tests
├── docs/                    # Architecture diagrams
└── README.md
```

> ⚠️ **Note:** Source code is not publicly available as this was an industry-partnered WIL placement project. This repository documents the architecture, design decisions, and technical approach.

---

## 📚 What I Built & Learned

- **End-to-end agent pipeline design** — from initial prompt design through to deployed output
- **OpenClaw agent framework** — building, configuring, and chaining specialised agents
- **LLM prompt engineering** — system prompts, few-shot examples, and structured output formatting
- **Tool calling patterns** — giving agents the ability to invoke external APIs and data sources
- **Production deployment** — delivering a working system as part of an industry placement
- **Technical communication** — presenting AI system architecture to non-technical stakeholders

---

## 🎯 Outcomes

- Successfully delivered a working AI assistant as part of a WIL industry placement at Griffith University
- Reduced manual email review overhead through intelligent classification and automated draft generation
- Designed and presented the system architecture to academic and industry supervisors

---

*Work Integrated Learning (WIL) Project — Griffith University, 2026*
*Satyam Sharma — [github.com/satyamsh04](https://github.com/satyamsh04)*
