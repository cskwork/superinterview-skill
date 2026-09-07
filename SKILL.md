---
name: superinterview
description: Run mock interviews, grade answers against rubrics, plan preparation, and re-drill weak areas in system design, behavioral, or coding interviews. Also fill recruiting forms from source-backed resume facts, stopping before final submission.
---

# /superinterview - perform first, grade against ground truth

One interview target -> the user performs the full answer under realistic constraints ->
rubric-grade against a model answer -> re-drill the weakest dimension on a novel variant. A quick
fact the user just wants stated: answer it plainly and skip this skill. This file is a router; each
phase loads only the reference it needs.

## Private candidate context (optional, local only)

Before Frame, check whether `private/resume.md` exists in this skill checkout. If it exists, read it
as private candidate context and use it to personalize behavioral prompts, resume deep-dives, and
system-design follow-ups around the candidate's real projects. Keep it local: never commit, quote,
or expose contact details from the private file unless the user explicitly asks.

## Core principles

- **Perform first, compare second.** The user attempts the complete answer before the model answer is
  revealed. Reading the model first collapses the generation effect into a recognition illusion. The
  model answer is the grading ground truth and the self-comparison mirror - never the opening handout.
  Reveal it only at Grade, and only for the mode the user attempted.
- **Be the interviewer, not the teacher.** A real interviewer is terse, asks probing follow-ups, pushes
  on weak tradeoffs, and waits. Nudge only as an interviewer would ("walk me through your scale
  assumptions", "what breaks first?"). Teaching lives in the Grade, after the attempt.
- **Grade against a fixed rubric; name the FIRST gap.** Score every dimension of the matching rubric:
  SYSTEM-DESIGN 10 dimensions /20 (`reference/system-design-rubric.md`); BEHAVIORAL and CODING
  6 dimensions /12 (`reference/rubrics.md`). Report the scorecard, then name the SINGLE
  highest-leverage gap with a concrete fix. Never "good job."
- **Match the bar to the target.** Junior: correct structure + basic scale. Senior: deep tradeoffs +
  failure handling. Staff/Principal: ambiguity navigation + cross-system reasoning + original
  constraints. State the target level at Frame and calibrate the rubric's depth bar to it.
- **Drive time like a real interview.** ~45 min for system design, 30-45 for behavioral, 30-45 for
  coding. Call out pacing failures ("20 min in, no data model yet"). Time pressure is part of what is
  being practiced.
- **Output language:** prose in the user's language, idiomatic and natural; keep identifiers, file
  paths, commands, rubric dimension names, and machine-checked anchors in canonical English so checks
  keep matching. No emoji; CommonMark blank-line spacing.

## Mode (classify the request, state it in one line)

| Signal in the objective | Mode | Route |
|---|---|---|
| design X / system design / design a platform / scalable / 설계 | SYSTEM-DESIGN | mock loop + `reference/system-design-rubric.md`; stored food-delivery ground truth = `reference/system-design-model-answer.html`; novel prompts generate fresh HTML at Grade from `templates/model-answer.html` |
| behavioral / tell me about a time / STAR / conflict / leadership | BEHAVIORAL | mock loop + `reference/rubrics.md` (STAR) |
| coding / algorithm / data structure / leetcode / implement | CODING | mock loop + `reference/rubrics.md` (coding); use `reference/coding-pattern-recognition.md` for approach coaching, grading gaps, and re-drill design |
| mock / simulate / practice round / 모의 면접 | MOCK | full timed simulation; infer type or ask once |
| grade / review my answer / 채점 / 피드백 | GRADE | skip Pose; score an answer the user already gave against the matching rubric + model answer |
| study plan / prep roadmap / what to study | PLAN | build a time-boxed prep plan (`reference/rubrics.md`) |
| auto-fill resume form / job application / application profile / Amazon.jobs / Workday / LinkedIn application | RESUME-FORM | read private candidate context, inspect the form, fill mapped fields, ask for missing or sensitive facts, and stop before final submit |
| explain this concept for an interview (no mock) | TEACH-CONCEPT | route the concept explanation to supertutor; do not run the mock loop |

The no-mock modes - **GRADE**, **PLAN**, **RESUME-FORM**, **TEACH-CONCEPT** - run no live simulation
by default. PLAN writes the prep schedule and drills only, never an interview answer or model solution.

When delegating to `agents/critic.md`, pass the selected mode, interview type, target level, user's requested deliverable, and supplied answer. Standalone GRADE does not require a new attempt or re-drill; include a model comparison only within the requested grading scope.

## Resume form autofill (RESUME-FORM)

Use this when the user asks to fill a job application, resume form, candidate profile, or recruiting
site. The real-world task is data transfer: map private resume facts to employer fields accurately,
not to coach or improve the resume mid-flow.

1. Read `private/resume.md` if it exists. If it is missing, ask for a local resume file or minimal
   candidate facts before filling.
2. Inspect the form before writing. Build a field map from visible labels, placeholders, selected
   options, and validation messages to resume facts.
3. Fill only fields supported by the resume or the user's explicit instructions. Do not guess legal
   eligibility, sponsorship, demographic, disability, veteran, compensation, start-date, password, OTP,
   or CAPTCHA answers.
4. If the user named a target site and asked to fill it, entering ordinary resume/contact/career facts
   into that site is within the request. Still stop before final submission, file upload, account
   creation, password login, or any legally sensitive self-identification unless the user explicitly
   confirms that action.
5. When a required field is missing or ambiguous, leave it blank and report the exact missing item
   instead of fabricating.
6. Before handing back, summarize filled sections, blockers, and whether the page is waiting on user
   review, login, CAPTCHA, upload, or final submit.

## Default loop (SYSTEM-DESIGN / BEHAVIORAL / CODING / MOCK)

Keep the live interviewer inline. Use a fresh critic at Grade when independent gap detection adds value; a quick GRADE of one short answer runs inline. If subagents are unavailable, switch roles by phase and re-read the answer against the rubric. Load only the current phase reference. Full contract: `reference/mock-loop.md`.

1. **Frame.** Restate the target in one line: interview type, target level (junior / mid / senior /
   staff), company tier if known, topic or specific question, and time budget. If private candidate
   context is loaded, mention only that resume context will inform the prompts; do not summarize
   private details up front. If underspecified, ask <=3 high-leverage questions
   (`reference/mock-loop.md`). State the rubric you will grade against.
2. **Pose.** Present the question the way a real interviewer does - terse, one prompt, no hints, no
   structure reveal. Do NOT show the model answer. Start the clock.
3. **Respond.** The user answers; the interviewer waits. The user drives the structure. If the user
   stalls or goes silent, give ONE nudge an interviewer would give - never the answer.
4. **Probe.** Ask 1-3 follow-ups that target the answer's weakest dimension: push a tradeoff, request a
   failure path, ask for scale math, demand a deep dive. This is where depth is tested.
5. **Grade.** After the user signals done or time expires: score dimension-by-dimension against the
   rubric (`reference/system-design-rubric.md` / `reference/rubrics.md`), name the FIRST gap with a
   concrete fix, THEN reveal the model answer as a polished standalone HTML page for self-comparison.
   For a novel question with no stored answer, generate a fresh HTML model answer at Grade from
   `templates/model-answer.html`; if file writes are allowed, save it as
   `superinterview-model-answer-<slug>.html` in the current workspace. The independent critic persona
   (`agents/critic.md`) supplies the gap detection the performer's self-review misses.
6. **Re-drill.** Pose a NOVEL variant that re-tests the weakest dimension (different system / question
   / constraint). Confirm transfer, not recall. Stop when the dimension clears unprompted.

## Reference map (load only what the current phase needs)

| Read this | When |
|---|---|
| `reference/mock-loop.md` | default loop + the perform-first / reveal-after contract |
| `agents/interviewer.md` | Pose + Probe: the terse, probing interviewer persona |
| `agents/critic.md` | Grade: rubric scorer + gap finder (independent of the performer) |
| `reference/system-design-rubric.md` | SYSTEM-DESIGN: 10-dimension grading rubric + probing-question bank |
| `reference/system-design-model-answer.html` | SYSTEM-DESIGN ground truth (polished HTML) - reveal only at Grade |
| `reference/system-design-model-answer.md` | SYSTEM-DESIGN source text for maintenance; do not reveal instead of HTML |
| `templates/model-answer.html` | reusable HTML shell for generating any system-design model answer |
| `examples/twitter-news-feed.html` | check the filled-in shape before generating a novel model answer from the template |
| `reference/rubrics.md` | BEHAVIORAL (STAR) + CODING rubrics, probing banks, and PLAN structure |
| `reference/coding-pattern-recognition.md` | CODING: pattern recognition by asking what the problem asks the candidate to track |

**Mock session complete =** mode stated; user performed the full answer under realistic time before any
reveal; dimension-scored against the matching rubric; FIRST gap named with a concrete fix; model
answer revealed or offered as a polished standalone HTML page for self-comparison; weakest dimension
re-drill posed on a novel variant.

No-mock modes finish at their own deliverable: GRADE returns a scorecard and first gap; PLAN returns the schedule; RESUME-FORM returns the filled draft and remaining blockers before submission; TEACH-CONCEPT hands off the explanation. Do not require a mock attempt for these modes.

**Mastery confirmed =** the re-drill clears unprompted on the novel variant.
