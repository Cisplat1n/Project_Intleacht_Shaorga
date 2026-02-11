# Project Intleacht Shaorga


## LLM-Assisted DataFrame Tidy Engine

> *Automatically reason about, validate, and improve tabular data using a Large Language Model.*

---

### Overview

This project is a **proof-of-concept** showcasing how a Large Language Model (LLM), accessed via an API key, can be used as an *intelligent data quality assistant*.

Instead of manually writing repetitive validation and cleaning logic, this tool:

* Accepts structured instructions and a statistics about a pandas dataframe
* Builds a prompt from a predefined, constrained skeleton (which also has a helper_reg for additional constraints)
* Sends that prompt to an LLM (GLM-4.7) via an API (Cerebras Inference)
* Receives suggested transformations and reasonings/justifications
* Then also enables the user to send the stats and suggested transformations back to the LLM for additional suggestions

The goal is not blind automation, but **transparent, explainable data tidying**.

---

### What It Does

Given a DataFrame, the system will:

1. **Inspect the data** for common quality issues

   * Dataset shape and dimensionality
   * Column names and data types
   * Missing value patterns
   * Descriptive metastatistics and distributions
   * Structural and format characteristics (e.g. ranges, delimiters, embedded newlines)

2. **Generate suggested transformation code**

   * Pandas-native
   * Non-destructive by default
   * Human-readable and reviewable
   * Use additional constraints from the helper_reg.txt for added guidance

3. **Explain its reasoning**

   * Why each check was performed
   * Why each transformation is suggested

4. **Recommend further improvements**

   * Optional additional cleaning steps
   * Potential downstream transformations
   * Data consistency or schema ideas

---

### Privacy Model

This system **does NOT send raw data values** to the LLM.

It does send **COLUMN NAMES**, a future feature will be added to restrict this behaviour!

Instead, it extracts and transmits descriptive metadata **only**, such as:

* Dataset shape and schema
* Column-level data types
* Missingness patterns
* Statistical summaries (e.g. counts, ranges, distributions)
* Structural and format signals (without exposing content)

No actual cell values, identifiers, or sensitive strings are included in the prompt.

This design ensures that the LLM can reason about structure and quality without ever seeing real data.

---

### Architecture (High-Level)

```
DataFrame
   ↓
Metadata extracted
   ↓
Prompt Skeleton populated(Predefined & Controlled)
   ↓
LLM API Call
   ↓
─────────────────────────────
│  Suggested Pandas Code     │
│  Justifications            │
│  Further Recommendations  │
─────────────────────────────
```

Key design goal: **Flexible, data agnostic, LLM reasoning, but does not execute and with transparency**.

---

### Design Principles

* **Clean-room friendly** — no proprietary logic embedded
* **Explainability first** — every suggestion is justified
* **LLM is meant to act as assistant, not an oracle**
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
* Outputs should **always** be reviewed before execution
* Not intended for production use without safeguards

---

### Future Ideas

* Schema-aware validation
* Streamlit UI for interactive review
* Pluggable rule systems -> expansion on the helper registry
* Test generation from LLM output


---

### Status

Approaching end status!

Contributions, critiques, and experiments welcome.

---

