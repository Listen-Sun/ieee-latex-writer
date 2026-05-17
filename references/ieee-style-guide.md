# IEEE Style Guide

## Official Sources To Check

- IEEE Author Center authoring tools and templates: https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/
- IEEE tools for authors: https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/authoring-tools-and-templates/tools-for-ieee-authors/
- IEEE Template Selector: https://template-selector.ieee.org/
- IEEE LaTeX Analyzer: https://latexqc.ieee.org/
- IEEE Reference Preparation Assistant: https://refassist.ieee.org/
- IEEE PDF Checker: https://ieee-pdfchecker.org/
- CTAN IEEEtran package: https://www.ctan.org/pkg/ieeetran

Treat these as navigation pointers, not frozen rules. Verify current venue pages for page limits, anonymity, open-access language, data/code policies, and special class options.

## Paper Structure

Common IEEE research article flow:

1. Title
2. Abstract
3. Index Terms
4. Introduction
5. Related Work or Background
6. Method/System/Model
7. Experimental Setup or Analysis
8. Results
9. Discussion, Limitations, or Ablation
10. Conclusion
11. Acknowledgment, when allowed and placed by venue rules
12. References
13. Appendices, biographies, or supplementary material if required

Conference papers often compress background and related work. Journal papers often need fuller derivations, broader experiments, and clearer reproducibility detail.

## Abstract

Use one paragraph unless the venue says otherwise. Include:

- Problem and context
- Gap or limitation in existing work
- Proposed method
- Key results with numbers where possible
- Main implication

Avoid:

- Citations
- Undefined acronyms
- Displayed equations
- Claims such as "first", "novel", or "significant" without precise support
- Implementation details that belong in methods

## Introduction

Use a clear argument chain:

1. Problem importance
2. Specific technical difficulty
3. Existing families of approaches and their limitation
4. Paper's core idea
5. Contributions and evidence

Good contribution statements are measurable:

- "We formulate..."
- "We design..."
- "We prove..."
- "We evaluate..."
- "We release..."

Avoid contribution statements that only describe writing:

- "We introduce the background..."
- "We discuss..."
- "The paper is organized as follows..."

## Figures And Tables

- Use figures to prove a point, not to decorate.
- Give each figure a message title in the caption's first sentence.
- Define symbols, colors, and abbreviations in captions or nearby text.
- Use consistent fonts and sizes across plots.
- Refer to every figure and table in the text.
- Put table captions above tables and figure captions below figures.
- Keep tables compact, but do not shrink below readability.
- Prefer `table*` and `figure*` only when a two-column float is necessary.

IEEE Author Center notes that IEEE graphics submissions accept PS, EPS, PDF, PNG, or TIFF. It also gives naming and graphics preparation guidance, including flattening layers and checking resolution/dimensions before submission.

## Equations

- Define every symbol before or immediately after first use.
- Use equations only when they improve precision.
- Number equations that are referenced in text.
- Use `\IEEEeqnarray`, `align`, or `aligned` for multi-line equations.
- Avoid using images for equations.
- Check dimensional consistency and units.

## Citations And Bibliography

- Use numbered IEEE citations: `[1]`, `[2]`, `[3]`.
- In prose, write "Smith et al. [1]" rather than "(Smith et al., 2024)".
- Group citations only when they support the same claim.
- Cite primary sources for technical claims.
- Keep BibTeX fields complete enough for IEEE formatting: authors, title, venue, year, pages/article number, DOI when available.
- Use `\bibliographystyle{IEEEtran}` with BibTeX unless the venue gives a different instruction.

## Double-Blind And Preprints

For double-blind review:

- Replace author blocks with the venue's anonymous template or neutral placeholders.
- Remove acknowledgments, grant numbers, funding IDs, project IDs, ORCID IDs, personal websites, institutional repositories, and lab-specific URLs.
- Neutralize unique internal equipment or software descriptions that identify the lab. Prefer generic descriptions unless the detail is scientifically necessary.
- Rewrite first-person self-citations. Use "Li et al. [1]" or "the approach in [1]" instead of "our previous work [1]".
- Check figure metadata, filenames, supplementary files, and comments for identity leaks.

For preprints:

- Verify the venue's current arXiv and preprint policy before submission.
- Cite an allowed preprint in third person during double-blind review.
- Avoid explaining that the submitted manuscript is an extension of "our arXiv paper" unless the venue explicitly permits such disclosure.
- When overlap must be explained, use neutral wording and follow the venue's disclosure mechanism.

## BibTeX Sanitization

Clean exported `.bib` entries before final submission:

- Protect proper nouns and acronyms with double braces: `{{Kalman}} filter`, `{{IEEE}}`, `{{ROS}}`, `{{LiDAR}}`.
- Remove fields that usually pollute IEEEtran output: `publisher`, `issn`, `isbn`, `url`, `arxivId`, `archivePrefix`, `eprint`, `abstract`, `keywords`, and `language`, unless the venue requires them.
- Keep useful identifiers such as `doi` when present and accurate.
- Normalize IEEE journal names to official abbreviations, for example `IEEE Trans. Robot.` instead of `IEEE Transactions on Robotics`.
- Keep BibTeX keys stable when editing so existing `\cite{...}` commands do not break.

Common IEEE abbreviations:

- `IEEE Transactions on Robotics` -> `IEEE Trans. Robot.`
- `IEEE Transactions on Automatic Control` -> `IEEE Trans. Automat. Control`
- `IEEE Transactions on Control Systems Technology` -> `IEEE Trans. Control Syst. Technol.`
- `IEEE Robotics and Automation Letters` -> `IEEE Robot. Autom. Lett.`
- `IEEE Transactions on Intelligent Transportation Systems` -> `IEEE Trans. Intell. Transp. Syst.`

## Control And Robotics Notation

- Keep state, input, disturbance, output, estimate, and error notation stable across the entire paper.
- Use a defined convention such as `$x(t)$`, `$u(t)$`, `$w(t)$`, and `$y(t)$` for continuous-time systems.
- Use `$x_k$`, `$x_{k+1}$`, `$u_k$`, `$w_k$`, and `$y_k$` for discrete-time systems.
- Define the sampling relationship if both forms appear, for example `$x_k = x(kT_s)$`.
- Use bold or matrix notation consistently. Do not switch between `$A$`, `$\mathbf{A}$`, and `$\bm{A}$` without a rule.
- For Lyapunov arguments, state assumptions, choose `$V(x)$`, prove positive definiteness, derive `$\dot{V}(x)$` or `$\Delta V_k$`, and cite or state the theorem connecting the inequality to stability.
- Distinguish local, global, asymptotic, exponential, input-to-state, and practical stability claims.

## Language Polish

Prefer:

- "reduces latency by 18%" over "greatly improves latency"
- "under the same compute budget" over "fairly"
- "we observe" for empirical findings and "we prove" for formal results
- "may" for plausible but unproven interpretations

Avoid:

- Marketing adjectives
- Overclaiming causality from correlation
- Long noun stacks
- Ambiguous "this", "it", and "they"
- Unexplained acronyms
