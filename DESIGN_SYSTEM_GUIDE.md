# StormSense AI Design System Guide

Generated: 2026-06-08

## Design Intent
StormSense AI uses an operational workstation style: dark panels, high-contrast status text, restrained accent colors, dense but readable metadata, and command-deck navigation. This guide documents the existing interface; it does not propose a redesign.

## Typography
| Use | Font |
| --- | --- |
| Headings, navigation, labels, buttons, cards, table headers | Satoshi |
| Dates, times, station codes, metadata, parameters, verification codes, forecast IDs | JetBrains Mono |
| Fallback stack | Inter, Roboto, system sans-serif where configured by the frontend |

## Interface Tokens
| Element | Observed Pattern |
| --- | --- |
| Page shell | Dark operational canvas with fixed sidebar and content workspace. |
| Cards/panels | Low-radius dark panels with subtle borders and status accent colors. |
| Buttons | Compact action buttons, primary blue for action, accent red/amber/green/purple for status. |
| Inputs | Dark select/input fields with visible borders and mono values where technical. |
| Tables | Dense operational rows with sticky/visible headers where useful and overflow protection. |
| Accordions | Advanced/scientific details collapsed by default where complexity is high. |
| Metadata HUD | Observation date/time, forecast generated, station, cycle, and data source in a compact mono layout. |

## Status Color Semantics
| Color Family | Operational Meaning |
| --- | --- |
| Blue | Primary action, selected station, forecast metadata, stable operation. |
| Green | Online, accepted, pass, source-traceable, favorable completed state. |
| Amber/Yellow | Monitoring, caution, heavy rain, cycle timing, intermediate risk. |
| Red/Pink | Critical alert, miss, static data warning, severe thunderstorm risk. |
| Purple | Review/evidence accent, severe escalation, advanced scientific detail. |

## Screenshot Evidence
46 supplied screenshots are catalogued in `SCREENSHOT_ANALYSIS_REPORT.md` and copied under `docs/screenshots/`.

