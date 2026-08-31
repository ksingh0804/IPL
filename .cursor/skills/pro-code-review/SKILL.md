---
name: pro-code-review
description: Staff-level code review covering memory leaks, resource lifetime, security, concurrency, correctness, and related production defects. Use when the user asks for a code review, PR review, leak check, leak hunt, production readiness review, or to "review like a pro".
---

# Professional Code Review

Use this skill whenever you are asked to review code, a PR, a diff, or to
check for memory leaks and similar production defects.

Read and follow `prompts/pro-code-review.md` as the source of truth.
Paste-equivalent rules are restated below so you can execute them without
waiting for a human to fill placeholders.

## When to apply

- User asks for a code review, PR review, or "review like a senior / pro"
- User mentions memory leaks, resource leaks, file-descriptor leaks,
  matplotlib figure leaks, pandas copies, or unbounded caches
- User asks for a production-readiness or merge-readiness check

## Inputs you must gather first

1. Diff: `git diff` against the base branch, or the files the user named.
2. Intent: PR title, commit messages, issue text, or stated goal.
3. Surrounding context: callers of every changed function that acquires a
   resource (files, sockets, HTTP, plots, DataFrames, threads, processes).

Do not review from memory of a previous turn. Re-read the current files.

## Review order

1. Correctness of the intended behavior
2. Safety: crashes, data loss, undefined behavior
3. Memory and resource leaks (see below)
4. Security
5. Concurrency
6. Error handling
7. Performance at realistic scale
8. Tests and observability
9. Maintainability only when it will cause bugs

Skip nits. Do not praise style. Do not invent issues.

## Memory and resource leaks

A leak is any acquired resource that is not released on every path,
including exceptions, early returns, cancellation, and retries.

Inspect this repo's common sources:

- `scripts/bootstrap_legacy_data.py`: `urlopen`, writes into `site-packages`
- `IPL.ipynb`: `pd.read_csv` of `Match.csv` / `Deliveries.csv`, derived
  frames kept in the kernel, matplotlib / seaborn figures, cell re-runs
- Any new I/O, caches, threads, or long-lived globals

For each suspected leak report:

- What is acquired
- Which path fails to release it
- How it grows (once vs per request / cell / figure / retry)
- Whether GC / notebook restart would hide it
- Smallest correct fix
- How to verify (`with` rewrite, `plt.get_fignums()`, `tracemalloc`,
  `resource.getrusage`, `lsof`, heap profile)

Do not mark exploratory pandas copies in a one-shot notebook as Blocker
unless they will OOM on realistic data or live in a long-running process.
Do flag unbounded growth and unclosed native / FD / HTTP handles as
High or Blocker.

## Output

Start with a 3–6 line verdict: ship / request changes / block, and the
risks you would lose sleep over.

Then a markdown table:

| Severity | Category | Location | Defect | Why it matters | Fix |
|---|---|---|---|---|---|

Then one section per Blocker / High / Medium finding:

### [SEVERITY] {short title}

- Location, category, evidence, failure mode, suggested fix, confidence,
  how to verify

End with residual risks, tests you would add, and explicit "no leak found
in X" notes for resource-owning paths you inspected and found clean.

If the change is actually fine, say so and list what you checked.

## After the review

If the user asked only for a review, do not start rewriting the code
unless they also asked for fixes. Offer to apply the High / Blocker fixes
next.
