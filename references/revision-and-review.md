# Revision And Review Workflow

## Editing A Draft

First diagnose the paper's argument:

1. What is the central claim?
2. What exact gap does it fill?
3. What method or system enables the claim?
4. What evidence supports it?
5. What limitations remain?

Then edit in this order:

1. Abstract and introduction logic
2. Section order and paragraph transitions
3. Method clarity and reproducibility
4. Experimental fairness and result interpretation
5. Figure/table captions
6. Sentence-level polish
7. LaTeX and reference cleanup

## Paragraph Pattern

For technical exposition, prefer:

1. Topic sentence stating the point
2. Necessary context or definition
3. Evidence, derivation, or example
4. Interpretation tied to the paper's claim

Avoid paragraphs that are only literature lists. Convert "A did X. B did Y. C did Z." into categories, contrast, and gap statements.

## Related Work

Organize by technical families, not by chronology. For each family:

- State the shared idea
- Name representative work
- Explain what it cannot handle for this paper's setting
- Connect to the proposed method

Do not make novelty depend on weak phrases such as "to the best of our knowledge" unless the venue expects it and the claim is narrow.

## Results

For each result section:

1. State the question.
2. Describe the setup only as much as needed.
3. Report the main number or trend.
4. Explain why it happens.
5. Tie it back to the contribution.

Use absolute and relative improvements carefully. If the baseline is unstable or the denominator is small, report raw values too.

## Reviewer Response

For each reviewer comment:

1. Thank the reviewer briefly.
2. State the action taken.
3. Quote or summarize the changed manuscript location.
4. Provide evidence when disagreeing.
5. Keep tone factual and calm.

Response template:

```text
Comment: [reviewer comment]

Response: Thank you for pointing this out. We have revised Section X to clarify [issue]. Specifically, we now [change]. The revised text reads: "[short excerpt]". This change addresses the concern by [reason].
```

When disagreeing:

```text
Response: We agree that [shared premise]. However, [evidence or constraint]. To avoid ambiguity, we have added [clarification/limitation] in Section X.
```
