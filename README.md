# AI Operations Engine

AI Operations Engine is an experimental platform designed to bring artificial intelligence into real-world infrastructure and business operations.

It combines deterministic automation, operational memory, and AI-assisted reasoning to reduce operational noise, improve decision-making, and progressively learn from validated solutions.

The system is designed to **prioritize safety, control, and auditability**, ensuring that automation evolves in a governed and predictable way and does not send raw errors directly to the LLM. It first retrieves relevant operational documentation and builds an enriched context before reasoning.

---

## Core Idea

Most operational problems should not be solved directly by AI.

Instead, the system follows a structured decision flow:

```text
Event
  ↓
Normalization
  ↓
Deterministic Rules (Reflexes)
  ↓
Operational Memory
  ↓
Decision Engine
  ↓
AI Reasoning (only if needed)
  ↓
Human Validation
  ↓
Learning & Rule Promotion
```
## Key Principles

- Deterministic rules should always be preferred over AI when possible  
- AI is used only when context interpretation is required  
- No automatic execution of risky actions  
- All learning must be validated before becoming automation  
- All automation must pass governance validation before becoming deterministic behavior  
- The system evolves through controlled feedback loops  

---

## Current Features

### 1. Event Normalization

Converts heterogeneous system events into a common operational format.

**Supported sources:**

- Prefect (flows)  
- Rundeck (jobs)  
- Onboarding workflows  

---

### 2. Deterministic Rule Engine

Implements high-confidence "reflexes" for known issues.

- YAML-based rule definitions  
- Priority-based evaluation  
- Safe recommendation actions  

---

### 3. Operational Memory

Stores previously resolved incidents.

- JSONL-based memory store  
- Similarity scoring system  
- Reuse of validated solutions  
- Success/failure tracking  

---

### 4. Decision Engine

Combines rules and memory to produce an operational decision.

**Outputs:**

- decision type  
- recommended action  
- confidence level  
- whether AI reasoning is required  

---

### 5. Reasoning Layer (Mock Implementation)

Provides AI-assisted analysis when deterministic logic is insufficient.

- Prompt-based reasoning design  
- Mock reasoning engine (no external LLM yet)  
- Designed for future integration with LLM providers (e.g., Gemini, OpenAI)  

---

### 6. Feedback Loop & Learning

Tracks whether applied solutions were successful.

- Updates memory success/failure counters  
- Enables learning from real-world outcomes  

---

### 7. Controlled Rule Promotion

Promotes frequently successful solutions into deterministic rules.

**Flow:**

```text
Memory → Repeated Success → Rule Candidate → Governance → Human Approval → Rule
```
## Rule Governance & Safety Controls

The system includes a governance layer to prevent uncontrolled growth of deterministic rules and unsafe automation.

Before any rule is promoted, it must pass a strict validation process.

### Governance Checks

- Duplicate rule detection: no repeated IDs
- Validation of rule structure and required fields
- Prevention of overly generic conditions, such as `"error"` or `"failure"`
- Limitation of rule complexity, including the number of conditions
- Detection of conflicts with existing rules
- Restriction of dangerous action types, such as `delete`, `execute` or `deploy`

### Safety Principles

- No rule is automatically promoted from AI or memory
- All rule candidates must pass governance validation
- Final approval always requires human validation
- Rules are designed to recommend actions, not execute them

### Why This Matters

Without governance, AI-assisted systems can quickly become unstable:

- Too many rules can create noisy matches
- Generic rules can trigger incorrect automation
- Conflicting rules can produce unpredictable behavior

This layer ensures that the system remains:

- predictable
- auditable
- safe for real-world operations

---

## 🔧 Learning Pipeline


```text
Operational Memory
  ↓
Repeated Success
  ↓
Rule Candidate
  ↓
Governance Validation
  ↓
Human Approval
  ↓
Deterministic Rule
```
---

## 🔧 Example Flows

### Known Issue (No AI Required)

```text
Prefect flow fails (401 Unauthorized)
  ↓
Event normalized
  ↓
Deterministic rule detects authentication issue
  ↓
Decision generated
  ↓
No AI reasoning required
```
### Unknown Issue (AI-Assisted)

Rundeck job fails (403 Forbidden)
  ↓
Event normalized
  ↓
No strong rule match
  ↓
Weak memory match
  ↓
AI reasoning triggered
  ↓
Suggested cause and action
  ↓
If repeated → candidate rule

---

## 🔧 Project Structure


```text
engine/
├── events/         # Event normalization
├── rules/          # Deterministic rule engine + governance
├── memory/         # Operational memory
├── orchestrator/   # Decision engine
├── reasoning/      # AI reasoning layer (mock)
├── feedback/       # Learning and promotion pipeline
```
## Current Limitations

- No real LLM integration yet (mock reasoning only)  
- No persistence beyond local files (JSONL/YAML)  
- No API layer  
- No UI for approvals or monitoring  
- No vector-based similarity search  

---

## Roadmap

- Integrate real LLM provider (Gemini / OpenAI)  
- Add vector-based memory search  
- Expose API (FastAPI)  
- Add workflow execution layer (Rundeck / Prefect integration)  
- Add observability and feedback scoring  
- Add UI for rule approval and governance  
- Add policy-based automation controls  

---

## Positioning

This project is not a simple AI demo.

It is an exploration of how to build **AI-assisted operational systems** where:

- automation is deterministic when possible  
- AI is used when necessary  
- learning is controlled and validated  
- governance ensures long-term stability  

---

## Status

Early-stage prototype with a complete functional architecture.

The AI layer is currently mocked but fully designed for future integration.