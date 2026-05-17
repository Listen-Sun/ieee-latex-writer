# IEEE LaTeX Writer

A Codex skill for drafting, revising, formatting, and auditing IEEE-style LaTeX papers.

It helps with IEEEtran manuscripts, paper structure, abstracts, introductions, methods, results, figures, tables, equations, BibTeX references, reviewer responses, and pre-submission checks.

## Install

Copy or clone this folder into your Codex skills directory:

```bash
git clone https://github.com/YOUR-USER/ieee-latex-writer.git ~/.codex/skills/ieee-latex-writer
```

Then invoke it as:

```text
Use $ieee-latex-writer to audit my IEEE LaTeX paper before submission.
```

## Included

- `SKILL.md`: Core skill instructions and trigger description
- `references/`: IEEE writing, LaTeX workflow, and reviewer-response guidance
- `assets/minimal-ieee-paper.tex`: Lightweight starter skeleton
- `scripts/audit_ieee_latex.py`: Static audit for common IEEE LaTeX issues

## Static Audit

```bash
python scripts/audit_ieee_latex.py path/to/main.tex
```

The audit checks common risks such as missing IEEEtran class usage, risky formatting packages, unresolved citations, missing figure files, float caption/label ordering, double-blind identity leaks, Chinese/full-width punctuation, percent and unit formatting, math-environment prose, and dirty BibTeX fields.

This does not replace the official IEEE Template Selector, IEEE LaTeX Analyzer, Reference Preparation Assistant, PDF Checker, or target venue instructions.

## License

MIT
