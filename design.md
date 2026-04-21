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

## Brand & Style

The design system is an unapologetic homage to the golden age of physical media rental. It prioritizes high-energy, high-contrast visuals over modern minimalism. The personality is "Commercial Energetic"—evoking the feeling of walking into a brightly lit store on a Friday night. 

The aesthetic style merges **High-Contrast Bold** with **Tactile / Skeuomorphic** elements. It utilizes the "Physicality of the 90s" by referencing real-world objects: the glossy plastic of a VHS case, the magnetic strip of a membership card, and the punchy, backlit glow of store signage. It avoids subtle gradients and ambient blurs in favor of hard-edged shadows, thick strokes, and vibrant saturation.

## Colors

The palette is anchored by the iconic duo of Royal Blue and Pop Yellow. 
- **Royal Blue (#003399)**: Used for primary containers, headers, and backgrounds to provide a deep, reliable foundation.
- **Pop Yellow (#FFF000)**: Reserved for primary actions, highlights, and "New Release" style callouts. It must always be paired with dark text for accessibility.
- **New Release Red (#E60000)**: An accent color used sparingly for urgency, sale prices, or "Live" indicators, reminiscent of clearance stickers.
- **VHS Black (#1A1A1A)**: Used for typography and "plastic" elements, ensuring high legibility against the yellow and white.

## Typography

This design system uses a "Chunky Sans" approach. **Epilogue** is the hero font, utilized in heavy weights (800-900) to mimic the weight of physical signage. Headlines should feel massive and authoritative.

**Inter** provides a clean, neutral balance for long-form text, ensuring the interface remains functional despite the loud brand elements. **Space Grotesk** is used for utility labels and "meta" information, nodding to the technical, monospaced-adjacent look of rental receipts and VHS spine labels. Large headlines should utilize tight letter-spacing to reinforce the "blocky" feel.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy, reminiscent of organized store shelves. Content is housed in 12-column layouts with generous margins to prevent the high-contrast colors from feeling claustrophobic.

Spacing is calculated in 8px increments. The "Shelf" model is preferred for content discovery: horizontal rows with strict alignment that mimic the experience of browsing VHS tapes. Use defined borders rather than whitespace to separate different sections of the UI.

## Elevation & Depth

Depth is communicated through **Bold Borders** and **Hard Shadows** rather than soft blurs. 

1.  **Level 0 (Floor):** Flat white or Royal Blue background.
2.  **Level 1 (Card):** 2px solid border (VHS Black or Royal Blue) with a 4px-8px hard offset shadow in Pop Yellow or VHS Black.
3.  **Level 2 (Active/Pressed):** Shadow offset reduces to 0px, and the element shifts slightly to simulate a physical button press.

Avoid all use of Gaussian blurs or "glassmorphism." Surfaces should feel opaque, solid, and made of high-gloss plastic or cardstock.

## Shapes

The primary shape language is **Rounded**, reflecting the injection-molded plastic of tape cassettes and the die-cut corners of membership cards. 

A specific signature element of this design system is the **"Ticket Notch"**—a 45-degree inward corner cut used on the corners of primary containers and hero sections, directly referencing the classic "torn ticket" logo silhouette. Buttons use a standard 0.5rem radius, while "VHS Case" cards use a slightly tighter 0.25rem radius to look more rectangular and stackable.

## Components

- **Buttons:** Primary buttons are Pop Yellow with heavy VHS Black text. They feature a 2px solid black border and a hard offset shadow. On hover, the shadow grows; on click, it disappears.
- **VHS Cards:** Content items (like movie posters or product cards) should be styled as VHS boxes. This includes a subtle "plastic" sheen overlay and a vertical "spine" label on the left edge for metadata.
- **Membership Chips:** Use a "magnetic strip" style footer for tags or status indicators. Rounded-lg backgrounds with a dark horizontal bar.
- **Inputs:** Styled after rental agreement forms. Thick borders, bright yellow focus states, and bold labels.
- **Status Badges:** Styled like "Be Kind, Rewind" stickers—circular or oval shapes placed at a slight 5-degree tilt to look manually applied.
- **Dividers:** Use a "Film Strip" pattern—a black line with white rectangular perforations—to separate major page sections.
