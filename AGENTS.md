@docs/project.md

# Harness

## Research working method

This is the core principle that governs every session. Read it first.

**Nothing technical is predetermined.** The approved proposal is a compass: it fixes the scope, the pollutants, the geographic region, and the DSR framing. It does not fix the models, the validation protocol, the optimization method, or any other technical choice. Those are open questions that the research process earns the right to answer.

**The research progression is the plan.** Every technical choice must be earned in order:
1. Problem grounding (§1): establish the real-world problem precisely; name the gap; state the claim in general terms
2. Literature review (§2): survey what exists; what has been tried; what those attempts reveal about which methods are appropriate
3. Research design (§3): choose and argue methodology based on what phases 1-2 established; only here do technical choices get made
4. Data feasibility: confirm the chosen methodology is actually possible with the available data
5. Implementation: execute what phases 1-3 specified

**Do not suggest or commit to any technical choice before the phase that earns it.** If a model name, algorithm, or validation protocol appears before Phase 3, that is a signal something has been assumed rather than argued. Challenge it.

**The proposal is not an answer; it is a starting hypothesis.** When the literature review in Phase 2 reveals that a different method is more appropriate, the thesis must follow the evidence. Document the divergence and justify the change.

**Guide the user through the progression, not toward a predetermined destination.** The job is to ask the right question at each phase, not to confirm what the proposal already says.

## Writing standards

These rules apply whenever generating or editing text in `writing/thesis.tex`. They are not stylistic preferences: they are structural and methodological requirements.

**Register and voice**

The thesis must be written in formal academic prose consistent with master's-level research. Specifically:

- Use the third person and passive constructions where appropriate: "this study investigates", "the results indicate", not "I show" or "we prove"
- Do not use contractions, colloquial expressions, or informal hedges
- Claims must be hedged in proportion to the evidence: "the findings suggest", "this is consistent with", "one interpretation is" -- do not write "this proves" or "this demonstrates" for empirical results
- Sentences should be precise and economical: one idea per sentence where possible; subordinate clauses only when they carry necessary qualification

**Section roles: enforced constraints**

Each section of the thesis has a defined argumentative role. These roles are not interchangeable:

- §1 (Introduction): establishes the real-world problem, names the monitoring gap, and states the research aim in general terms. No model names, algorithm names, or validation protocol names belong in §1. Those are arguments for §3.
- §2 (Background and Related Work): surveys the existing literature across all relevant streams and identifies what that literature leaves unresolved. §2 describes the landscape: it does not commit to any method for this thesis. It ends with a gap statement, not a solution.
- §3 (Research Methodology): the only section that may name and argue specific technical choices (models, validation protocol, optimization approach). All choices must be argued from the literature established in §2: none assumed, none imported from the proposal without justification.

If a specific model name, validation protocol, or optimization algorithm appears in §1 or §2, that is a structural error. Flag it and move the commitment to §3.

**Unverified citations**

- Any citation whose author list, year, or title has not been confirmed against the original source must carry a `% VERIFY` comment immediately after the `\cite{}` command in the LaTeX source
- Unverified citations must not remain in the version submitted for examination
- Use only bib keys that exist in `writing/references.bib`; do not invent keys or cite from memory

## Session rules

- Read this file before starting any session
- Update `docs/next.md` at end of every session: where things stand, next step, open threads, decisions made
- Update `docs/roadmap.md` phase status whenever a phase is completed or its status changes
- Never delete or overwrite core project documents without explicit instruction

## Roadmap (agentkan)

Live task tracking now lives on the agentkan board, not in new prose appended to
`docs/next.md` / `docs/roadmap.md`. Those two files are kept as the historical record
of Phases 0-7 (all done) and are not deleted, but going forward, board state is the
source of truth for what's open.

Board directory: `docs/board/`. State lives in JSON (`roadmap.json`, `next.json`);
prose detail lives in `docs/board/epics/<ID>.md`.

**Start:** read `docs/board/next.json` and skim the active epics (`P8`) in
`docs/board/roadmap.json`.

**Board work:** follow the installed `agentkan` skill. After edits: `npx agentkan validate docs/board`.

**End (handoff):** run agentkan handoff — status snapshot, update the board, validate,
optionally log to `docs/sessions/`.

**Human owns:** dragging epics to Done and archiving in the viewer (`npx agentkan serve docs/board`).

**New epic stub:** `npx agentkan epic new "<title>" [--phase Pn]`, then fill goal, exit, tasks, and `docs/board/epics/<ID>.md`.

## Key files

| Path | Purpose |
|---|---|
| `docs/board/` | agentkan roadmap board — live task state (`roadmap.json`, `next.json`, `epics/`) |
| `writing/proposal.md` | Approved research proposal (anchor document) |
| `writing/thesis.tex` | Thesis LaTeX (skeleton; sections are TODO stubs) |
| `writing/thesis-structure.md` | MAU structure and formatting rules |
| `writing/references.bib` | Bibliography (seeded from proposal; expand in Phase 2) |
| `writing/images/` | Generated figures (add logo before first compile) |
| `docs/roadmap.md` | Phase tracking (Phases 0--8) |
| `docs/next.md` | Session handoff |
| `docs/project.md` | Thesis identity, RQs, data sources, risks |
| `Taskfile.yml` | Runnable commands (`task --list`) |

## Load on demand

| File | Load when |
|---|---|
| `agents/council.md` | Council triggers only (see below) |
| `agents/povs/the-skeptic.md` | Council invocation only |
| `agents/povs/the-editor.md` | Council invocation only |
| `agents/povs/the-researcher.md` | Council invocation only |
| `agents/povs/the-domain-expert.md` | Council invocation only |
| `agents/templates/decision-packet.md` | Preparing a council session |
| `docs/roadmap.md` | Checking phase status or planning next milestone |
| `writing/thesis-structure.md` | Before any edit to `writing/thesis.tex`: load this first. It contains the MAU formatting rules (margins, line spacing, bibliography style, figure and table conventions). Do not edit the thesis without loading it. |

## Council (opt-in only)

Not loaded by default. Invoke when a trigger applies or when selected explicitly. Load `agents/council.md` then the four POV seats in protocol order.

**Triggers:**
- Irreversible actions; autonomous scope expansion; external integrations or new dependencies
- Significant time or cost commitment with unclear return
- Committing to any methodological choice (model selection, validation protocol, optimization approach)
- Finalizing any section whose claim the rest of the thesis depends on (§1 problem statement, §2 identified gap, §3 methodology)
- Any decision that would change what phases 4-7 are required to do

## Hard rules

- Do not push to remote or publish without explicit instruction
- Do not modify files outside this repo directory
- Ask before taking any irreversible action
- **Never use em dashes anywhere:** not in thesis prose, slides, or generated text. Use commas, colons, parentheses, or semicolons instead. No exceptions.
