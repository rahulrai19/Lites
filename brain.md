# 🧠 Lites Project Brain & Context Knowledge Base

> **North Star**: Lites is an intelligent, high-performance LLM token optimization middleware and AI proxy. It intercepts API payloads to deterministically cut token waste, cache responses, intelligently compress conversation history, and dynamically route requests to the most cost-effective models without sacrificing intent or quality.

---

## 📌 Repository & Metadata

* **Repository:** `rahulrai19/Lites` (`main` branch)
* **Local Root:** `d:\Lites\Lites`
* **Original Archival Session ID:** `f7df70b0-4869-447e-8c1c-a4843da6cf02` (5,560 steps, Sept 2026)
* **Tech Stack:**
  * **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic V2, `pydantic-settings`
  * **Package Management:** `uv`
  * **Token Counting:** `tiktoken` (OpenAI cl100k_base / o200k_base)
  * **Caching:** In-memory LRU, Redis (Upstash compatible), FAISS Semantic Embedding Cache
  * **Telemetry & Metrics:** MongoDB (`motor`), Non-PII token savings tracker
  * **Frontend:** React 18, Vite, TypeScript, Tailwind CSS, Lucide icons (Redis-inspired dark aesthetic)
  * **SDKs:** Python (`lites-sdk` on PyPI) & TypeScript/Node.js (`lites-sdk` on NPM)

---

## 🏛️ Core Architectural Principles

1. **ROI-Guarded Optimization:** Never perform an optimization if the cost or latency overhead exceeds the expected token/dollar savings.
2. **Strict Intent Preservation:** The optimizer must prefer **NO-OP (no change)** over an optimization that risks altering negative constraints, conditionals, punctuation in code/JSON, or technical semantics.
3. **Bring Your Own Intelligence (BYOI):** Provider-agnostic abstraction layer supporting OpenAI, Google Gemini, Anthropic, or local open-weights engines.
4. **Zero-PII Telemetry:** Track savings percentages, provider latency, cache hits, and token deltas without persisting sensitive user prompt contents in metrics databases.

---

## ⚡ The 6 Pillars of Optimization

The Lites pipeline (`app/core/engine.py` -> `LitesCoreEngine`) evaluates incoming requests through six layered optimization strategies:

```
User / Client Request
       │
       ▼
[ 1. Cache Lookup ] ─────────► Exact Match (Redis) / Semantic Match (FAISS) ──► Instant Return (0 LLM Cost)
       │ (Cache Miss)
       ▼
[ 2. Context Management ] ───► Sliding-window truncation & relevant history retrieval
       │
       ▼
[ 3. Rule Optimization ] ────► Deterministic regex: whitespace trim, paragraph deduplication, safe filler stripping
       │
       ▼
[ 4. Decision Engine ] ──────► ROI Gatekeeper: Evaluates token length, expected savings vs. overhead
       │
       ├─► [ 5. AI Prompt Optimization ] (Optional: Secondary model prompt summarization)
       │
       ▼
[ 6. Adaptive Model Router ] ─► Evaluates complexity: Routes simple queries to cheap/fast models (e.g. Gemini Flash)
       │
       ▼
Target LLM Provider (OpenAI, Gemini, Anthropic)
       │
       ▼
Telemetry & Cache Write ─────► Record tokens saved, latency ms, cache entry
```

1. **Exact & Semantic Cache (`app/cache/`):**
   * Normalizes whitespace and casing before hashing to guarantee consistent hits.
   * Semantic caching embeds prompt text and searches vector similarity (cosine threshold ≥ 0.92).
2. **Context Compression (`app/models/context.py`):**
   * Compresses multi-turn conversation histories by pruning obsolete intermediate chatter while preserving system prompts and the latest turns.
3. **Deterministic Rule Optimizer (`app/optimizer/rules.py`):**
   * Multi-space collapse (preserving code/YAML indentation).
   * Multiple newline reduction (`\n{3,}` -> `\n\n`).
   * Paragraph and non-empty line deduplication.
   * Context-aware filler word removal (e.g., conversational "could you please kindly tell me" -> stripped, but "please the customer" -> preserved).
4. **Optimization Decision Engine (`app/optimizer/decision.py`):**
   * Evaluates thresholds (`min_tokens`, `max_tokens`, `ai_threshold`).
   * Reverts changes to original prompt if `tokens_saved <= 0`.
5. **AI Prompt Optimization (`app/optimizer/ai.py`):**
   * Invokes secondary fast LLMs to condense verbose instructions if prompt size justifies the secondary call cost.
6. **Adaptive Model Router (`app/optimizer/router.py`):**
   * Inspects complexity indicators (reasoning cues, code requirements, token density) and dynamically downgrades expensive models (e.g. GPT-4o) to cheaper equivalents (e.g. Gemini Flash) when quality will not be compromised.

---

## 📂 Codebase Directory Map

```
d:\Lites\Lites\
├── app/
│   ├── api/
│   │   ├── models.py           # Pydantic schemas for /v1/chat/completions & health
│   │   └── server.py           # FastAPI proxy endpoints & auth middleware
│   ├── cache/
│   │   ├── embedder.py         # Semantic vector embedding generator
│   │   ├── memory.py           # In-memory LRU and vector cache implementations
│   │   ├── models.py           # Cache entry schemas & hashes
│   │   ├── provider.py         # Redis & Upstash cache interfaces
│   │   └── redis_semantic.py   # Redis-backed semantic vector cache
│   ├── config/
│   │   └── env.py              # Pydantic-settings environment schema
│   ├── core/
│   │   ├── client.py           # Provider LLM client abstraction (OpenAI, Gemini)
│   │   ├── engine.py           # LitesCoreEngine orchestrating all 6 pillars
│   │   └── multiplexer.py      # Request streaming and proxy forwarding
│   ├── models/
│   │   ├── context.py          # Context sliding window models
│   │   └── optimization.py     # Optimization metadata & token metrics
│   ├── optimizer/
│   │   ├── ai.py               # AI prompt compression engine
│   │   ├── decision.py         # DecisionEngine ROI threshold logic
│   │   ├── router.py           # AdaptiveRouter (model tier downscaling)
│   │   └── rules.py            # Deterministic regex-based rule engine
│   ├── telemetry/
│   │   └── tracker.py          # TelemetryTracker pushing metrics to MongoDB
│   └── tokenizer/
│       └── openai.py           # Tiktoken-based token counting service
├── clients/
│   ├── node/                   # Node.js SDK (published to NPM as 'lites-sdk')
│   └── python/                 # Python SDK (published to PyPI as 'lites-sdk')
├── frontend/                   # React/Vite dashboard & interactive doc application
├── tests/
│   ├── integration/            # End-to-end and subsystem integration test suites
│   └── unit/                   # Unit tests for tokenizer, rules, cache, router, etc.
├── testing.md                  # Comprehensive 22-step testing roadmap logs
├── BACKLOG.md                  # V2 architectural ideas and deferred roadmap items
└── Dockerfile                  # Container definition for Lites proxy service
```

---

## 🧪 Testing Roadmap Summary (17 of 22 Completed)

Full audit logs reside in [`testing.md`](testing.md).

| Test | Objective | Status | Key Fix / Achievement |
|---|---|---|---|
| **TEST 01** | Project Foundation | **PASS** | Added missing `/health` route, resolved `pyproject.toml` wheel targets. |
| **TEST 02** | Tokenizer | **PASS** | Validated invariant properties (determinism, monotonicity, non-negativity). |
| **TEST 03** | Rule-Based Optimizer | **PASS** | Fixed indentation preservation for code/YAML, deduplication across blank lines. |
| **TEST 04** | Intent & Safety Preservation | **PASS** | Adversarial tests ensuring negative instructions ("Do not delete DB") are never inverted. |
| **TEST 05** | Optimization Metrics | **PASS** | Reversion safeguard: prompts reverting to original if `tokens_saved <= 0`. |
| **TEST 06** | Decision Engine | **PASS** | Integrated ROI cost guard: skips optimization if cost > savings. |
| **TEST 07** | Exact Cache | **PASS** | LRU eviction, expiration TTL, and thread-safe read/write verification. |
| **TEST 08** | Cache Normalization | **PASS** | Case-insensitive and whitespace-invariant prompt normalization before hashing. |
| **TEST 09** | Context Manager | **PASS** | Sliding-window pruning retaining latest system & user turns. |
| **TEST 10** | Provider Abstraction | **PASS** | Pluggable client layer with mock fallbacks for offline testing. |
| **TEST 11** | Full MVP Pipeline | **PASS** | End-to-end integration across all modules working harmoniously. |
| **TEST 12** | AI Prompt Optimizer | **PASS** | Dynamic prompt compression via secondary model with token length checks. |
| **TEST 13** | Semantic Cache | **PASS** | Vector similarity lookup bypassing identical LLM queries. |
| **TEST 14** | Adaptive Model Router | **PASS** | Classification heuristics routing trivial queries to cheaper models. |
| **TEST 15** | Metrics & Observability | **PASS** | Non-blocking background telemetry sync to MongoDB. |
| **TEST 16** | FastAPI API Layer | **PASS** | Full HTTP proxy testing against `/v1/chat/completions`. |
| **TEST 17** | SDK Validation | **PASS** | Python and Node.js SDK integration in both `mode="api"` and `mode="core"`. |
| **TEST 18-22** | CLI, Load & Security | *Pending* | Mapped for future production scaling and staging hardening. |

---

## 📦 SDK Distribution

Both SDKs are published as **`lites-sdk`**:

### 🐍 Python SDK (`lites-sdk`)
* **Registry:** [PyPI](https://pypi.org/project/lites-sdk/)
* **Dual Execution Modes:**
  * `mode="api"`: Lightweight HTTP proxy client (requires only `httpx` & `openai`).
  * `mode="core"`: Embedded engine directly running `LitesCoreEngine` in-process without network overhead.
* **Install:**
  ```bash
  pip install lites-sdk          # Proxy mode
  pip install lites-sdk[core]    # Embedded engine mode
  ```

### 🟢 Node.js SDK (`lites-sdk`)
* **Registry:** [NPM](https://www.npmjs.com/package/lites-sdk)
* **Design:** Drop-in extension of the official OpenAI TypeScript SDK. Automatically handles proxy routing and `X-Lites-Context` headers.
* **Install:**
  ```bash
  npm install lites-sdk
  ```

---

## 🛠️ Manual Operations & Development Guide

*(Following manual step-by-step instructions without automated bundle batch scripts)*

### 1. Backend Setup & Run
```powershell
# Navigate to project root
cd d:\Lites\Lites

# Sync virtual environment and dependencies using uv
uv sync

# Run FastAPI development server (with hot reload on port 8000)
uv run uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload
```
* Health check: `http://localhost:8000/health`
* Proxy endpoint: `http://localhost:8000/v1/chat/completions`

### 2. Running Test Suites
```powershell
# Run the entire test suite
uv run pytest

# Run unit tests only
uv run pytest tests/unit/ -v

# Run integration tests only
uv run pytest tests/integration/ -v
```

### 3. Frontend Dashboard Setup & Run
```powershell
# Navigate to frontend folder
cd d:\Lites\Lites\frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
* Dashboard will run at: `http://localhost:5173`

### 4. Docker Deployment
```powershell
# Build Docker image
docker build -t lites:latest .

# Run container with environment configuration
docker run -d --name lites-proxy -p 8000:8000 --env-file .env lites:latest
```

---

## 🔮 Active Backlog & Next Roadmap Items

Refer to [`BACKLOG.md`](BACKLOG.md) for full context:
1. **Upstash Vector Integration:** Horizontal scaling for semantic caching via `@upstash/vector` REST API (replacing in-process FAISS).
2. **Router Transparency Headers:** Inject `X-Lites-Routed-Model` and `X-Lites-Cost-Saved` headers into HTTP responses for frontend toast notifications.
3. **Prometheus Scraping Endpoint:** Expose a native `/metrics` endpoint to replace periodic MongoDB background writes in high-concurrency clusters.

