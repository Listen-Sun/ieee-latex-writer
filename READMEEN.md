# IEEE LaTeX Writer Open

A Codex Skill for research-paper writing across most IEEE fields, including IEEEtran journals, conferences, Letters, Magazine-style papers, and common IEEE-style submission workflows.

It goes beyond LaTeX formatting: it helps improve research narrative, contribution coherence, double-blind anonymity, experimental rigor, BibTeX cleanup, reviewer responses, and pre-submission static auditing. Robotics, reinforcement learning, control, and intelligent systems are enhanced modules, not the only supported scope.

中文版本：[README.md](README.md)

## Features

- IEEEtran paper drafting, revision, restructuring, and pre-submission checks
- Research narrative, contribution framing, experimental logic, and reviewer-aware writing across IEEE fields
- Domain modules for robotics/RL/control, computer and intelligent systems, communications and signal processing, power and energy systems, and more
- Venue-aware adaptation for IEEE Transactions, Letters, conferences, RA-L, T-RO, T-AC, ICRA, IROS, RSS, CoRL, and related venues
- Double-blind anonymity checks for authors, affiliations, grants, self-citations, and lab-identifying details
- Response Letter workflow that maps reviewer comments to concrete manuscript changes
- BibTeX cleanup, including capitalization protection, noisy-field removal, and IEEE venue abbreviation
- Static audit script for common LaTeX, citation, figure, encoding, unit, and formatting risks

## Install

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/YOUR-USER/ieee-latex-writer.git ~/.codex/skills/ieee-latex-writer
```

Or install with an Agent Skills compatible CLI:

```bash
npx skills add https://github.com/YOUR-USER/ieee-latex-writer --agent codex --yes
```

Replace `YOUR-USER` with the actual GitHub user or organization.

## Usage

Example prompt:

```text
Use $ieee-latex-writer to improve the research narrative, LaTeX structure, and submission readiness of my IEEE paper.
```

Other examples:

```text
Use $ieee-latex-writer to audit my IEEE paper for double-blind review.
```

```text
Use $ieee-latex-writer to clean my BibTeX file and check IEEE formatting risks.
```

## Repository Contents

- `SKILL.md`: Core skill instructions and trigger description
- `agents/openai.yaml`: Skill UI metadata
- `references/`: IEEE writing, LaTeX workflow, and reviewer-response references
- `assets/minimal-ieee-paper.tex`: Lightweight IEEEtran starter template
- `scripts/audit_ieee_latex.py`: Static audit script for IEEE LaTeX projects

## Static Audit

Run:

```bash
python scripts/audit_ieee_latex.py path/to/main.tex
```

The audit checks common risks such as IEEEtran class usage, risky packages, unresolved citations, missing figure files, caption/label ordering, double-blind identity leaks, Chinese/full-width punctuation, percent and unit formatting, prose inside math environments, and dirty BibTeX fields.

This script does not replace the official IEEE Template Selector, IEEE LaTeX Analyzer, Reference Preparation Assistant, PDF Checker, or target venue instructions.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR-USER/ieee-latex-writer&type=Date)](https://www.star-history.com/#YOUR-USER/ieee-latex-writer&Date)

> After publishing to GitHub, replace `YOUR-USER` with your GitHub user or organization.

## License

This project is licensed under the [MIT License](LICENSE).
