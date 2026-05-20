---
name: design-system
description: Extract or document a reusable design system from an existing website, local HTML/app, screenshot, or project. Use when Codex should create DESIGN.md, identify colors/typography/components/spacing, reverse engineer visual style, or prepare design tokens for future page generation.
---

# Design System Extractor

Use this skill to create a practical `DESIGN.md` that Codex can reuse for consistent UI generation.

## Workflow

1. Identify the source: live URL, local route, local HTML/CSS files, screenshot, or existing project pages.
2. Prefer source code and computed HTML/CSS over screenshot-only guesses.
3. Gather raw design data:
   - colors from CSS variables, Tailwind config/classes, inline styles, or computed styles
   - typography from font imports, font families, sizes, weights, and line heights
   - component patterns for buttons, cards, nav, forms, tables, badges, modals
   - spacing/layout rules such as max width, grid columns, gutters, section padding
4. Synthesize semantic tokens instead of dumping CSS.
5. Write `.design/DESIGN.md` unless the user asks for a different path.
6. If possible, verify by comparing a generated sample or target page visually with Browser/Playwright.

## DESIGN.md Structure

Use this structure:

```markdown
# Design System: [Project Name]

## 1. Visual Theme & Atmosphere
[Describe the mood, density, and visual philosophy.]

## 2. Colour Palette & Roles
| Role | Name | Value | Usage |
|---|---|---|---|

## 3. Typography
| Element | Font | Weight | Size | Line Height |
|---|---|---|---|---|

## 4. Component Styles
[Buttons, cards, navigation, forms, tables, badges, states.]

## 5. Layout Principles
[Max width, grids, section spacing, responsive behavior.]

## 6. Design System Notes for Generation
[Concise copy-paste block for future page prompts.]
```

## Codex Notes

- Use `rg` and file reads to inspect local projects.
- Use Browser/Playwright for screenshots or computed visual checks when available.
- Flag approximate values when they come from screenshots rather than source.
- Keep the output actionable for future implementation, not just descriptive.
