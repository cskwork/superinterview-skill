# Changelog - 2026-06-29

## Private resume context hook

- Added an optional `private/resume.md` hook so mock interviews can ask resume-aware questions without
  placing personal resume data in the public skill repository.
- Updated `.gitignore` to ignore `private/`. The actual candidate profile belongs in that local folder,
  not in tracked references, examples, docs, or eval fixtures.
- Rejected adding resume facts to public references because the repository is public and the profile
  contains personal career history and contact-adjacent links.
