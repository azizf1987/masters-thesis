# Council

The council is a structured deliberation protocol for non-trivial decisions. Four seats, each holding a distinct lens. Not a vote: a pressure test.

## Primary tension

This thesis must defend a linked chain of claims, but the chain is built through the research, not assumed from the proposal. At any given decision point, the council holds this tension: is the claim being made supported by what the research has actually established so far, or is it being borrowed from a proposal that has not yet been argued? The council pushes every argument to be as strong as the evidence actually permits, and no stronger. It also pushes every technical choice to be argued, not assumed.

## When to invoke

- An irreversible action: publishing, deleting, deprecating, pushing to remote
- Autonomous scope expansion beyond the current task
- External integrations or new dependencies
- Significant time or cost commitment with unclear return
- Committing to any methodological choice before the phase that earns it (model selection, validation protocol, optimization approach)
- Finalizing any section whose claim the rest of the thesis depends on (§1 problem statement, §2 identified gap, §3 methodology design)
- Any decision that would change what phases 4-7 are required to do

## Active seats

| Seat | File | Role |
|---|---|---|
| **The Skeptic** | `agents/povs/the-skeptic.md` | Challenges the premise; tests whether claims are earned or assumed |
| **The Editor** | `agents/povs/the-editor.md` | Guards coherence; cuts accumulation and premature commitment |
| **The Researcher** | `agents/povs/the-researcher.md` | Protects research integrity and contribution clarity |
| **The Domain Expert** | `agents/povs/the-domain-expert.md` | Checks accuracy within spatial science, air quality, and DSR methodology |

## Protocol

1. State the decision in one sentence
2. Load `agents/templates/decision-packet.md` and fill it in
3. Run each seat in order: Skeptic → Editor → Researcher → Domain Expert. Before each seat deliberates, provide it with the verdicts and key findings from all preceding seats so later seats can respond to what has already been raised.
4. Each seat returns its verdict and findings
5. Claude (orchestrator) writes the Synthesis section of the decision packet: map all four verdicts to the combined signal below, state the decision, and name any conditions that must be met before proceeding
6. Proceed only if no seat returns Block

## Guardrails

- All writes stay within this repo directory
- No publishing, pushing to remote, or tagging releases without human confirmation
- If two or more seats return Block, stop immediately and surface the conflict to the human before any further action

## Verdict mapping

| Combined signal | Action |
|---|---|
| All Proceed | Build |
| One or more Pause, no Reframe or Block | Address each pause before building |
| Any Reframe | Stop, restate the decision, re-run the full council |
| Any Block | Escalate to human before proceeding |
