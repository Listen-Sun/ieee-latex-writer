# LaTeX Project Workflow

## Create Or Repair A Project

1. Locate the main `.tex` file by finding `\documentclass`.
2. Confirm the class is IEEEtran or a venue-provided IEEE-compatible class.
3. Preserve the user's file layout. Do not flatten projects unless requested.
4. Keep figures in a predictable folder such as `figures/` when creating a new project.
5. Use a separate `.bib` file for references unless the official venue template embeds references.
6. Keep local macros in the preamble or a clearly named file such as `macros.tex`.

## Compile Commands

Use the project's existing tool first:

- `latexmk -pdf main.tex`
- `pdflatex main.tex`, `bibtex main`, `pdflatex main.tex`, `pdflatex main.tex`
- `xelatex` or `lualatex` only when the project already requires them or the venue allows them

When diagnosing errors:

1. Read the first real LaTeX error, not the last cascade.
2. Check missing files, unmatched braces, undefined control sequences, and package conflicts.
3. Compile again after each focused fix.
4. Preserve generated files only if the user needs them; otherwise leave source changes as the main deliverable.

## Static Audit

Run:

```bash
python scripts/audit_ieee_latex.py path/to/main.tex
```

The audit checks common risks:

- Missing IEEEtran class
- Suspicious class options
- Missing abstract, keywords, bibliography, or IEEEtran BibTeX style
- Citation keys missing from `.bib`
- Unreferenced labels
- Risky formatting packages and margin hacks
- Missing figure files and discouraged graphics extensions
- Caption/label ordering in floats

The audit is not a replacement for compilation or IEEE's official LaTeX Analyzer.

## Submission Archive Checklist

For actual submission preparation:

- Include all `.tex`, `.bib`, `.bst` if locally required, figures, and nonstandard style files.
- Exclude generated clutter unless the venue asks for it: `.aux`, `.bbl`, `.blg`, `.log`, `.out`, `.synctex.gz`.
- Include `.bbl` when the submission system requires a self-contained bibliography.
- Verify that figure file names match the source exactly, including case.
- Check whether anonymous review requires removing author names, affiliations, acknowledgments, funding IDs, repository links, or self-identifying comments.
- Run the official IEEE LaTeX Analyzer and PDF Checker for final submission.
