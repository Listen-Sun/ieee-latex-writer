---
name: ieee-latex-writer
description: Open-community research-paper and IEEE LaTeX writing support for most IEEE fields, including IEEEtran journals, conferences, letters, magazines, robotics, reinforcement learning, control, intelligent systems, communications, signal processing, power, energy, and related venues. Use when Codex needs to draft, polish, anonymize, audit, or strategically reshape IEEE-style research manuscripts; improve scientific narrative, contribution coherence, reviewer awareness, experimental rigor, domain-specific notation, LaTeX structure, BibTeX references, reviewer responses, or static checks on .tex/.bib projects before submission.
---

# IEEE LaTeX Writer Open

Open-community skill for writing, revising, anonymizing, and auditing IEEE-style LaTeX manuscripts across most engineering and computing fields. Treat paper strategy and scientific argument quality as first-class tasks, then apply venue style, domain conventions, LaTeX mechanics, and static checks.

## Core Workflow

1. Identify the target venue, IEEE society/field, manuscript type, page limit, review mode, and submission stage: first submission, double-blind review, revision, camera-ready, or archive cleanup.
2. Verify format-sensitive requirements when they may have changed: venue page, IEEE Template Selector, IEEE Author Center, page limits, anonymity policy, preprint/arXiv policy, supplementary-material rules, and bibliography requirements.
3. Work in IEEEtran-compatible LaTeX. Do not modify margins, fonts, title spacing, bibliography style, or class internals unless the venue explicitly allows it.
4. Identify the paper strategy before line editing: core novelty, likely reviewer concerns, missing evidence, weak ablations, venue fit, and whether secondary ideas dilute the main contribution.
5. Route the manuscript through the relevant venue and domain modules before polishing: robotics/control, RL robotics, computer science/intelligent systems, communications/signal processing, power/energy systems, or general IEEE engineering.
6. Improve the scientific argument first: claim, gap, method, evidence, limitation, contribution, and reproducibility. Then polish style, notation, and LaTeX mechanics.
7. Preserve user source structure. Avoid overwriting macros, comments, figure paths, bibliography databases, or package choices unless they conflict with IEEE requirements.
8. For double-blind review, run an anonymity pass before style polishing. Detect and flag author names, affiliations, acknowledgments, grant numbers, ORCID IDs, repository links, institutional URLs, lab-specific datasets, and distinctive equipment/software descriptions.
9. Rewrite self-citations in third person. Use forms such as "In [1], Smith et al. developed..." or "The method in [1]..." and never "In our previous work [1]..." during double-blind review.
10. For revision tasks, create a response letter with a fixed mapping for every reviewer item: `Reviewer's Comment`, `Response`, and `Changes in the Revised Manuscript`. Keep the tone polite, respectful, specific, and evidence-based.
11. Run compilation or static audit when files are available. If compilation is unavailable, run or simulate `scripts/audit_ieee_latex.py <project-or-main.tex>` and report residual risks.

## Resource Map

- Read `references/ieee-style-guide.md` for IEEE writing, citation, figure, table, equation, anonymity, BibTeX, and domain-notation guidance.
- Read `references/latex-project-workflow.md` when creating or repairing a LaTeX project, choosing compile commands, preparing an archive, or explaining the static audit spectrum.
- Read `references/revision-and-review.md` when revising a draft, building a response letter, mapping reviewer comments to manuscript changes, or marking changed text.
- Use `assets/ieee-official-templates/` as the bundled IEEEtran starter package when a local template is needed. Prefer the target venue's current template package or IEEE Template Selector for real submissions, then fall back to the bundled official journal sample.
- Run `scripts/audit_ieee_latex.py <project-or-main.tex>` for lightweight static checks. Treat it as a preflight aid, not a replacement for compilation or official IEEE validation tools.

## Paper Strategy Layer

Before drafting or revising, identify the paper's strategic shape:

- State the core novelty in one sentence. Separate it from supporting modules, implementation details, and replaceable engineering components.
- Map the title, abstract, introduction, method, experiments, and conclusion to the same central claim. If any section sells a different paper, revise it.
- Identify likely reviewer attacks: missing baselines, weak ablations, scalability, sim-to-real gap, hardware fragility, unclear novelty, statistical weakness, excessive complexity, or overclaiming.
- Suppress secondary ideas that dilute the main contribution. Move them to ablations, implementation details, appendices, or limitations unless they are essential to the claim.
- Label each contribution as methodological novelty, scientific insight, system integration, or engineering optimization. Do not present routine tuning as a conceptual breakthrough.
- Check whether the paper would still stand if an auxiliary module were replaced. If yes, describe that module as engineering support, not the main innovation.

## Research Narrative Constraints

Use this as the main reasoning layer for paper quality:

- Enforce a closed chain: Problem -> Limitation -> Insight -> Method -> Evidence. Every abstract, introduction, and conclusion should preserve this chain.
- Make every contribution map to a prior limitation, a method component, and a concrete evidence source such as theorem, ablation, benchmark, deployment, or failure analysis.
- Avoid floating modules. Every estimator, reward term, transformer block, curriculum stage, filter, loss, or controller component must have a causal role in the stated limitation.
- Force introductions to explain why existing methods fundamentally fail in the target setting, not merely that they perform worse.
- Distinguish engineering optimization, methodological novelty, scientific insight, and system integration. Use different claim strength for each.
- Identify the core innovation versus auxiliary modules. Do not let a long method list hide a weak central idea.
- Keep abstract, introduction, and conclusion consistent in claim scope, evidence, and limitations.
- Require ablation isolation logic: each ablation should test one causal hypothesis, not just remove a convenient block.
- Avoid unsupported claims. If evidence is missing, weaken the statement or add a TODO rather than inventing a result.
- Discourage novelty inflation. Prefer "we show that X enables Y under Z" over broad claims of generality.

## Venue Style Adaptation

Adapt emphasis to the target venue:

- `T-RO` and `RA-L`: balance technical clarity, embodied validation, hardware realism, failure cases, and reproducibility. Prefer concise claims with strong experiments.
- For RA-L with ICRA/IROS joint submission, maintain two page-budget modes: a compact conference-facing version and the RA-L journal version. Shift detail between main text, references, appendices/supplementary material, and biographies according to the active template; hide biographies during review when required and restore them only for accepted journal/camera-ready files. Adjust reference compactness only through venue-approved bibliography/template settings, never by manual font or spacing hacks.
- `T-AC` and control-theory venues: prioritize formal problem statements, assumptions, theorem/proof structure, stability or convergence guarantees, and precise notation.
- `ICRA` and `IROS`: emphasize a clear robotics problem, system contribution, implementation detail, comparisons, and real or credible simulated deployment.
- `RSS`: favor insight-driven robotics papers with clean problem framing, convincing analysis, strong experiments, and restrained writing.
- `CoRL`: favor learning-based robotics, representation, policy learning, generalization, sim-to-real evidence, and careful ablations.
- NeurIPS-style robotics papers: emphasize representation learning, objective design, benchmark protocol, statistical rigor, and generalizable insight over system description alone.
- For theorem-heavy papers, lead with assumptions, definitions, lemmas, guarantees, and proof intuition.
- For empirical papers, lead with a sharp failure mode, method intuition, baselines, ablations, and credible deployment or benchmark evidence.
- For system papers, lead with integration constraints, reliability, latency, hardware, interfaces, and failure recovery.

## Domain-Specific Modules

Select the closest module from the venue, topic, or manuscript vocabulary. If multiple modules apply, combine them conservatively and state the chosen assumptions.

### Robotics, Automation, And Control

Typical venues include T-RO, T-ASE, L-CSS, T-CST, T-AC, RA-L, ICRA, IROS, RSS, CoRL, CDC, and ACC.

- Enforce notation continuity for states, inputs, disturbances, outputs, estimates, errors, gains, frames, and constraints across prose, equations, algorithms, figures, and tables.
- Use standard italic symbols for scalars and a consistent bold or bold-italic convention for vectors, matrices, and tensors. Do not switch between `$A$`, `$\mathbf{A}$`, `$\boldsymbol{A}$`, and `$\bm{A}$` without defining a convention.
- Distinguish continuous-time systems such as `$x(t)$`, `$\dot{x}(t)$`, and `$u(t)$` from discrete-time systems such as `$x_k$`, `$x_{k+1}$`, and `$u_k$`. Define the sampling relation when both appear, for example `$x_k=x(kT_s)$`.
- For Lyapunov, barrier, passivity, ISS, or MPC stability arguments, define the candidate function, domain, assumptions, positive definiteness, radial unboundedness when needed, derivative or difference bounds, and the theorem-level stability claim. Use rigorous inequalities such as `$\dot{V}(x)\le -\alpha(\|x\|)$` or `$\Delta V_k\le -\ell(x_k,u_k)$`; do not jump from algebra to "therefore stable" without boundary conditions.
- Separate simulation parameters from real hardware validation. State simulator, physics settings, random seeds, controller frequency, sensor suite, compute platform, calibration, environment, and safety constraints when relevant.
- For modern embodied-AI papers, define the observation space, latent representation, adaptation mechanism, policy/controller interface, reward or objective, randomization protocol, and deployment pipeline as separate concepts.
- For blind locomotion or adaptation-based control, distinguish what is privileged during training from what is deployable on the robot.
- Avoid identity leaks from lab-specific robots, motion-capture rooms, internal software stacks, facility names, or repository URLs during double-blind review.

### Reinforcement Learning Robotics Module

Use this module for RL locomotion, manipulation, navigation, sim-to-real control, adaptation, and partially observable embodied systems.

- Formulate the task as an MDP or POMDP when appropriate. Define state, observation, action, transition assumptions, reward, discount, horizon, termination, and partial observability.
- Separate privileged observations from deployable observations. Make clear which signals are available only in simulation, teacher policies, critics, estimators, or training-time adaptation.
- Define observation history handling: frame stacking, recurrent policy, temporal convolution, transformer, history encoder, or state estimator. Explain why memory is needed.
- Separate observation design, latent representation, adaptation module, policy head, reward design, curriculum, randomization, and deployment pipeline. Do not merge them into a vague "network architecture".
- Specify reward terms with equations or tables, including weights, units, clipping, termination penalties, and which terms are diagnostic versus essential.
- Report terrain, command, dynamics, sensor, latency, actuator, payload, friction, mass, push, and noise randomization. State which randomizations are used for robustness and which model known real-world uncertainty.
- Define disturbance protocols: push magnitude/duration, terrain geometry, sensor dropout, command changes, external loads, recovery windows, and failure thresholds.
- Include failure metrics, not only success metrics: falls, resets, foot slippage, collisions, tracking loss, energy spikes, unsafe torques, overheating, timeout, or recovery failure.
- State sim-to-real assumptions: simulator, actuator model, latency, control frequency, policy frequency, observation delay, filtering, calibration, and onboard compute.
- Do not claim real-time deployment without latency, frequency, and hardware evidence.

### Computer Science And Intelligent Systems

Typical venues include T-PAMI, T-NNLS, T-CYB, T-CC, T-MC, T-KDE, TDSC, CVPR, ICCV, ICML-adjacent IEEE submissions, and intelligent systems venues.

- Use `algorithmicx`, `algpseudocode`, or `algorithm2e` consistently. Every algorithm must include explicit input, output, initialization when needed, complete control-flow closure, and line references when discussed in prose.
- Include time and space complexity in Big-O notation for each algorithm or major step. If complexity differs by training/inference, average/worst case, graph density, or batch size, state the regime.
- Disclose dataset splits: training, validation, test, cross-validation folds, leakage prevention, preprocessing, augmentation, class balance, and evaluation protocol.
- Report reproducibility state: random seeds, number of runs, hardware, framework versions when relevant, checkpoint selection, hyperparameter search budget, and statistical uncertainty.
- Define metrics precisely and avoid cherry-picking. For learned systems, separate model architecture, optimization, ablation, and deployment assumptions.
- Ensure pseudocode control flow is closed: `end if`, `end for`, `end while`, and `end procedure/function` where the chosen package style requires them.

### Communications And Signal Processing

Typical venues include T-WC, T-COM, T-SP, SPL, T-IT, JSAC, ICC, GLOBECOM, and ICASSP.

- Keep time-domain and frequency-domain notation distinct: use forms such as `$x[n]$`, `$x(t)$`, `$X(e^{j\omega})$`, `$X(f)$`, and `$X[k]$` according to signal type and transform.
- Distinguish random variables from realizations: use uppercase for random variables and lowercase for observed values when following that convention, and define any deviation.
- Define probability spaces, distributions, expectations, covariance matrices, noise assumptions, and independence conditions before using them in derivations.
- Expand standard acronyms at first use, including MIMO, OFDM, SNR, SINR, CSI, BER, SER, AWGN, DFT, FFT, and MMSE. For acronym-heavy manuscripts, create or maintain a notation/acronym table.
- Keep channel, antenna, subcarrier, block, and time-slot indices consistent. Avoid reusing `$N$`, `$M$`, or `$K$` for different dimensions without a notation table.

### Power And Energy Systems

Typical venues include T-PWRS, T-PS, T-SG, T-TE, T-IA, T-PEL, PESGM, ECCE, and industrial application venues.

- Format per-unit notation consistently as `p.u.` and define the base power, base voltage, and conversion assumptions.
- Use standard power and electrical units with nonbreaking spaces: `10~kW`, `5~MW`, `2~MVAR`, `60~Hz`, `13.8~kV`, and `0.95~p.u.`.
- Distinguish phase labels `A`, `B`, and `C`, line-to-line versus line-to-neutral voltage, active/reactive/apparent power, and RMS versus peak quantities.
- Describe bus configuration, line data, generator/load models, contingencies, and network topology clearly. When using IEEE standard test systems, name them precisely, for example IEEE 14-bus, 39-bus, 57-bus, or 118-bus systems.
- Separate simulation studies from field, HIL, OPAL-RT, RTDS, microgrid, inverter, or hardware validation. State control cycle, sampling rate, grid code assumptions, and protection constraints.

## Method Structure Templates

Choose a template that matches the paper's real contribution. Keep section names venue-appropriate, but preserve the conceptual separation.

For robotics RL papers:

1. Problem Formulation
2. System Overview
3. Observation and State Design
4. Latent Representation or Estimator
5. Adaptation Module
6. Policy or Controller
7. Reward and Training Objective
8. Curriculum and Randomization
9. Safety, Stability, or Constraint Handling
10. Deployment Pipeline
11. Complexity and Runtime

For locomotion papers:

1. Robot Model and Assumptions
2. Command and Terrain Distribution
3. Observation History and Proprioception
4. Policy Architecture or Controller Interface
5. Reward, Termination, and Curriculum
6. Domain Randomization and Disturbances
7. Hardware Deployment
8. Failure Analysis and Recovery

For partially observable control papers:

1. POMDP or Output-Feedback Formulation
2. Observable Signals and Hidden Variables
3. Estimator, Belief, or History Encoder
4. Controller or Policy Synthesis
5. Stability, Robustness, or Safety Argument
6. Simulation and Real-World Validation
7. Complexity, Latency, and Implementation

Always separate observation, latent representation, adaptation, policy head, reward design, curriculum, and deployment pipeline. If two are combined, state why the coupling is necessary.

## Experimental Integrity Constraints

- Do not fabricate benchmark results, statistical significance, datasets, runtime numbers, hardware specs, citations, hyperparameters, ablation outcomes, or real-world deployment claims.
- Use TODO placeholders for unknown values: `TODO: insert baseline`, `TODO: report seed count`, `TODO: verify hardware`, or `TODO: confirm citation`.
- Weaken claims instead of inventing evidence. Use "suggests", "in this setting", or "under the tested conditions" when evidence is limited.
- Distinguish simulation, emulation, HIL, real hardware, and field deployment. Do not let simulation-only evidence imply real-world robustness.
- Do not claim real-time control without policy frequency, control loop frequency, latency, onboard hardware, and measurement method.
- Report number of seeds, variance or confidence intervals, episode counts, evaluation protocol, and failure criteria when experimental claims depend on stochastic learning.
- Treat missing baselines and weak ablations as strategic risks, not cosmetic gaps.

## Innovation Quality Constraints

- Avoid unnecessary module stacking, bag-of-tricks designs, random attention/transformer additions, and unjustified architectural complexity.
- Require causal justification for every module: what limitation it targets, what signal it uses, why it should help, and which ablation isolates it.
- Prefer mechanistic insight over architectural inflation. A simple estimator with a clear failure-mode argument is stronger than an unexplained large network.
- Discuss computational tradeoffs: parameter count, inference latency, memory, training cost, onboard compute, and control frequency where relevant.
- If a module is replaceable, describe it as one implementation of the idea rather than the idea itself.

## Drafting Rules

- Write in a precise technical voice: concrete nouns, active verbs where natural, and claims tied to evidence.
- Make the abstract self-contained: problem, gap, method, main quantitative result, and significance. Avoid citations, undefined acronyms, display equations, and hype.
- Make the introduction answer why the problem matters, what prior approaches miss, what this paper contributes, and how the evidence supports the contribution.
- Use contribution bullets only when the venue style allows them. Keep each contribution falsifiable and tied to a section, theorem, experiment, figure, table, or released artifact.
- Use present tense for general truths, paper structure, and figure/table descriptions: "Figure 2 illustrates..." and "Section III presents...".
- Use past tense for completed experimental procedures, data collection, model training, and hardware trials: "The model was trained for..." and "We collected data from...".
- Use IEEE citation style in prose: "Smith et al. [1]" or "prior work [1], [2]" rather than author-year phrasing.
- For double-blind review, cite the authors' own prior work in third person and avoid identity-revealing phrasing, repositories, acknowledgments, grants, facility names, or preprint overlap statements.
- For preprints, verify the venue's current policy before citing, uploading, or describing overlap. If allowed in double-blind review, refer to the preprint neutrally in third person.
- Reduce vocabulary repetition by rotating precise alternatives. Use `present`, `introduce`, `formulate`, `design`, or `develop` instead of repeating `propose`; use `address`, `tackle`, `mitigate`, `alleviate`, or `solve` according to the strength of the claim; use `demonstrate`, `show`, `validate`, or `evaluate` according to the evidence.
- Do not overclaim novelty, causality, superiority, or generality. Qualify claims by dataset, operating condition, assumptions, and statistical confidence.

## Anti-LLM Writing Constraints

- Avoid repetitive rhetorical templates such as "To address this issue", "Extensive experiments demonstrate", "In order to", "This paper proposes", and "The main contributions are summarized as follows".
- Vary paragraph rhythm naturally. Do not make every paragraph follow the same four-sentence arc or the same contrast-transition-result pattern.
- Keep the abstract less templated when possible. It should still cover problem, gap, method, and evidence, but not read like a rigid form.
- Use concrete technical phrasing over generic praise. Prefer "estimates terrain slope from proprioceptive history" over "effectively captures complex environmental features".
- Limit adjective inflation: "robust", "novel", "efficient", "comprehensive", and "state-of-the-art" require evidence or should be removed.
- Avoid excessive contribution bullets. Use bullets when they clarify the argument, not to inflate the paper.
- Allow moderate asymmetry in prose. Strong papers often spend more space on the hard idea and less on routine implementation.
- Replace over-smooth transitions with precise logical links: cause, limitation, evidence, assumption, or failure mode.

## LaTeX Rules

- Start from the current target-venue package when provided. If no venue package is available, use `assets/ieee-official-templates/bare_jrnl_new_sample4.tex` plus `IEEEtran.cls` for journal manuscripts, or convert the official IEEEtran class options carefully for conference work according to IEEE/venue instructions.
- Keep official template files under `assets/ieee-official-templates/` intact. When creating a user project, copy the needed `.tex`, `IEEEtran.cls`, bibliography/style resources if present, and sample figures into the user's project before editing.
- Use BibTeX with `\bibliographystyle{IEEEtran}` unless the venue explicitly requires another workflow.
- Keep figures, tables, equations, algorithms, and references in normal IEEE floating environments. Avoid manual placement hacks, margin changes, and font-size compression.
- Use nonbreaking spaces before citations, references, and units: `Fig.~\ref{fig:overview}`, `Table~\ref{tab:results}`, `Section~\ref{sec:method}`, `Algorithm~\ref{alg:main}`, `\cite{key}` when preceded by prose, `10~m`, and `3~V`.
- Distinguish hyphen, en dash, and em dash in LaTeX source: `-` for compound modifiers, `--` for numeric ranges such as `1--5`, and `---` for parenthetical breaks when allowed by style.
- Prefer vector graphics (`.pdf`, `.eps`) for plots and diagrams, and high-resolution `.png` or `.tif` only when raster output is appropriate.
- Place table captions above tables and figure captions below figures. Put `\label{...}` after `\caption{...}` so references resolve to the correct number.
- Use `booktabs`-style three-line tables when allowed: `\toprule`, `\midrule`, and `\bottomrule`. Do not use vertical grid lines in IEEE tables.
- Use `\IEEEeqnarray` or aligned math environments for long equations. Do not use screenshots of equations.
- In math environments, wrap descriptive text in `\text{...}` and keep non-English prose out of equations unless the venue explicitly allows it.
- Keep package additions conservative. Be suspicious of `geometry`, `fullpage`, `titlesec`, `caption`, `subcaption`, `setspace`, local `\fontsize`, and heavy class/style modifications in final submissions.

## BibTeX Clean-Up

Apply this protocol whenever creating, editing, or auditing `.bib` files:

1. Preserve citation keys unless the user asks to rename them; update all `\cite{...}` commands if a key must change.
2. Protect proper nouns, algorithm names, standards, software names, and acronyms with braces, preferably double braces for fragile terms: `{{Kalman}} filter`, `{{IEEE}}`, `{{LiDAR}}`, `{{ROS}}`, `{{SLAM}}`, `{{MIMO}}`, and `{{OFDM}}`.
3. Remove fields that usually pollute IEEEtran output or leak irrelevant metadata: `publisher`, `issn`, `isbn`, `url`, `doi`, `arxivId`, `archivePrefix`, `eprint`, `abstract`, `keywords`, `language`, `month`, and `note`, unless the venue explicitly requires them. For Early Access articles or preprints without assigned volume/pages, preserve `doi` or `arxivId` so the work remains legally and technically traceable.
4. Keep the minimal clean field set by entry type: authors, title, journal or booktitle, volume/number/pages or article number when available, and year.
5. Normalize IEEE venue names to official abbreviations. Examples: `IEEE Transactions on Robotics` -> `IEEE Trans. Robot.`, `IEEE Transactions on Automatic Control` -> `IEEE Trans. Automat. Control`, `IEEE Transactions on Signal Processing` -> `IEEE Trans. Signal Process.`, `IEEE Transactions on Wireless Communications` -> `IEEE Trans. Wireless Commun.`, and `IEEE Transactions on Power Systems` -> `IEEE Trans. Power Syst.`.
6. Check capitalization after cleanup by compiling or inspecting the generated `.bbl` when possible.

## Static Audit Engine

When source files are available, first verify source-file encoding before analysis, rewriting, or repair. Prefer standard UTF-8; if a legacy encoding such as GBK is detected or suspected, warn the user and avoid blind rewrites that could corrupt local source files. Then run `scripts/audit_ieee_latex.py <project-or-main.tex>`. When execution is unavailable, perform the same audit mentally and report findings by severity. The audit should intercept:

- IEEE structure risks: missing IEEEtran class, suspicious class options, missing abstract/keywords, missing IEEEtran bibliography style, unresolved citations, unmatched labels, missing graphics, discouraged graphics extensions, and float caption/label order errors.
- Source file encoding compliance: non-UTF-8 files, mixed encodings, BOM-related surprises, or decode fallbacks that could change characters during automated fixes.
- Double-blind risks: author names, affiliations, email addresses, acknowledgments, grant numbers, ORCID IDs, institutional repositories, self-identifying URLs, lab-specific equipment/software names, and first-person self-citations such as "our previous work [1]".
- Text encoding and punctuation risks: Chinese characters, Chinese commas/periods/parentheses, full-width punctuation, or multibyte source-region punctuation left in text or comments.
- Unit and numeric formatting risks: unescaped percentages such as `10%` instead of `10\%`, glued units such as `10m`, `3V`, or `180C`, and temperature formatting that should appear as `180$^\circ$C` or a venue-approved equivalent.
- Math hygiene risks: Chinese text or narrative English directly inside `equation`, `align`, `IEEEeqnarray`, `multline`, or similar environments unless wrapped in `\text{...}`.
- Cross-reference risks: missing nonbreaking spaces before `\ref`/`\cite`, labels placed before captions, duplicate labels, and unreferenced floats when detectable.
- Table risks: vertical grid lines, `\hline`-heavy tables, missing units in column headers, and tables that should use three-line `booktabs` style.
- Formatting-cheat risks: negative `\vspace`, manual margin edits, local font shrinking, `\resizebox` abuse for dense tables, and packages that override IEEE spacing or captions.
- BibTeX risks: dirty exported fields, unprotected capitalization, missing citation keys, nonstandard IEEE venue names, and entries that include URL/arXiv metadata when the venue does not require it.

Return audit results with concrete file/line locations when possible, then propose minimal source-preserving fixes.

## Response Letter Workflow

For major or minor revisions:

1. Preserve reviewer numbering and quote or summarize each comment accurately.
2. Under every item, generate `Reviewer's Comment`, `Response`, and `Changes in the Revised Manuscript`.
3. Use a polite and respectful tone. Acknowledge valid concerns, avoid defensiveness, and support disagreements with evidence.
4. Map every claimed change to a section, page, paragraph, figure, table, equation, or appendix.
5. If the venue permits highlighted changes, recommend `\textcolor{blue}{...}` or the venue-specified marking convention in the revised manuscript. Remove markings for camera-ready submission if required.
6. When a requested change is impossible, explain the constraint and add a clarifying limitation or discussion note in the manuscript.

## Submission Checks

Before calling a paper ready:

1. Compile from a clean checkout with the expected engine.
2. Check that references resolve, citation keys exist, figures are included, and the PDF has no important overfull boxes.
3. Run IEEE's official LaTeX Analyzer, Reference Preparation Assistant, and PDF Checker when preparing an actual IEEE submission.
4. Confirm page limit, anonymity requirements, preprint policy, funding/acknowledgment placement, supplementary-material rules, copyright, ORCID, and final-file packaging.
5. For double-blind review, verify that identity leaks are removed from source, PDF metadata, figure files, supplementary files, comments, filenames, and repository links.
6. State remaining risks clearly if only a static audit was possible.
