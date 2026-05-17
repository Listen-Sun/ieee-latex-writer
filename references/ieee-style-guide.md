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
