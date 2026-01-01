# React UI Component Libraries - Claude Code Install Guide

This document contains all npm install commands for building a v0/Figma Make-style app builder.
Copy-paste sections as needed or run the bulk install commands.

---

## BULK INSTALL - ESSENTIALS (Run First)

```bash
# Core utilities - REQUIRED for all Tailwind component libraries
npm install clsx tailwind-merge class-variance-authority
```
- `clsx`: Conditional className construction
- `tailwind-merge`: Merges conflicting Tailwind classes intelligently
- `class-variance-authority`: Type-safe component variants for Tailwind

---

## 1. HEADLESS/UNSTYLED PRIMITIVES

### Radix UI (Full Suite) - Foundation for shadcn/ui
```bash
npm install @radix-ui/react-accordion @radix-ui/react-alert-dialog @radix-ui/react-aspect-ratio @radix-ui/react-avatar @radix-ui/react-checkbox @radix-ui/react-collapsible @radix-ui/react-context-menu @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-hover-card @radix-ui/react-label @radix-ui/react-menubar @radix-ui/react-navigation-menu @radix-ui/react-popover @radix-ui/react-progress @radix-ui/react-radio-group @radix-ui/react-scroll-area @radix-ui/react-select @radix-ui/react-separator @radix-ui/react-slider @radix-ui/react-slot @radix-ui/react-switch @radix-ui/react-tabs @radix-ui/react-toast @radix-ui/react-toggle @radix-ui/react-toggle-group @radix-ui/react-tooltip
```

### Headless UI - Tailwind Labs Official
```bash
npm install @headlessui/react
```

### React Aria - Adobe Accessibility Library
```bash
npm install react-aria-components
```

---

## 2. TAILWIND-BASED COMPONENT LIBRARIES

### shadcn/ui - Industry Standard
```bash
npx shadcn@latest init
npx shadcn@latest add button card dialog dropdown-menu form input label select tabs toast
```

### daisyUI
```bash
npm install -D daisyui@latest
```

---

## 3. ANIMATION LIBRARIES

### Motion (Framer Motion)
```bash
npm install motion
```

### Auto-Animate
```bash
npm install @formkit/auto-animate
```

### GSAP
```bash
npm install gsap @gsap/react
```

---

## 4. ICON LIBRARIES

### Lucide React (shadcn default)
```bash
npm install lucide-react
```

### Heroicons
```bash
npm install @heroicons/react
```

---

## 5. FORM LIBRARIES

### React Hook Form + Zod
```bash
npm install react-hook-form zod @hookform/resolvers
```

---

## 6. TABLE LIBRARIES

### TanStack Table
```bash
npm install @tanstack/react-table
```

---

## 7. CHART LIBRARIES

### Recharts
```bash
npm install recharts
```

---

## 8. TOAST/NOTIFICATIONS

### Sonner
```bash
npm install sonner
```

---

## 9. DRAG AND DROP

### dnd-kit
```bash
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities
```

---

## ONE-LINER: ESSENTIAL STACK

```bash
npm install clsx tailwind-merge class-variance-authority lucide-react motion react-hook-form zod @hookform/resolvers sonner cmdk usehooks-ts
```

---

## NOTES
- Run `npx shadcn@latest init` first if using shadcn/ui
- daisyUI needs to be added to `tailwind.config.js` plugins
