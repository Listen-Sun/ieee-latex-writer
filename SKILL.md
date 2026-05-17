---
name: ieee-latex-writer
description: IEEE LaTeX paper writing, revision, formatting, and submission-preparation support for IEEEtran journal, conference, letter, and magazine manuscripts. Use when Codex needs to draft or polish IEEE-style LaTeX papers; restructure abstracts, introductions, methods, experiments, conclusions, figures, tables, equations, BibTeX references, or responses to reviewers; create IEEEtran-compatible LaTeX skeletons; or audit .tex/.bib projects before IEEE submission.
---

# IEEE LaTeX Writer

## Core Workflow

1. Identify the target venue, manuscript type, page limit, and whether the work is a journal, conference, letter, magazine, or revision response.
2. Prefer the venue's official instructions over general IEEE habits. If requirements may have changed, verify the current venue page, IEEE Template Selector, and IEEE Author Center before making format-sensitive claims.
3. Work in IEEEtran-compatible LaTeX. Do not rewrite margins, fonts, title spacing, bibliography style, or class internals unless the venue explicitly permits it.
4. Improve the scientific argument first: claim, gap, method, evidence, limitation, and contribution. Then polish style and LaTeX mechanics.
5. Keep all edits source-preserving. Avoid overwriting user macros, comments, figure paths, bibliography databases, or local package choices unless they conflict with IEEE requirements.
6. For double-blind venues, run an anonymity pass before style polishing: remove or neutralize author names, affiliations, acknowledgments, grant numbers, lab-specific equipment/software identifiers, self-identifying URLs, and first-person self-citations.
7. For revision tasks, build a response letter with a fixed mapping for every reviewer comment: `Reviewer's Comment`, `Response`, and `Changes in the Revised Manuscript`. Keep tone polite, respectful, and evidence-based.
8. Run a compile or static audit whenever files are available. If compilation is not possible, state the reason and run `scripts/audit_ieee_latex.py` as a lightweight check.

## Resource Map

- Read `references/ieee-style-guide.md` for IEEE-specific writing, structure, citation, figure, table, and equation guidance.
- Read `references/latex-project-workflow.md` when creating or repairing a LaTeX project, choosing compile commands, or preparing a submission archive.
- Read `references/revision-and-review.md` when revising a draft, responding to reviewers, generating a response letter, or turning notes/results into an IEEE paper.
- Use `assets/minimal-ieee-paper.tex` only as a lightweight starter skeleton. For real submission templates, direct the user to the official IEEE Template Selector or the target venue package.
- Run `scripts/audit_ieee_latex.py <project-or-main.tex>` to detect common IEEE LaTeX risks before submission.

## Drafting Rules

- Write in a precise technical voice: concrete nouns, active verbs where natural, and claims tied to evidence.
- Make the abstract self-contained: problem, gap, method, main quantitative result, and significance. Avoid citations, undefined acronyms, display equations, and vague hype.
- Make the introduction answer: why the problem matters, what prior approaches miss, what this paper contributes, and how the evidence supports the contribution.
- Use contribution bullets only when the venue style allows them. Keep each contribution falsifiable and tied to a section or result.
- Put limitations and assumptions where they help credibility: end of introduction, discussion, experiment setup, or conclusion.
- Use IEEE citation style in prose: "Smith et al. [1]" or "prior work [1], [2]" rather than author-year phrasing.
- For double-blind review, rewrite self-citations in third person: use "Li et al. [1]" or "the method in [1]" instead of "in our previous work [1]". Do not expose identity through author initials, repository names, acknowledgments, grants, institutional facilities, lab-only datasets, or uniquely named internal equipment/software.
- For preprints, check the venue's current arXiv/preprint policy before citing or describing overlap. If allowed, cite the preprint neutrally in third person during double-blind review and avoid wording that reveals authorship.

## LaTeX Rules

- Start from `\documentclass[conference]{IEEEtran}` for conferences and `\documentclass[journal]{IEEEtran}` or the venue-provided variant for journals, unless the official template says otherwise.
- Use BibTeX with `\bibliographystyle{IEEEtran}` unless the venue explicitly requires another workflow.
- Keep figures, tables, equations, algorithms, and references in normal IEEE floating environments. Avoid manual placement hacks such as repeated negative `\vspace`, margin changes, or font-size compression.
- Prefer vector graphics (`.pdf`, `.eps`) for plots and diagrams, and high-resolution `.png`/`.tif` only when raster output is appropriate.
- Place table captions above tables and figure captions below figures. Put labels after captions so references resolve correctly.
- Use `\IEEEeqnarray` or aligned math environments for long equations. Do not use screenshots of equations.
- For control, robotics, navigation, and guidance papers, enforce symbol continuity: keep state variables, control inputs, disturbances, outputs, estimates, errors, and gains consistent across text, equations, algorithms, and figures. Distinguish continuous-time notation such as `$x(t)$`, `$\dot{x}(t)$`, and `$u(t)$` from discrete-time notation such as `$x_k$`, `$x_{k+1}$`, and `$u_k$`; do not mix them without defining the sampling relationship.
- For stability proofs, present Lyapunov functions and derivatives/differences rigorously: define `$V(x)$`, state positive definiteness and radial unboundedness when needed, derive `$\dot{V}(x)$` or `$\Delta V_k$`, and connect the sign condition to the claimed stability theorem. Avoid skipping from an algebraic inequality directly to "therefore stable" without conditions.
- In math environments, wrap descriptive text in `\text{...}` and keep Chinese text out of equations unless the venue explicitly allows it. Use English notation and prose for IEEE submissions.
- Sanitize BibTeX before final submission. Preserve capitalization with double braces for proper nouns and acronyms, e.g., `{{Kalman}} filter`, `{{IEEE}}`, and `{{LiDAR}}`; remove noisy fields such as `publisher`, `issn`, `isbn`, `url`, `arxivId`, `archivePrefix`, `eprint`, and `abstract` unless the venue requires them; normalize IEEE journal names to official abbreviations such as `IEEE Trans. Robot.`.
- Keep package additions conservative. Be suspicious of `geometry`, `fullpage`, `titlesec`, `caption`, and heavy class/style modifications in final submissions.

## Static Audit Spectrum

When compilation is unavailable, simulate or run `scripts/audit_ieee_latex.py` and report findings by severity. The audit must cover:

- IEEEtran class usage, common mode options, abstract/keywords, bibliography style, citation keys, labels, figure files, graphics extensions, and float caption/label ordering.
- Double-blind risks: author names or affiliations in author blocks, acknowledgments, funding/grant numbers, self-identifying phrases, and first-person self-citations such as "our previous work [1]".
- Text hygiene: Chinese characters or Chinese punctuation in the manuscript body, raw Chinese commas/periods/parentheses, unescaped percent signs, and likely missing spaces before physical units such as `10m`, `3V`, or `180C`.
- Math hygiene: Chinese characters or narrative English words inside equation-like environments unless wrapped in `\text{...}`.
- BibTeX hygiene: missing keys, dirty exported fields, unprotected capitalization for known technical terms, and nonstandard IEEE journal names when detectable.

## Submission Checks

Before calling a paper ready:

1. Compile from a clean checkout with the same engine the project expects.
2. Check that references resolve, citation keys exist, figures are included, and the generated PDF has no overfull boxes in important text.
3. Run IEEE's official LaTeX Analyzer, Reference Preparation Assistant, and PDF Checker when preparing an actual IEEE submission.
4. Confirm the target venue's current page limit, anonymity requirements, preprint/arXiv policy, funding/acknowledgment placement, supplementary-material rules, and copyright/ORCID requirements.
5. For double-blind review, verify that author metadata, grants, acknowledgments, self-citations, institutional repositories, and lab-specific artifacts are anonymized in both source and PDF.
6. State remaining risks clearly if only a static audit was possible.
