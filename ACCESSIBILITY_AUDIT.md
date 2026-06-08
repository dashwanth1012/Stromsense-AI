# Accessibility Audit

Generated: 2026-06-08

This audit records evidence visible in source/screenshots and identifies the final checks needed for WCAG 2.1 AA certification. It does not certify WCAG compliance by itself.

| Area | Evidence | Remaining Validation |
| --- | --- | --- |
| Keyboard navigation | Primary controls are standard buttons/selects/inputs in React modules. | Manual keyboard traversal still required before public release. |
| ARIA semantics | Operational status text is visible; icon-only controls should have accessible labels where implemented. | Audit with browser accessibility tree recommended. |
| Color contrast | Screenshots show high-contrast text on dark panels and color-coded status labels. | Run automated WCAG contrast check on production URL. |
| Responsive layouts | Screenshots include laptop/desktop evidence; archive/table overflow issues were previously targeted. | Validate 1366x768, 1600x900, 1920x1080. |
| Focus states | Buttons and inputs are visible; focus state needs browser validation. | Use keyboard-only review mode walkthrough. |
| Screen readers | Complex maps/charts require textual companion summaries. | Ensure maps/charts retain adjacent operational summary text. |
| Review Mode | Reduces visual complexity and hides diagnostic clutter. | Validate reviewer can understand a case within 20-30 seconds. |

