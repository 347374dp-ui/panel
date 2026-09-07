# DP Control Panel — UI continuity notes

## Current visual direction
- Premium dark glass interface with blue-to-violet accents.
- Calm background constellation behind transparent cards.
- Bright, short impact bloom, three water-ripple rings, and four-point sparkle feedback when clicking non-interactive page space.
- Tables have a single uniform resting state and a subtle contiguous blue hover state.

## Important safeguards
- `app.js` is the Firebase/data layer. Do not modify it for visual work.
- `#particleCanvas` must remain `pointer-events: none` and sit at `z-index: 0`.
- App content needs `z-index: 1`; the navbar needs a higher z-index.
- Every page, including `dashboard.html`, includes both the canvas and `particles.js`.
- The click listener must ignore every interactive control (`a`, `button`, form fields, labels, and exporter tabs).
- Keep click effects capped (`MAX_CLICK_EFFECTS`) to preserve smooth repeated clicks.
- Account creation actions intentionally use one full-width button per row; long labels must not share the narrow account card.
- `.maxuid-input` uses a fixed 96px numeric field; retain this width so multi-digit UID limits remain readable.
- Account-table action cells use `display: table-cell`; never apply flex directly to a `<td>`, or buttons and headers will become misaligned.
- UID identifiers and dates must remain unbroken; use a scrolling table wrapper rather than forcing word breaks.

## If work resumes later
Start by visually checking `index.html`, `admin.html`, `panel_admin.html`, and `feature_builder.html`. Prioritize working navigation, readable buttons, and stable tables before adding more effects.
