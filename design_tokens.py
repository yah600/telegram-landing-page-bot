"""
Professional Design Token System - Matching v0/Figma Make quality.
"""

# Modern, professional color palettes
COLOR_PALETTES = {
    "modern": {
        "primary": {"50": "#eff6ff", "100": "#dbeafe", "200": "#bfdbfe", "300": "#93c5fd", "400": "#60a5fa", "500": "#3b82f6", "600": "#2563eb", "700": "#1d4ed8", "800": "#1e40af", "900": "#1e3a8a"},
        "neutral": {"50": "#fafafa", "100": "#f4f4f5", "200": "#e4e4e7", "300": "#d4d4d8", "400": "#a1a1aa", "500": "#71717a", "600": "#52525b", "700": "#3f3f46", "800": "#27272a", "900": "#18181b"},
        "accent": "#8b5cf6",
        "success": "#22c55e",
        "warning": "#f59e0b",
        "error": "#ef4444",
    },
    "elegant": {
        "primary": {"50": "#fdf4ff", "100": "#fae8ff", "200": "#f5d0fe", "300": "#f0abfc", "400": "#e879f9", "500": "#d946ef", "600": "#c026d3", "700": "#a21caf", "800": "#86198f", "900": "#701a75"},
        "neutral": {"50": "#f8fafc", "100": "#f1f5f9", "200": "#e2e8f0", "300": "#cbd5e1", "400": "#94a3b8", "500": "#64748b", "600": "#475569", "700": "#334155", "800": "#1e293b", "900": "#0f172a"},
        "accent": "#06b6d4",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#f43f5e",
    },
    "bold": {
        "primary": {"50": "#fef2f2", "100": "#fee2e2", "200": "#fecaca", "300": "#fca5a5", "400": "#f87171", "500": "#ef4444", "600": "#dc2626", "700": "#b91c1c", "800": "#991b1b", "900": "#7f1d1d"},
        "neutral": {"50": "#f9fafb", "100": "#f3f4f6", "200": "#e5e7eb", "300": "#d1d5db", "400": "#9ca3af", "500": "#6b7280", "600": "#4b5563", "700": "#374151", "800": "#1f2937", "900": "#111827"},
        "accent": "#fbbf24",
        "success": "#34d399",
        "warning": "#fb923c",
        "error": "#f87171",
    },
    "minimal": {
        "primary": {"50": "#f9fafb", "100": "#f3f4f6", "200": "#e5e7eb", "300": "#d1d5db", "400": "#9ca3af", "500": "#6b7280", "600": "#4b5563", "700": "#374151", "800": "#1f2937", "900": "#030712"},
        "neutral": {"50": "#fafafa", "100": "#f5f5f5", "200": "#e5e5e5", "300": "#d4d4d4", "400": "#a3a3a3", "500": "#737373", "600": "#525252", "700": "#404040", "800": "#262626", "900": "#171717"},
        "accent": "#0ea5e9",
        "success": "#22c55e",
        "warning": "#eab308",
        "error": "#dc2626",
    }
}

# Typography system
TYPOGRAPHY = {
    "font_families": {
        "sans": "Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "display": "Cal Sans, Inter, system-ui, sans-serif",
        "mono": "JetBrains Mono, Fira Code, monospace",
    },
    "font_sizes": {
        "xs": "0.75rem",      # 12px
        "sm": "0.875rem",     # 14px
        "base": "1rem",       # 16px
        "lg": "1.125rem",     # 18px
        "xl": "1.25rem",      # 20px
        "2xl": "1.5rem",      # 24px
        "3xl": "1.875rem",    # 30px
        "4xl": "2.25rem",     # 36px
        "5xl": "3rem",        # 48px
        "6xl": "3.75rem",     # 60px
        "7xl": "4.5rem",      # 72px
    },
    "line_heights": {
        "tight": "1.25",
        "snug": "1.375",
        "normal": "1.5",
        "relaxed": "1.625",
        "loose": "2",
    },
    "letter_spacing": {
        "tighter": "-0.05em",
        "tight": "-0.025em",
        "normal": "0",
        "wide": "0.025em",
        "wider": "0.05em",
    }
}

# Spacing system (8px base)
SPACING = {
    "0": "0",
    "1": "0.25rem",   # 4px
    "2": "0.5rem",    # 8px
    "3": "0.75rem",   # 12px
    "4": "1rem",      # 16px
    "5": "1.25rem",   # 20px
    "6": "1.5rem",    # 24px
    "8": "2rem",      # 32px
    "10": "2.5rem",   # 40px
    "12": "3rem",     # 48px
    "16": "4rem",     # 64px
    "20": "5rem",     # 80px
    "24": "6rem",     # 96px
    "32": "8rem",     # 128px
}

# Shadow system
SHADOWS = {
    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "DEFAULT": "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)",
    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
    "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
    "2xl": "0 25px 50px -12px rgb(0 0 0 / 0.25)",
    "inner": "inset 0 2px 4px 0 rgb(0 0 0 / 0.05)",
}

# Border radius
RADIUS = {
    "none": "0",
    "sm": "0.125rem",   # 2px
    "DEFAULT": "0.25rem",  # 4px
    "md": "0.375rem",   # 6px
    "lg": "0.5rem",     # 8px
    "xl": "0.75rem",    # 12px
    "2xl": "1rem",      # 16px
    "3xl": "1.5rem",    # 24px
    "full": "9999px",
}

# Animation timing
ANIMATIONS = {
    "durations": {
        "fast": "150ms",
        "normal": "200ms",
        "slow": "300ms",
        "slower": "500ms",
    },
    "easings": {
        "default": "cubic-bezier(0.4, 0, 0.2, 1)",
        "in": "cubic-bezier(0.4, 0, 1, 1)",
        "out": "cubic-bezier(0, 0, 0.2, 1)",
        "in-out": "cubic-bezier(0.4, 0, 0.2, 1)",
        "bounce": "cubic-bezier(0.68, -0.55, 0.265, 1.55)",
    }
}

# V0-style component patterns
COMPONENT_PATTERNS = """
/* === BUTTONS === */
.btn-primary {
  @apply inline-flex items-center justify-center gap-2 rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-200 hover:bg-primary-700 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 active:scale-[0.98];
}

.btn-secondary {
  @apply inline-flex items-center justify-center gap-2 rounded-lg border border-neutral-300 bg-white px-5 py-2.5 text-sm font-semibold text-neutral-700 shadow-sm transition-all duration-200 hover:bg-neutral-50 hover:border-neutral-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2;
}

.btn-ghost {
  @apply inline-flex items-center justify-center gap-2 rounded-lg px-5 py-2.5 text-sm font-semibold text-neutral-600 transition-all duration-200 hover:bg-neutral-100 hover:text-neutral-900;
}

/* === CARDS === */
.card {
  @apply rounded-2xl border border-neutral-200 bg-white p-6 shadow-sm transition-all duration-200 hover:shadow-md;
}

.card-elevated {
  @apply rounded-2xl bg-white p-6 shadow-lg ring-1 ring-neutral-900/5 transition-all duration-200 hover:shadow-xl;
}

/* === INPUTS === */
.input {
  @apply block w-full rounded-lg border border-neutral-300 bg-white px-4 py-2.5 text-neutral-900 placeholder-neutral-400 shadow-sm transition-all duration-200 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/20;
}

/* === BADGES === */
.badge {
  @apply inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium;
}

.badge-primary {
  @apply bg-primary-100 text-primary-700;
}

/* === SECTIONS === */
.section {
  @apply py-16 md:py-24 lg:py-32;
}

.container {
  @apply mx-auto max-w-7xl px-4 sm:px-6 lg:px-8;
}

/* === GRADIENTS === */
.gradient-text {
  @apply bg-gradient-to-r from-primary-600 to-primary-400 bg-clip-text text-transparent;
}

.gradient-bg {
  @apply bg-gradient-to-br from-primary-50 via-white to-primary-50;
}
"""

def get_tailwind_config(palette_name: str = "modern") -> str:
    """Generate Tailwind config with design tokens."""
    import json
    palette = COLOR_PALETTES.get(palette_name, COLOR_PALETTES["modern"])

    primary_json = json.dumps(palette['primary'])
    neutral_json = json.dumps(palette['neutral'])

    return f"""
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            primary: {primary_json},
            neutral: {neutral_json},
            accent: '{palette['accent']}',
            success: '{palette['success']}',
            warning: '{palette['warning']}',
            error: '{palette['error']}',
          }},
          fontFamily: {{
            sans: ['Inter', 'system-ui', 'sans-serif'],
          }},
          boxShadow: {{
            'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
          }},
        }},
      }},
    }}
    """


def get_design_system_prompt_addition() -> str:
    """Get additional prompt content for better designs."""
    return """
## DESIGN PRINCIPLES (CRITICAL - FOLLOW EXACTLY)

### Visual Hierarchy
- Headlines: text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight
- Subheadlines: text-xl md:text-2xl text-neutral-600 font-normal
- Body: text-base md:text-lg text-neutral-600 leading-relaxed
- Use max-w-3xl for readable text blocks

### Spacing (Use Generously)
- Sections: py-20 md:py-28 lg:py-32
- Between elements: space-y-6 or space-y-8
- Container: max-w-7xl mx-auto px-4 sm:px-6 lg:px-8

### Colors (Use Semantic)
- Primary actions: bg-primary-600 hover:bg-primary-700
- Secondary: bg-white border border-neutral-200
- Text: text-neutral-900 (headings), text-neutral-600 (body)
- Backgrounds: bg-white, bg-neutral-50, bg-gradient-to-b from-white to-neutral-50

### Modern UI Patterns
- Rounded corners: rounded-xl or rounded-2xl for cards
- Subtle shadows: shadow-sm hover:shadow-md transition-shadow
- Borders: border border-neutral-200 or ring-1 ring-neutral-900/5
- Hover states: Always include hover transitions
- Focus states: focus:ring-2 focus:ring-primary-500 focus:ring-offset-2

### Buttons (EXACT patterns)
Primary: "inline-flex items-center justify-center gap-2 rounded-xl bg-primary-600 px-6 py-3 text-base font-semibold text-white shadow-lg shadow-primary-500/25 transition-all hover:bg-primary-700 hover:shadow-xl hover:shadow-primary-500/30 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"

Secondary: "inline-flex items-center justify-center gap-2 rounded-xl border-2 border-neutral-200 bg-white px-6 py-3 text-base font-semibold text-neutral-900 transition-all hover:border-neutral-300 hover:bg-neutral-50"

### Cards
"rounded-2xl border border-neutral-200 bg-white p-8 shadow-sm transition-all duration-300 hover:shadow-lg hover:border-neutral-300"

### Hero Section Pattern
- Full viewport or near: min-h-[90vh] or min-h-screen
- Centered content with max-width
- Large headline with gradient or accent color
- Clear value proposition
- Two CTAs (primary + secondary)
- Trust indicators below CTAs
- Optional: subtle background pattern or gradient

### Feature Grid Pattern
- 3-column grid on desktop: grid md:grid-cols-3 gap-8
- Icon + Title + Description per card
- Consistent icon styling: w-12 h-12 text-primary-600
- Card hover effects

### Testimonial Pattern
- Avatar + Name + Role + Quote
- Star ratings if applicable
- Subtle card background
- Consider carousel for multiple

### CTA Section Pattern
- Contrasting background: bg-primary-600 or bg-neutral-900
- White/light text
- Centered content
- Single focused action
- Optional: subtle pattern overlay

### Footer Pattern
- Multi-column layout
- Logo + tagline
- Navigation links grouped
- Social icons
- Copyright + legal links
"""
