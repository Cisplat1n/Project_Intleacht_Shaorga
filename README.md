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

# How to Use: LLM Data Cleaning Pipeline

## Quick Start (5 minutes)

### Prerequisites
- Python 3.8+ with pandas, numpy installed, use requirements.txt for full 
- Access to LLM API (OpenAI, Anthropic, or compatible)
- Your dataset in CSV format

### Basic Setup

1. **Clone or Download**


2. **Place Your Data**
   ```
   data_test/
   └── your_dataset.csv  # Put your CSV file here
   ```

3. **Configure LLM Settings**
   - Open `llm-notebook.ipynb`
   - Update API credentials in cell 1
   - Set model parameters (temperature, max_tokens)

4. **Run the Pipeline**
   - Execute cells sequentially from top to bottom
   - Review outputs after each cell
   - Generated code appears in `func_test_suite.txt`

---

## Detailed Workflow

### Phase 1: Data Profiling (Automatic)

**What happens:**
1. Pipeline loads your CSV from `data_test/`
2. Runs `df_checker()` to analyse data quality
3. Generates statistics without exposing sensitive data
4. Saves profile to `stats/` folder

**Output:**
- `stats/stats.txt` - Full analysis
- Detects: missing values, format issues, embedded data

**Review checkpoint:** Check console for detected issues

---

### Phase 2: Helper Registry Configuration (Optional)

**File:** `helper_reg.txt`

This file guides the LLM toward your specific needs. It's **optional but powerful**.

#### When to Use Helper Registry

| Use Case | Add to helper_reg.txt |
|----------|----------------------|
| **Specific output format** | "Store salaries in thousands (137 not 137000)" |
| **Feature engineering** | "Extract state from Location column" |
| **Reference values** | "Use 2026 as reference year for age calculations" |
| **Skill extraction** | "Extract skills: python, sql, excel, aws, spark" |
| **Privacy requirements** | "Do not create columns with PII" |
| **Constraints** | "Do not drop any columns" |

#### Example Helper Registry

```plaintext
# Reference Values
reference_year: 2026
currency: USD

# Data Standards  
salary_format: Store in thousands for readability (137 not 137000)
date_format: Convert to age/duration metrics

# Feature Engineering
location_parsing: Extract state abbreviation from "City, State" format
seniority_extraction: Extract from Job Title (Senior/Mid/Junior)
skill_keywords: python, sql, r, excel, tableau, aws, spark, hadoop

# Constraints
do_not_drop: Keep all original columns
privacy_level: Do not expose PII in outputs
```

**Pro tip:** Start without helper registry, then add guidance based on first run results.

---

### Phase 3: Generate Cleaning Code (Automatic)

**What happens:**
1. LLM analyses statistics + helper registry
2. Generates transformation functions
3. Writes code to `llm_cleaning/llm_output.txt`
4. Writes reasoning to internal reasoning section

**Output files:**
```
llm_output.txt
```

**Review checkpoint:** Read generated functions before running

---


### Phase 4: Request Enhancement Suggestions (Optional)

**When:** After code has been generated and reviewed 

**How:**
1. Send the suggested code + stats back into the LLM
2. LLM automatically enters "suggestion mode"
3. Receives suggestions in `llm_suggestions/llm_suggestions.txt`

**What you get:**
- Feature engineering ideas
- Encoding strategies
- Derived metrics
- Imputation approaches

**Output:**
```
===== SUGGESTIONS =====
1. Create Skill Synergy Features
   - What: Binary indicators for skill pairs (python_and_sql)
   - Why: Jobs requiring combinations pay premium
   - Risk: May create sparse features
...
```

---


## Best Practices

### IMPORTANT: Clean Between Runs

**Before each new dataset:**

```bash
# Clear generated outputs
rm -rf stats/*
rm -rf final_prompt/*
rm -rf llm_cleaning/*
rm -rf temp/*
rm -rf llm_suggestions/*

**Why:** Old outputs can confuse the LLM or cause append conflicts.

---

### Optimisation Tips

#### 1. Start Simple
```
First run:  No helper_reg, just let LLM detect issues
Second run: Add guidance based on what was missed
Third run:  Request enhancements
```

#### 2. Iterative Refinement
- Don't expect perfection first try
- Review → Refine helper_reg → Re-run
- Each iteration improves results

#### 3. Validate Everything
```python
# After each transformation
print(f"Before: {df.shape}")
print(f"After:  {df_cleaned.shape}")
print(f"Changed: {df.compare(df_cleaned)}")
```

#### 4. Use Helper Registry Strategically

**Good guidance:**
```
reference_year: 2026
salary_format: thousands
```

**Too vague:**
```
make it better
clean the data
```

**Too specific (constrains LLM):**
```
create exactly 47 functions
use only these exact column names: [long list]
```

---

## Advanced Usage

### Custom Profiling

Edit `df_checker.py` to add domain-specific checks:
```python
# Add custom format detection
"has_json_format": col_data.str.contains(r'\{.*\}', na=False).sum()
```



## FAQ

**Q: Can I use this on non-CSV data?**  
A: Modify `llm-notebook.ipynb` to load other formats (Excel, JSON, SQL). The profiler works with any pandas DataFrame.

**Q: How do I know if suggestions are good?**  
A: Check if they:
- Reference actual columns in your data
- Explain analytical value clearly
- Note risks/assumptions
- Build on completed transformations
- Always ensure you know what each function does before performing in on your data!

**Q: Can I edit generated functions?**  
A: Yes! They're just Python functions. Copy to your script and modify as needed.

**Q: What if I don't want to use all functions?**  
A: Pick and choose. Each function is independent (non-destructive, takes df, returns df).

**Q: How do I add my own functions?**  
A: Append below the marker in `func_test_suite.txt` following the same format.

**Q: Can I use multiple datasets?**  
A: Yes, but run one at a time. Clean workspace between datasets.

**Q: What models work best?**  
A: Tested: GLM-4.7, llama 3.3 70b, and GPT OSS
---

## Next Steps

1. **First run**: Try with sample data, no helper_reg
2. **Learn**: Review what LLM detected and suggested
3. **Refine**: Add helper_reg guidance for your use case
4. **Integrate**: Package functions for production use

---

**Ready to start?** Open `llm-notebook.ipynb` and run cell 1! 

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

