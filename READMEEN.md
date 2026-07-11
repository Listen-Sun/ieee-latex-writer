# IEEE LaTeX Writer Open

A Codex Skill for research-paper writing across most IEEE fields, including IEEEtran journals, conferences, Letters, Magazine-style papers, and common IEEE-style submission workflows.

It goes beyond LaTeX formatting: it helps improve research narrative, contribution coherence, double-blind anonymity, experimental rigor, formal citation verification, BibTeX cleanup, reviewer responses, and pre-submission static auditing. Robotics, reinforcement learning, control, and intelligent systems are enhanced modules, not the only supported scope.

中文版本：[README.md](README.md)

## Features

- IEEEtran paper drafting, revision, restructuring, and pre-submission checks
- Research narrative, contribution framing, experimental logic, and reviewer-aware writing across IEEE fields
- Domain modules for robotics/RL/control, computer and intelligent systems, communications and signal processing, power and energy systems, and more
- Venue-aware adaptation for IEEE Transactions, Letters, conferences, RA-L, T-RO, T-AC, ICRA, IROS, RSS, CoRL, and related venues
- Double-blind anonymity checks for authors, affiliations, grants, self-citations, and lab-identifying details
- Response Letter workflow that maps reviewer comments to concrete manuscript changes
- Authorized scholarly lookup workflow for DOI, publisher records, access status, and formal publication versions
- BibTeX cleanup, including capitalization protection, noisy-field removal, DOI preservation, arXiv/preprint handling, and IEEE venue abbreviation
- Static audit script for common LaTeX, citation, figure, encoding, unit, and formatting risks

## Install

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/Listen-Sun/ieee-latex-writer.git ~/.codex/skills/ieee-latex-writer
```

For a workspace-local install, keep the editable source anywhere convenient and mirror or copy the `ieee-latex-writer` folder into:

```text
<workspace>/.agents/skills/ieee-latex-writer
```

Or install with an Agent Skills compatible CLI:

```bash
npx skills add https://github.com/Listen-Sun/ieee-latex-writer --agent codex --yes
```

## Update

If the repository is installed directly in the Codex skills directory, run:

```bash
git -C ~/.codex/skills/ieee-latex-writer pull
```

If it was installed through an Agent Skills compatible CLI, rerun the install command to refresh it:

```bash
npx skills add https://github.com/Listen-Sun/ieee-latex-writer --agent codex --yes
```

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

```text
Use $ieee-latex-writer to find the formal publication version, DOI, access status, and IEEEtran BibTeX for these papers.
```

If IEEE Xplore returns `418`, `403`, `429`, or a `202` response with no paper content or a challenge page, the skill treats it as a publisher automation/access block and falls back to legal sources such as DOI records, Crossref, OpenAlex, DBLP, arXiv, or author-posted manuscripts. It explicitly distinguishes metadata/abstract access from full-text reading.

Run:

```bash
python scripts/lookup_ieee_paper.py https://ieeexplore.ieee.org/document/11279722/
```

If institutional access works only in the normal browser, hand the page to that browser:

```bash
python scripts/lookup_ieee_paper.py https://ieeexplore.ieee.org/document/11279722/ --open-browser
```

Download the PDF legally in the browser, then let Codex read the local PDF. The script never exports or reuses browser cookies.

For exact IEEE article-number lookup, obtain a Metadata API key from the IEEE Developer Portal and set it only in the local environment:

```powershell
$env:IEEE_XPLORE_API_KEY="your-local-api-key"
python scripts/lookup_ieee_paper.py 11279722
```

Never commit or paste the API key into paper files or chat prompts.

## Repository Contents

- `SKILL.md`: Core skill instructions and trigger description
- `agents/openai.yaml`: Skill UI metadata
- `references/`: IEEE writing, LaTeX workflow, and reviewer-response references
- `assets/ieee-official-templates/`: Bundled official IEEEtran template files and instructions
- `scripts/audit_ieee_latex.py`: Static audit script for IEEE LaTeX projects
- `scripts/clean_ieee_bib.py`: Conservative IEEEtran BibTeX cleanup script
- `scripts/lookup_ieee_paper.py`: Resilient paper lookup through the official IEEE API and scholarly-index fallbacks
- `.codex-plugin/plugin.json`: Optional package metadata for plugin-style skill distribution

## Static Audit

Run:

```bash
python scripts/audit_ieee_latex.py path/to/main.tex
```

The audit checks common risks such as IEEEtran class usage, risky packages, unresolved citations, missing figure files, caption/label ordering, double-blind identity leaks, Chinese/full-width punctuation, percent and unit formatting, prose inside math environments, and dirty BibTeX fields.

This script does not replace the official IEEE Template Selector, IEEE LaTeX Analyzer, Reference Preparation Assistant, PDF Checker, or target venue instructions.

## BibTeX Cleanup

Run:

```bash
python scripts/clean_ieee_bib.py path/to/references.bib
```

The script writes `*_ieee_clean.bib` beside the input, preserves citation keys, removes common exported noise fields, and protects common robotics/control/learning acronyms in titles. Review DOI completeness, venue correctness, duplicates, and arXiv-only entries manually before submission.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Listen-Sun/ieee-latex-writer&type=Date)](https://www.star-history.com/#Listen-Sun/ieee-latex-writer&Date)

## License

This project is licensed under the [MIT License](LICENSE).
