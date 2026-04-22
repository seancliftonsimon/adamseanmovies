---
name: Blockbuster Nostalgia
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f4'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#444653'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f0f1f1'
  outline: '#747684'
  outline-variant: '#c4c5d5'
  surface-tint: '#3557bc'
  primary: '#002068'
  on-primary: '#ffffff'
  primary-container: '#003399'
  on-primary-container: '#8aa4ff'
  inverse-primary: '#b5c4ff'
  secondary: '#676000'
  on-secondary: '#ffffff'
  secondary-container: '#f2e400'
  on-secondary-container: '#6b6400'
  tertiary: '#580000'
  on-tertiary: '#ffffff'
  tertiary-container: '#810100'
  on-tertiary-container: '#ff8572'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b5c4ff'
  on-primary-fixed: '#00164e'
  on-primary-fixed-variant: '#153ea3'
  secondary-fixed: '#f5e700'
  secondary-fixed-dim: '#d7ca00'
  on-secondary-fixed: '#1f1c00'
  on-secondary-fixed-variant: '#4d4800'
  tertiary-fixed: '#ffdad4'
  tertiary-fixed-dim: '#ffb4a8'
  on-tertiary-fixed: '#410000'
  on-tertiary-fixed-variant: '#930100'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-lg:
    fontFamily: Epilogue
    fontSize: 64px
    fontWeight: '900'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-xl:
    fontFamily: Epilogue
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Epilogue
    fontSize: 32px
    fontWeight: '800'
    lineHeight: '1.2'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-bold:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1.2'
  vhs-label:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.0'
    letterSpacing: 0.1em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-margin: 32px
  gutter: 24px
  shelf-padding: 16px
---

## Refined Design Language (Pick for Us Baseline)

This system is now optimized around a **clean retro utility** style: still VHS-inspired, but less decorative and more layout-disciplined. The goal is to keep the "movie night" personality while making controls scannable and aligned.

### 1) Visual Personality
- **Tone:** Bold, playful, decisive.
- **Structure:** Functional panels first, ornament second.
- **Rule:** Decorative copy should never float outside panel logic. If text does not guide an action, remove it.

### 2) Composition Rules
- Use two primary zones on picker-style screens:
  1. **Filter Panel** (left / top on mobile): source selection + constraints.
  2. **Result Panel** (right / below on mobile): candidate count, preview posters, primary action.
- Every zone uses the same shell:
  - 3px dark border
  - hard offset shadow
  - warm off-white panel background
- Section labels must align directly with their controls (no detached hero text above empty boxes).

### 3) Typography System
- **Epilogue 800/900:** Headlines and major outcomes only (movie title, count headline).
- **Space Grotesk 700:** Utility labels and control headings (WHOSE PICKS, GENRES, RUNTIME).
- **Inter 400/500:** Supporting text only when needed.
- Remove redundant explanatory lines like onboarding slogans once interaction is self-explanatory.

### 4) Color & Contrast Usage
- **Royal Blue `#003399`:** structural emphasis (headers, active nav, kickers).
- **Pop Yellow `#F2E400`:** primary CTA and high-priority highlights.
- **Ink Black `#111111` / `#1A1A1A`:** borders and shadow anchors.
- **Paper `#fffcf3` to `#f7f3e8`:** content canvas.
- Maintain high contrast and avoid soft translucency for interactive elements.

### 5) Interaction Language
- Controls should be explicit and stacked in workflow order:
  1. Whose picks?
  2. Genres
  3. Runtime
  4. Pick action
- Active states must be obvious via color inversion (blue/yellow or dark/light).
- Only one primary action per panel ("Pick for Us"); secondary actions are visually quieter.

### 6) Spacing & Rhythm
- Base unit: **8px**.
- Typical vertical rhythm inside panels: **16–24px**.
- Labels sit immediately above controls with **8–10px** gap.
- Do not insert decorative empty framed elements; all framed elements should contain useful UI.

### 7) Component Guidance for Other Pages
- Reuse the picker panel shell for "task" surfaces (forms, filters, summaries).
- Reuse rounded pills for multi-select filters.
- Use hard-shadow buttons consistently:
  - default: offset shadow visible
  - hover: slightly larger offset
  - pressed/active: reduced offset
- Keep content hierarchy compact: label → control → feedback.

### 8) Content Guidelines
- Prefer direct, action-oriented copy.
- Avoid duplicated headlines/subtitles when labels already explain controls.
- Reserve celebratory voice for outcomes (final picked movie), not setup instructions.
