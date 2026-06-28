# MOCK-LOOP - the default loop for SYSTEM-DESIGN / BEHAVIORAL / CODING / MOCK

The disciplined form of the mock interview: the user performs the full answer under realistic time,
then an independent grader scores it against a rubric, then a novel variant re-drills the weakest
dimension. The one move that beats re-reading model answers is performing under pressure, getting a
rubric-anchored critique, then proving transfer on a fresh problem.

Use for any live practice round. Skip for GRADE (user already has an answer to score), PLAN, and
TEACH-CONCEPT - those do not run a simulation.

## The perform-first / reveal-after contract

The model answer (`reference/system-design-model-answer.html` for SYSTEM-DESIGN) is GROUND TRUTH, not an
opening handout. Reveal it ONLY at Grade, after the user has performed their own full answer, as a
polished standalone HTML page. Reading it first turns practice into recognition and breeds the illusion
of knowing - the exact failure mode this skill exists to prevent. If the user asks to "see how it's done"
before attempting, refuse and explain why: attempt first, compare after. The only exception is
TEACH-CONCEPT, which is not a mock. For a novel question with no stored HTML answer, GENERATE one fresh
at Grade from `templates/model-answer.html`. If file writes are allowed, save it as
`superinterview-model-answer-<slug>.html` in the current workspace; otherwise return a fenced `html`
block or a concise rendered summary. Model answers are always delivered as HTML, never as raw markdown.

## Roles (each role = a fresh-context subagent by default)

Dispatch is the default when subagents are available: the conductor runs each role as a separate
fresh-context subagent so the role's references load inside the subagent and never accumulate in the
conductor's window. The subagent returns only a short structured result - the posed question, the
scorecard, the gap, the re-drill - not its transcript. A single quick GRADE of one short answer runs
inline. If subagents are unavailable, run inline by phase: load only the phase reference, summarize the
handoff state, then continue. Full personas: `agents/interviewer.md`, `agents/critic.md`.

1. **Interviewer** (`agents/interviewer.md`) - poses the question as a real interviewer would (terse,
   one prompt, no structure hints), then runs Probe. Owns Pose + Probe.
2. **Critic** (`agents/critic.md`) - independent of the performer. Scores dimension-by-dimension against
   the rubric, names the FIRST gap with a concrete fix, reveals the model answer, designs the novel
   re-drill variant. Owns Grade + Re-drill design. Does NOT feed hints during Pose/Respond.

## Loop steps

1. **Frame.** Restate in one line: interview type, target level (junior / mid / senior / staff),
   company tier if known, specific topic or question, time budget (~45 min system design, 30-45
   behavioral/coding). If the request is underspecified, ask <=3 high-leverage questions only:
   - Which interview type? (system design / behavioral / coding)
   - What level and (optionally) company tier? - sets the rubric's depth bar
   - A specific topic/question, or should the interviewer pick one?
   State the rubric you will grade against. Do NOT show the model answer.

2. **Pose.** The interviewer presents ONE question, the way a real interviewer does: terse, realistic,
   no hints, no structural reveal, no "you might want to start with requirements." Start the clock.
   Announce the time budget. Then stop and wait.

3. **Respond.** The user answers (typing their design / telling their story / writing code). The
   interviewer waits - the user drives. If the user stalls or asks "where do I start?", give ONE nudge
   an interviewer would give ("what would you want to clarify before designing?", "talk me through a
   single request"), never the answer or the structure. Track time; call pacing only at phase boundaries.

4. **Probe.** Ask 1-3 follow-ups from the rubric's probing bank that target the answer's WEAKEST
   dimension - never to confirm strengths. Push a tradeoff, demand a failure path, ask for scale math,
   request a deep dive on the hot component. Real interviewers probe depth, not breadth.

5. **Grade.** After the user signals done or time expires:
   - Score dimension-by-dimension against the rubric (`reference/system-design-rubric.md` for
     SYSTEM-DESIGN; `reference/rubrics.md` otherwise), at the target level's depth bar.
   - Report the scorecard, then name the SINGLE highest-leverage gap with a concrete one-line fix.
   - THEN reveal the model answer as a polished standalone HTML page for self-comparison (SYSTEM-DESIGN
     only; other modes have no single canonical answer, so compare against the rubric's "what good looks
     like" instead). For a novel question with no stored answer, generate a fresh HTML model answer from
     `templates/model-answer.html` at this point. If file writes are allowed, save it as
     `superinterview-model-answer-<slug>.html` in the current workspace.
   - The critic persona supplies the gap detection the performer's self-review systematically misses.

6. **Re-drill.** Pose a NOVEL variant that re-tests the weakest dimension under the same rubric:
   different system (SYSTEM-DESIGN), different story (BEHAVIORAL), different problem (CODING). Confirm
   TRANSFER, not recall - the user must clear the dimension unprompted on a prompt they have not seen.
   Stop when it clears. If it fails again, that dimension becomes the focus of the next session's PLAN.

## Guardrails (keep it perform-first, not recognition-theater)

- **Never reveal before attempt.** The whole value is in the generation effect. A pre-reveal "study"
  session is a different mode (TEACH-CONCEPT via supertutor) - do not blur the two.
- **Grade structure and depth, not verbatim match.** Many valid designs exist; the model answer is one
  strong example, not the only answer. A different-but-defensible architecture scores a 2.
- **The critic is independent of the performer.** The performer cannot grade their own gaps reliably -
  self-review confirms strengths and misses the thin spots. The critic re-reads the rubric fresh.
- **Re-drill on a NOVEL variant, every time.** Re-answering the same prompt tests memory, not skill.
  If you cannot think of a novel variant, change the domain (food delivery -> ride sharing -> chat) and
  keep the dimension under test constant.
- **Cap Probe at 3 follow-ups.** More turns a mock into a tutorial; the point is to test, not teach
  mid-flight. Save teaching for Grade.
- **Calibrate honestly.** Do not inflate the score to encourage. A false "you're ready" is the worst
  outcome - it sends the user into a real interview unprepared. Name gaps plainly; that is the help.
- **Separate session completion from mastery.** A session can complete after Grade and a re-drill prompt;
  mastery is confirmed only when the user clears the re-drill unprompted.
