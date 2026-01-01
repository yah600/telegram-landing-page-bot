"""
Professional Landing Page Generator - v0/Figma Make quality.
"""

import logging
from ai_client import AIClient
from design_tokens import get_tailwind_config, get_design_system_prompt_addition

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an elite frontend developer who creates stunning, high-converting landing pages.
Your code quality matches v0.dev and Figma Make. You write clean, semantic HTML with Tailwind CSS.
Every page you create looks professionally designed with perfect typography, spacing, and visual hierarchy."""

GENERATION_PROMPT = '''Create a COMPLETE, PRODUCTION-READY landing page.

## BUSINESS CONTEXT
{business_info}

## PAGE STRATEGY
{plan}

## VISUAL DIRECTION
{design_system}

## TECHNICAL REQUIREMENTS

### Stack
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Business Name] - [Value Proposition]</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    {tailwind_config}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{ font-family: 'Inter', system-ui, sans-serif; }}
    .animate-fade-in {{ animation: fadeIn 0.6s ease-out forwards; }}
    .animate-slide-up {{ animation: slideUp 0.6s ease-out forwards; }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
</head>
```

### Required Sections (implement ALL with FULL content)

1. **NAVIGATION** - Sticky, glass-morphism effect
   - Logo placeholder (text-xl font-bold)
   - Nav links with hover states
   - CTA button (primary style)
   - Mobile hamburger menu (Alpine.js)

2. **HERO** - min-h-[90vh], centered content
   - Eyebrow text (small badge above headline)
   - Main headline: text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight
   - Subheadline: text-xl md:text-2xl text-neutral-600 max-w-2xl
   - Two CTAs: Primary (filled) + Secondary (outlined)
   - Trust indicators (logos, stats, or badges)
   - Optional: subtle gradient background

3. **PROBLEM/PAIN POINTS** - py-20 bg-neutral-50
   - Section headline + description
   - 3 pain point cards with icons
   - Each card: icon + title + description

4. **SOLUTION** - py-20 bg-white
   - How the business solves problems
   - Feature image placeholder
   - Bullet points with checkmarks

5. **FEATURES/BENEFITS** - py-20 bg-gradient-to-b from-white to-neutral-50
   - Section headline centered
   - 3-column grid of feature cards
   - Each: icon + title + description + optional link
   - Cards with hover elevation effect

6. **SOCIAL PROOF** - py-20 bg-white
   - Section headline
   - 3 testimonial cards
   - Each: avatar + name + role + company + quote + star rating
   - Optional: company logos row

7. **HOW IT WORKS** - py-20 bg-neutral-50
   - 3-4 step process
   - Each step: number + title + description
   - Visual connection between steps

8. **PRICING/OFFER** (if applicable) - py-20
   - Pricing cards or single offer
   - Feature lists with checkmarks
   - CTA buttons

9. **FAQ** - py-20 bg-white
   - Accordion-style (Alpine.js)
   - 5-6 relevant questions
   - Smooth open/close animation

10. **FINAL CTA** - py-20 bg-primary-600 text-white
    - Compelling headline
    - Brief value reminder
    - Large CTA button (white/light)
    - Optional: form for email capture

11. **FOOTER** - py-12 bg-neutral-900 text-neutral-400
    - Logo + tagline
    - Link columns
    - Social icons
    - Copyright

{design_additions}

### UI COMPONENT PATTERNS (Use exactly)

**Primary Button:**
```html
<a href="#" class="inline-flex items-center justify-center gap-2 rounded-xl bg-primary-600 px-6 py-3.5 text-base font-semibold text-white shadow-lg shadow-primary-600/25 transition-all duration-200 hover:bg-primary-700 hover:shadow-xl hover:-translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
  Get Started
  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
</a>
```

**Secondary Button:**
```html
<a href="#" class="inline-flex items-center justify-center gap-2 rounded-xl border-2 border-neutral-200 bg-white px-6 py-3.5 text-base font-semibold text-neutral-900 transition-all duration-200 hover:border-neutral-300 hover:bg-neutral-50">
  Learn More
</a>
```

**Feature Card:**
```html
<div class="group rounded-2xl border border-neutral-200 bg-white p-8 transition-all duration-300 hover:shadow-xl hover:shadow-neutral-900/5 hover:border-neutral-300 hover:-translate-y-1">
  <div class="mb-5 inline-flex items-center justify-center w-12 h-12 rounded-xl bg-primary-100 text-primary-600">
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
  </div>
  <h3 class="mb-3 text-xl font-semibold text-neutral-900">Feature Title</h3>
  <p class="text-neutral-600 leading-relaxed">Description text goes here with helpful details.</p>
</div>
```

**Testimonial Card:**
```html
<div class="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-neutral-900/5">
  <div class="flex gap-1 mb-4">
    <svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
    <!-- Repeat 5x for 5 stars -->
  </div>
  <blockquote class="mb-6 text-lg text-neutral-700 leading-relaxed">"Quote text here..."</blockquote>
  <div class="flex items-center gap-4">
    <div class="w-12 h-12 rounded-full bg-neutral-200 flex items-center justify-center text-neutral-500 font-semibold">JD</div>
    <div>
      <div class="font-semibold text-neutral-900">John Doe</div>
      <div class="text-sm text-neutral-500">CEO, Company</div>
    </div>
  </div>
</div>
```

**Section Container:**
```html
<section class="py-20 md:py-28 bg-white">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center max-w-3xl mx-auto mb-16">
      <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold text-neutral-900 mb-6">Section Headline</h2>
      <p class="text-lg md:text-xl text-neutral-600">Section description with more context.</p>
    </div>
    <!-- Content here -->
  </div>
</section>
```

### Alpine.js for Interactivity
```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

**Mobile Menu:**
```html
<div x-data="{{ open: false }}">
  <button @click="open = !open" class="md:hidden">
    <svg x-show="!open" class="w-6 h-6">...</svg>
    <svg x-show="open" class="w-6 h-6">...</svg>
  </button>
  <div x-show="open" x-transition class="md:hidden">...</div>
</div>
```

**FAQ Accordion:**
```html
<div x-data="{{ active: null }}">
  <div class="border-b border-neutral-200">
    <button @click="active = active === 1 ? null : 1" class="w-full py-5 text-left flex justify-between items-center">
      <span class="text-lg font-medium">Question?</span>
      <svg :class="{{'rotate-180': active === 1}}" class="w-5 h-5 transition-transform">...</svg>
    </button>
    <div x-show="active === 1" x-collapse>
      <p class="pb-5 text-neutral-600">Answer...</p>
    </div>
  </div>
</div>
```

### Icons (Use Heroicons inline SVG)
```html
<!-- Check -->
<svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>

<!-- Arrow Right -->
<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>

<!-- Star (filled) -->
<svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
```

## OUTPUT FORMAT

Output ONLY the complete HTML code:
- Start with <!DOCTYPE html>
- End with </html>
- NO markdown code blocks
- NO explanations
- COMPLETE implementation of ALL sections
- Real, compelling copy based on the business
- Minimum 400 lines of HTML

Generate the landing page now:'''


class CodeGenerator:
    """Generate v0-quality landing pages."""

    def __init__(self):
        self.ai = AIClient()

    async def generate_website(
        self,
        business_info: str,
        plan: str,
        design_system: str,
        progress_callback=None
    ) -> str:
        """Generate a complete landing page."""

        async def update(msg):
            if progress_callback:
                await progress_callback(msg)

        await update("Generating professional landing page...")

        # Build the prompt
        prompt = GENERATION_PROMPT.format(
            business_info=business_info,
            plan=plan,
            design_system=design_system,
            tailwind_config=get_tailwind_config("modern"),
            design_additions=get_design_system_prompt_addition()
        )

        # Add system context
        full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"

        html_code = await self.ai.generate_code(full_prompt, max_tokens=16000, temperature=0.4)
        html_code = self._clean_html(html_code)

        await update("Validating code quality...")

        if not self._is_complete(html_code):
            await update("Enhancing sections...")
            html_code = await self._enhance_code(html_code)

        await update("Landing page generated!")
        logger.info(f"Generated HTML: {len(html_code)} chars, {html_code.count(chr(10))} lines")

        return html_code

    async def _enhance_code(self, html_code: str) -> str:
        """Fix incomplete code."""
        prompt = f"""Fix and complete this landing page HTML. Ensure ALL sections are fully implemented.

{html_code}

Return ONLY the complete, fixed HTML. Start with <!DOCTYPE html>, end with </html>."""

        enhanced = await self.ai.generate_code(prompt, max_tokens=16000, temperature=0.3)
        enhanced = self._clean_html(enhanced)

        if len(enhanced) > len(html_code) * 0.8 and self._is_valid_html(enhanced):
            return enhanced
        return html_code

    def _clean_html(self, code: str) -> str:
        """Clean up generated HTML."""
        if "```html" in code:
            code = code.split("```html", 1)[-1]
        if "```" in code:
            code = code.split("```")[0]

        if "<!DOCTYPE" in code:
            code = code[code.index("<!DOCTYPE"):]
        if "</html>" in code:
            code = code[:code.rindex("</html>") + 7]

        return code.strip()

    def _is_valid_html(self, code: str) -> bool:
        """Check if HTML structure is valid."""
        required = ["<!DOCTYPE", "<html", "<head", "<body", "</html>"]
        return all(tag.lower() in code.lower() for tag in required)

    def _is_complete(self, code: str) -> bool:
        """Check if HTML is complete."""
        incomplete = ["// rest", "/* rest", "...", "[MORE", "TODO:", "<!-- Add more"]
        for sign in incomplete:
            if sign.lower() in code.lower():
                return False

        required = ["nav", "hero", "footer", "section"]
        for section in required:
            if section not in code.lower():
                return False

        return len(code) > 8000
