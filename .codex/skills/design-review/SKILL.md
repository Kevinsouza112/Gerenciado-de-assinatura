---
name: design-review
description: Review a web page or app for visual design polish, including layout, spacing, typography, color, hierarchy, component consistency, interaction states, and responsive behavior. Use when the user asks for design review, visual audit, polish check, layout check, screenshots, or whether an interface looks professional.
---

# Design Review

Use this skill to review the visual quality of a web page or app. This is a visual design review, not a full UX research audit.

## Review Workflow

1. Identify the target URL or local app route.
2. Open the target with Browser or Playwright when available. For local apps, ensure the dev server is running first.
3. Inspect at least desktop and mobile widths when practical.
4. Look for issues in:
   - layout alignment and spacing
   - typography scale, weight, hierarchy, and line length
   - color contrast and semantic color consistency
   - visual hierarchy and primary action clarity
   - button, card, input, icon, and table consistency
   - hover/focus/active states
   - responsive behavior and touch target sizing
5. Capture screenshots when useful and the tooling is available.
6. Report findings by severity with file/component references when reviewing local code.

## Severity

- High: visually broken, unreadable, overlapping, inaccessible contrast, or clearly unprofessional.
- Medium: inconsistent spacing/components, weak hierarchy, awkward responsive behavior.
- Low: polish issues such as minor alignment, copy tone, overly strong shadows, or slight density mismatch.

## Output Shape

Lead with findings. Use this structure when there are issues:

```markdown
**Findings**
- High/Medium/Low: [issue] at [page/component/file] -> [fix]

**What Looks Good**
[Short notes]

**Top Fixes**
1. [highest impact]
2. [next]
3. [next]
```

If no issues are found, say that clearly and mention any limits of the review, such as not being able to run a browser.
