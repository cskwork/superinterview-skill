# Changelog - 2026-06-29

## Private resume context hook

- Added an optional `private/resume.md` hook so mock interviews can ask resume-aware questions without
  placing personal resume data in the public skill repository.
- Updated `.gitignore` to ignore `private/`. The actual candidate profile belongs in that local folder,
  not in tracked references, examples, docs, or eval fixtures.
- Rejected adding resume facts to public references because the repository is public and the profile
  contains personal career history and contact-adjacent links.

## Resume form autofill mode

- Added `RESUME-FORM` routing for job application, resume form, and candidate profile autofill tasks.
- The mode maps browser-visible fields to `private/resume.md`, fills only supported facts, and stops
  before final submit, login/password, uploads, CAPTCHA, or legally sensitive self-identification unless
  the user explicitly confirms that action.
- Rejected folding form filling into the mock loop because the goal is accurate private-data transfer,
  not interview practice or grading.

## Skill description cleanup

- Rewrote the frontmatter description to be English-only and shorter while preserving the main trigger
  surfaces: mock interviews, grading, prep plans, and resume/application form autofill.
- Rejected a long keyword list because the description is the routing surface and should stay concise.

## Coding pattern recognition reference

- Added a coding reference that teaches pattern detection by asking what information the problem asks
  the candidate to track while scanning, rather than starting from memorized algorithm names.
- Routed CODING mode to the new reference for approach coaching, grading gaps, and re-drill design.
- Kept the guide separate from `SKILL.md` so coding support improves without making the router heavy.
