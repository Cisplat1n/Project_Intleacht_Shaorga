# Project Intleacht Shaorga


## LLM-Assisted DataFrame Tidy Engine

> *Automatically reason about, validate, and improve tabular data using a Large Language Model.*

---

### Overview

This project is a **proof-of-concept** showcasing how a Large Language Model (LLM), accessed via an API key, can be used as an *intelligent data quality assistant*.

Instead of manually writing repetitive validation and cleaning logic, this tool:

* Accepts **structured instructions** and a **pandas DataFrame**
* Builds a prompt from a **predefined, constrained skeleton**
* Sends that prompt to an LLM via an API
* Receives **suggested transformations, justifications, and improvements**

The goal is not blind automation, but **transparent, explainable data tidying**.

---

### What It Does

Given a DataFrame, the system will:

1. **Inspect the data** for common structural and quality issues

   * Missing values (`NaN` / `None`)
   * Descriptive Statistics
   * Grab the column names
   * Use the data to make spoof data

2. **Generate suggested transformation code**

   * Pandas-native
   * Non-destructive by default
   * Human-readable and reviewable

3. **Explain its reasoning**

   * Why each check was performed
   * Why each transformation is suggested

4. **Recommend further improvements**

   * Optional additional cleaning steps
   * Potential downstream transformations
   * Data consistency or schema ideas

---

### Architecture (High-Level)

```
DataFrame
   ↓
Instruction Parser
   ↓
Prompt Skeleton (Predefined & Controlled)
   ↓
LLM API Call
   ↓
─────────────────────────────
│  Suggested Pandas Code     │
│  Justifications            │
│  Further Recommendations  │
─────────────────────────────
```

Key design goal: **the LLM reasons, but does not execute**.

---

### Design Principles

* **Clean-room friendly** — no proprietary logic embedded
* **Explainability first** — every suggestion is justified
* **LLM as an assistant, not an oracle**
* **Prompt constraints** to reduce hallucinations
* **Human-in-the-loop** by default

---

### Example Use Case

* Drop this into a data ingestion pipeline
* Use it to *audit* incoming datasets
* Generate cleaning code for review in PRs
* Bootstrap validation logic for new schemas
* Experiment with LLM-assisted data quality tooling

---

### Why This Exists

Data cleaning is:

* Repetitive
* Context-dependent
* Hard to generalise

This project explores whether LLMs can:

* Reduce boilerplate
* Surface *why* data checks matter
* Act as a reasoning layer on top of pandas

It is **not** intended to replace data engineers — only to make them faster and more informed.

---

### Disclaimer

* This is an **experimental project**
* Outputs should always be **reviewed before execution**
* Not intended for production use without safeguards

---

### Future Ideas

* Schema-aware validation
* Streamlit UI for interactive review
* Pluggable rule systems
* Test generation from LLM output
* Diff-based DataFrame transformations

---

### Status

Early-stage / exploratory

Contributions, critiques, and experiments welcome.

---

*Built to explore the intersection of LLMs, data quality, and explainable automation.*
