---
name: design-loop
description: Build complete multi-page static websites through an iterative baton workflow. Use when Codex should generate or continue multiple website pages, maintain shared navigation/footer consistency, read or write .design/next-prompt.md, create site/public HTML pages, or run an autonomous/step-by-step design loop for a site.
---

# Design Loop

Use this skill to build or continue a multi-page static website one page at a time while keeping project memory in `.design/`.

## Core Workflow

1. Check whether `.design/next-prompt.md` exists.
   - If it exists, read it and use it as the current page task.
   - If it does not exist, ask only for the minimum missing project context, then create `.design/SITE.md`, `.design/DESIGN.md`, and `.design/next-prompt.md`.
2. Read `.design/SITE.md`, `.design/DESIGN.md`, and the most recent page in `site/public/` before generating a new page.
3. Generate exactly one page per iteration in `site/public/{page}.html`.
4. Reuse shared header, nav, footer, fonts, colors, and Tailwind config from existing pages. Copy shared markup from the latest complete page instead of inventing a new variant.
5. Update all existing pages when navigation needs to include the new page.
6. Verify links and layout. If a local browser tool is available, open the page and capture/inspect desktop and mobile views.
7. Update `.design/SITE.md` to mark the page complete.
8. Rewrite `.design/next-prompt.md` with the next page task. If the site is complete, set `page: _complete` and summarize completion.

## Baton Format

Use `.design/next-prompt.md` with YAML frontmatter:

```markdown
---
page: about
layout: standard
---
Build the about page...

DESIGN SYSTEM:
[Relevant notes copied from .design/DESIGN.md]
```

## Codex Implementation Notes

- Prefer editing with `apply_patch`.
- Use `rg`/`rg --files` to inspect existing pages and project files.
- Use Browser or Playwright skills for visual checks when available.
- Keep pages self-contained unless the project already has a build system.
- Do not leave `href="#"` placeholders; link to real existing or planned pages.
- Do not regenerate completed pages except for shared navigation/link consistency.

## Completion Criteria

A page is complete when it is written, linked from navigation where appropriate, visually consistent with existing pages, responsive enough for desktop/mobile, and the next baton has been written.
