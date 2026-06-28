# Changelog - 2026-06-28

## superinterview skill contract audit

- Aligned the model-answer reveal contract on HTML. `SKILL.md` and `reference/mock-loop.md` already
  required polished standalone HTML, but `agents/critic.md` still routed to the Markdown source. The
  critic now reveals `reference/system-design-model-answer.html` and uses `templates/model-answer.html`
  for novel questions.
- Added an inline fallback for runtimes without fresh-context subagents. Keeping subagents as the best
  path preserves context hygiene, while the fallback prevents the skill from failing in simpler agents.
- Split session completion from mastery confirmation. Users can stop after Grade, but mastery is only
  proven after clearing the novel re-drill unprompted.
- Tightened behavioral privacy. The rubric now asks for anonymized specifics rather than real names or
  confidential client/coworker details.
- Added explicit behavioral and coding grade formats so every interview mode has a testable output
  skeleton, not only system design.
- Added `scripts/validate_skill.py` and `evals/evals.json` so maintainers can check frontmatter,
  resource links, reveal contract consistency, eval shape, and self-contained HTML artifacts locally.
- Fixed an unescaped ampersand in the food-delivery model-answer title and made the validator catch raw
  ampersands plus unresolved local HTML anchors.
- Added a GitHub Actions workflow that runs the same validator on pushes and pull requests.

## Alternatives rejected

- Did not add a package manager or browser automation harness. The repo has no runtime, so a
  dependency-free Python validation script plus a small CI wrapper is the smallest sustainable check.
- Did not rewrite the skill into a larger multi-file framework. The existing progressive-disclosure
  shape is sound; the problem was contract drift and missing test surfaces.
- Did not remove the stored Markdown model answer. It remains useful as maintenance source text, but the
  user-facing reveal path should stay HTML.
