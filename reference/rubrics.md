# BEHAVIORAL + CODING RUBRICS, probing banks, and PLAN structure

System design has a single canonical HTML model answer (`reference/system-design-model-answer.html`);
`reference/system-design-model-answer.md` is maintenance source text. Behavioral and coding have no one
canonical answer, so Grade compares against the rubric's "what good looks like" rather than a verbatim
mirror.

---

# BEHAVIORAL (STAR) - 6-dimension rubric

Behavioral interviews test whether the candidate can tell a structured, specific, self-aware story
about real work. STAR (Situation, Task, Action, Result) is the spine; the rubric grades the substance.

## Scoring (per dimension, 0-2; bar calibrated to level at Frame)

1. **Structure (STAR)** - Clear Situation -> Task -> Action -> Result. The listener never loses the
   thread. Did they OWN the story, or ramble?
2. **Specificity** - Concrete, not generic. Use anonymized roles, numbers, constraints, and outcomes;
   avoid real names, confidential client names, or private coworker details. "Led 4 people over 6 weeks
   to cut p99 from 800ms to 200ms" beats "improved performance."
3. **"I" vs "we"** - Actions attributed to the candidate personally. "We shipped" is a flag; "I decided
   to X, which let the team Y" is the bar. Probe: "what was YOUR specific contribution?"
4. **Conflict / ambiguity handled** - Did they show how they navigated disagreement, unclear
   requirements, or a failing situation? This is what the question is actually testing.
5. **Result + reflection** - Quantified outcome AND a genuine lesson/what-they'd-do-differently. A
   story with no result is incomplete; a story with no reflection shows no growth.
6. **Signal-to-noise / time** - 2-3 min, dense, on-point. No preamble, no tangent. Did they manage the
   clock?

## Probing bank (Behavioral)

- "What was YOUR specific role on that - walk me through what you personally did on Tuesday."
- "You said 'we decided' - who actually made the call, and what was your input?"
- "What was the hardest disagreement, and how did you resolve it?"
- "If you re-did it today, what would you change?"
- "What did this cost you? What did you have to give up?"

## Grade output format (Behavioral)

```
BEHAVIORAL grade  -  <total>/12  (bar: <level>)
1 Structure (STAR)                 <0-2>  <one-line evidence>
2 Specificity                      <0-2>  <evidence>
3 "I" vs "we"                      <0-2>  <evidence>
4 Conflict / ambiguity handled     <0-2>  <evidence>
5 Result + reflection              <0-2>  <evidence>
6 Signal-to-noise / time           <0-2>  <evidence>

FIRST gap: <dimension> - <what was thin> -> <concrete one-line fix>
Re-drill target: <dimension> with a novel behavioral prompt: <the new prompt>
```

## Common behavioral prompts

- Tell me about a time you had a conflict with a teammate.
- Tell me about a project that failed. What happened?
- Tell me about a time you had to influence without authority.
- Tell me about your biggest mistake.
- Tell me about a time you pushed back on a deadline or scope.

---

# CODING (algorithm) - 6-dimension rubric

Coding interviews test problem-solving process + correct code + communication. The rubric grades the
whole arc, not just "does it compile."

For approach coaching, weak-dimension diagnosis, and re-drill design, use
`reference/coding-pattern-recognition.md`. During a live mock, do not reveal the full pattern guide
before the user attempts the problem; use it to choose one interviewer-style nudge if the user stalls,
then use it fully at Grade.

## Scoring (per dimension, 0-2)

1. **Clarify before coding** - Restated the problem, asked about edge cases, input constraints,
   expected output, empty/duplicate/large-input behavior. Did NOT jump to typing.
2. **Approach / approach-tradeoff** - Named a strategy, discussed brute force -> optimized, stated
   time/space complexity BEFORE coding, and picked the structure for a reason.
3. **Correctness** - Logic handles the happy path AND edges (empty, single, boundary, overflow). The
   core algorithm is right even if a syntax slip remains.
4. **Code quality** - Readable, named variables, decomposed when it helps, no dead code. Production-ish,
   not a scratch mess.
5. **Testing / verification** - Traced the code on at least one normal + one edge input by hand, caught
   a bug from the trace, fixed it. Did not declare done without tracing.
6. **Communication & pace** - Thought process narrated, receptive to hints, asked clarifying questions
   mid-code when stuck, managed time.

## Probing bank (Coding)

- "What is the time and space complexity of your solution? Can you do better?"
- "Walk me through your code with this input: [edge case]."
- "What happens if the input is empty / huge / all duplicates?"
- "You assumed X - is that always true?"
- "Brute force first - then optimize. Why this data structure?"

## Grade output format (Coding)

```
CODING grade  -  <total>/12  (bar: <level>)
1 Clarify before coding            <0-2>  <one-line evidence>
2 Approach / tradeoff              <0-2>  <evidence>
3 Correctness                      <0-2>  <evidence>
4 Code quality                     <0-2>  <evidence>
5 Testing / verification           <0-2>  <evidence>
6 Communication & pace             <0-2>  <evidence>

FIRST gap: <dimension> - <what was thin> -> <concrete one-line fix>
Re-drill target: <dimension> with a novel coding problem or constraint: <the new prompt>
```

---

# PLAN mode - build a time-boxed prep plan

When the user asks for a study/prep plan rather than a mock, build a time-boxed plan. Do not write an
interview answer or model solution for them; write the schedule and drills that make them perform.
Structure:

1. **Target.** Role/level, company tier, interview mix (system design %, behavioral %, coding %),
   timeline (e.g. "4 weeks", "weekend crash").
2. **Gap assessment.** Run ONE quick diagnostic per interview type (a single framed question, 5 min)
   to find the weakest dimensions - do not assume. Map results to the rubric dimensions.
3. **Schedule.** Weight time toward the weakest dimensions. Spaced practice: system-design full mocks
   on a cadence (not stacked), behavioral story bank built once then refined, coding daily short sets.
4. **Mock cadence.** Full timed mocks increasing in frequency toward the date; each mock followed by a
   Grade + a Re-drill on the weakest dimension.
5. **Output.** A dated plan with weekly milestones and the specific rubric dimensions to lift, kept
   short - the plan structures the user's own work, it does not do the work.

Re-drill and spaced-retrieval beat cramming: the user performs, gets graded, rests, then performs a
novel variant. Massed re-reading of model answers is explicitly NOT the method here.
