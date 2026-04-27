---
name: Hospitality Modernist
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#855300'
  on-secondary: '#ffffff'
  secondary-container: '#fea619'
  on-secondary-container: '#684000'
  tertiary: '#006242'
  on-tertiary: '#ffffff'
  tertiary-container: '#007d55'
  on-tertiary-container: '#bdffdb'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#ffddb8'
  secondary-fixed-dim: '#ffb95f'
  on-secondary-fixed: '#2a1700'
  on-secondary-fixed-variant: '#653e00'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  h1:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  h2:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.25'
    letterSpacing: -0.01em
  h3:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
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
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  stat-value:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  container-max: 1440px
  gutter: 24px
---

## Brand & Style
The brand personality for this design system bridges the gap between high-efficiency operational software and the emotional warmth of the hospitality industry. It utilizes a **Corporate Modern** style for the administrative dashboard—prioritizing data density and clarity—while pivoting toward a **Minimalist** approach with soft, tactile influences for the guest-facing landing pages.

The target audience includes hotel general managers, front-desk staff, and potential guests. The UI evokes a sense of "Reliable Luxury": professional and systematic for the staff to reduce cognitive load, yet inviting and aspirational for guests to encourage bookings. The design relies on generous white space, deliberate information architecture, and a sophisticated interplay of cool and warm tones.

## Colors
The color strategy employs a dual-palette system to differentiate the internal "Engine" from the external "Experience."

- **Management Dashboard:** A professional foundation of Deep Navy and Sapphire Blues (`#2563EB`) signifies stability and precision. Greys are leaned toward Slate to maintain a modern, tech-forward feel.
- **Guest Landing Page:** Transition to warm, inviting tones. A primary "Champagne Gold" (`#F59E0B`) is used for Call-to-Actions to evoke a sense of premium service and sunlight. 
- **Functional Colors:** Success states utilize a soft Emerald, while critical alerts use a refined Crimson.
- **Dark Mode:** In dark mode, surfaces shift to deep navy-greys rather than pure black to maintain depth and reduce eye strain for night-shift front desk staff.

## Typography
This design system pairs **Plus Jakarta Sans** for headings with **Inter** for UI and body text. 

Plus Jakarta Sans provides a friendly, modern geometric rhythm that works exceptionally well for property names and marketing headers. Inter is utilized for the core SaaS dashboard elements because of its high legibility in dense data environments, such as booking grids and guest manifests. 

Visual hierarchy is maintained through strict adherence to the type scale, using weight (Semi-Bold to Bold) to denote interactive elements and lighter weights for secondary metadata.

## Layout & Spacing
The layout philosophy is built on an **8px linear scale** to ensure mathematical harmony across all components. 

- **Dashboard:** Uses a fixed-width sidebar (260px) with a fluid content area. Content is organized in a 12-column grid. Data density is "Comfortable" by default but can be toggled to "Compact" by reducing internal padding from `md` to `sm`.
- **Guest Landing Page:** Employs a fixed-width centered container (`1440px`) with generous `xxl` vertical section spacing to create a high-end, editorial feel.
- **Grids:** Use a 24px gutter for standard dashboard modules to allow the UI to "breathe" and prevent the software from feeling cluttered.

## Elevation & Depth
This design system uses **Ambient Shadows** to create a natural sense of depth. Instead of harsh borders, elevation is communicated through three distinct levels:

1.  **Level 0 (Flat):** Background surfaces and inactive states.
2.  **Level 1 (Low):** Standard cards and input fields. Uses a soft, diffused shadow: `0 2px 4px rgba(0,0,0,0.05)`.
3.  **Level 2 (Floating):** Navigation bars, dropdowns, and active "Quick Action" buttons. Uses a more pronounced shadow: `0 10px 15px -3px rgba(0,0,0,0.1)`.

In the dashboard, we use **Tonal Layers** (slight variations in background hex codes) to separate the sidebar from the main workspace, while the guest landing page uses **Glassmorphism** (backdrop-blur) on the sticky navigation bar to maintain a connection to the hero imagery.

## Shapes
The shape language is consistently **Rounded**, reflecting a modern, approachable aesthetic. 

- **Standard Components:** Buttons and Input fields use a `0.5rem` (8px) radius.
- **Containers:** Dashboard cards and Guest-facing content blocks use `rounded-lg` (16px) to soften the overall visual impact.
- **Imagery:** Property photos should use `rounded-xl` (24px) for a premium, framed appearance.
- **Selection Indicators:** Small indicators (like active menu states) use a full pill shape for clear distinction.

## Components
Consistent component styling is vital for the operational efficiency of the system:

- **Buttons:** Primary buttons are solid-fill with the primary blue (dashboard) or gold (guest). Secondary buttons use a subtle tonal background. All buttons have a subtle 1px inner border for definition on high-brightness screens.
- **Input Fields:** Use a subtle grey background (`#F1F5F9`) in their rest state and transition to a white background with a 2px blue border on focus.
- **Cards:** Dashboard cards feature a white background with Level 1 shadows. Header areas within cards are separated by a subtle 1px divider.
- **Status Chips:** Used for room status (e.g., "Cleaned", "Occupied"). These use high-chroma text on low-opacity backgrounds (e.g., Dark Green text on light green background).
- **Booking Calendar:** A custom component using a dense grid. Current day is highlighted with a soft blue tint; guest stays are represented by rounded pill-bars spanning multiple cells.
- **Navigation:** Vertical for the dashboard (icon + label) and horizontal for the landing page (typography-focused).