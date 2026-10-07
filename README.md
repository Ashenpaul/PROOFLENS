# PROOFLENS
# HNX26PSI08: Proof-Carrying Data Analyst (Agentic GenAI)

[![Hackathon](https://img.shields.io/badge/Hackathon-HACKNEX_Internal_Qualifier-blue.svg)](https://forms.gle/KGjkU5u66Va1MDhu5)
[![Verification](https://img.shields.io/badge/Sandbox_Verification-100%25_Deterministic-success.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

> **Presented by:** Division of Computer Science and Engineering, Karunya Institute of Technology and Sciences  
> **Domain:** Agentic GenAI · Data Analytics · Code Generation · Verification  
> **Official Submission Form:** [https://forms.gle/KGjkU5u66Va1MDhu5](https://forms.gle/KGjkU5u66Va1MDhu5)

---

## 1. What the Project Does (Executive Summary)

Real-world enterprise data is fragmented across tables and documents, riddled with silent failure modes: conflicting currencies, duplicate rows, ambiguous date notations, and contradictory accounting tables. Standard LLMs fail in these environments because they **hallucinate unverified numbers** and **overconfidently answer trick or unanswerable questions**.

**Proof-Carrying Data Analyst (PCDA)** enforces the principles of Proof-Carrying Code (PCC):
1. **Zero Unverified Numbers (Iron Rule):** Every single numerical claim emitted by the AI is bundled with **self-contained, re-runnable Python proof code**. An independent, sandboxed Verifier executes this code in an isolated subprocess to validate the exact calculation before any answer is certified.
2. **Adversarial Trap Defense ("Know When to Say No"):** A confident wrong answer scores worse than saying *"I cannot determine this from the data"*. The system detects cross-table contradictions, ambiguous dates, and trick questions, refusing them with formal evidentiary justification.
3. **Upload Any Dataset:** Ingests any custom CSV or JSON dataset, dynamically parses schemas, sanitizes dirty rows, and synthesizes verifiable mathematical proofs.

---

## 2. Technologies, Libraries, and Models Used

- **Language & Runtime:** Python 3.10+ (Standard Library: `subprocess`, `hashlib`, `http.server`, `json`, `dataclasses`, `unittest`).
- **Data Engineering & Manipulation:** `pandas` (>= 2.0.0), `numpy` (>= 1.24.0).
- **Core Reasoning Architecture:** Agentic reasoning pipeline with automated code synthesis, dynamic table matching, and self-healing repair loops.
- **Verification Engine:** Isolated subprocess execution sandbox with strict execution timeouts, stdout token parsing (`PROOF_RESULT`), and floating-point tolerance gates ($\le 10^{-4}$).
- **Security & Integrity:** SHA-256 cryptographic proof certificates sealing generated code and raw data fingerprints.
- **User Interface:** Single-page responsive web dashboard and conversational AI chatbot styled with Tailwind CSS (zero external npm/node dependencies required).

---

## 3. Data Pipeline: How Data is Collected, Processed, and Passed
