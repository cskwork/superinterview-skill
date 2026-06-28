# superinterview

**Landing page: https://cskwork.github.io/superinterview-skill/**

Interview preparation skill for coding-agent assistants. Mock interviews with rubric-graded feedback
and targeted re-drill. System design is the flagship (graded against a full model answer); behavioral
(STAR) and coding (algorithm) are included.

## The one rule

**Perform first, compare second.** The user attempts the full answer under realistic time before the
model answer is revealed. Reading the model answer first collapses practice into a recognition illusion.
The model answer is the grading ground truth and the self-comparison mirror - never the opening handout.

## How it works

```
Frame -> Pose -> Respond -> Probe -> Grade -> Re-drill
```

- **Frame** - interview type, target level, company tier, time budget.
- **Pose** - the interviewer (terse, one prompt, no hints) starts the clock.
- **Respond** - the user drives the answer; the interviewer waits.
- **Probe** - 1-3 follow-ups targeting the answer's weakest dimension.
- **Grade** - dimension-by-dimension scorecard against a fixed rubric, then the FIRST gap named with a
  concrete fix, then the model answer revealed for self-comparison.
- **Re-drill** - a NOVEL variant re-tests the weakest dimension to confirm transfer, not recall.

## Modes

| Mode | Use for |
|---|---|
| SYSTEM-DESIGN | design X, scalable platform (flagship; has a model answer) |
| BEHAVIORAL | STAR stories, conflict, leadership |
| CODING | algorithm / data-structure problems |
| MOCK | full timed simulation |
| GRADE | score an answer the user already gave |
| PLAN | build a time-boxed prep plan |
| TEACH-CONCEPT | explain a concept (routes to supertutor) |

## Structure

```
SKILL.md                              router - mode table + default loop + reference map
reference/
  mock-loop.md                        the perform-first / reveal-after loop contract
  system-design-rubric.md             10-dimension grading rubric + probing bank
  system-design-model-answer.html     SYSTEM-DESIGN ground truth (polished HTML; reveal at Grade)
  system-design-model-answer.md       ground-truth source text (verbatim)
  rubrics.md                          BEHAVIORAL (STAR) + CODING rubrics, PLAN
agents/
  interviewer.md                      terse probing interviewer persona
  critic.md                           independent rubric grader + re-drill designer
templates/
  model-answer.html                   reusable HTML shell for any system-design model answer
examples/
  twitter-news-feed.html              a generated HTML model answer (novel question)
```

## Model answers are HTML

Every system-design model answer is delivered as a polished standalone HTML page (self-contained,
inline CSS, no external deps), revealed at Grade for self-comparison. For a stored canonical answer
the HTML already exists (`reference/system-design-model-answer.html`); for a novel question the
critic generates a fresh one at Grade from `templates/model-answer.html`. Answers are never handed
out as raw markdown or before the user has performed their own full answer.

## Checks

Run the local contract check before publishing skill changes:

```bash
python3 scripts/validate_skill.py
```

The check covers frontmatter shape, referenced resource paths, the HTML reveal contract,
behavioral/coding grade templates, eval schema, and self-contained model-answer HTML artifacts.
GitHub Actions runs the same command on pushes and pull requests.

## Why perform-first

The generation effect and the testing effect: information the learner *produces* is encoded far more
durably than information they re-read. A mock where the user answers under pressure, gets a specific
rubric critique, then compares against a strong example - and is re-tested on a fresh problem - builds
transferable structure. A mock where they read the answer first builds the illusion of knowing.

## License

MIT
