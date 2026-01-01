"""
React Landing Page Generator - Creates Next.js/React components.
"""

import logging
from ai_client import AIClient

logger = logging.getLogger(__name__)

REACT_PROMPT = '''Create a React landing page component for this business:

{business_info}

Requirements:
- Export default function LandingPage()
- Use Tailwind CSS for styling
- Include: Hero, Features (3 cards), Testimonials, CTA, Footer
- Use Lucide React icons: import {{ Star, Check, ArrowRight }} from 'lucide-react'
- Professional design with proper spacing (py-20, px-6)
- Responsive (mobile-first)
- Modern colors: primary-600, neutral-900, neutral-600

Example structure:
```jsx
import {{ Star, Check, ArrowRight, Menu, X }} from 'lucide-react'
import {{ useState }} from 'react'

export default function LandingPage() {{
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-white">
      {{/* Navigation */}}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b">
        ...
      </nav>

      {{/* Hero */}}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-neutral-900 mb-6">
            Headline Here
          </h1>
          <p className="text-xl text-neutral-600 mb-8 max-w-2xl mx-auto">
            Subheadline
          </p>
          <button className="bg-primary-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-primary-700 transition">
            Get Started <ArrowRight className="inline ml-2 w-5 h-5" />
          </button>
        </div>
      </section>

      {{/* Features */}}
      <section className="py-20 bg-neutral-50 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {{/* Feature cards */}}
          </div>
        </div>
      </section>

      {{/* More sections... */}}

      {{/* Footer */}}
      <footer className="bg-neutral-900 text-white py-12 px-6">
        ...
      </footer>
    </div>
  )
}}
```

Output ONLY the complete React component code. Start with imports, end with export.
No explanations. No markdown code blocks. Just the JSX code.

Generate now for: {business_name}'''


class CodeGenerator:
    """Generate React landing pages."""

    def __init__(self):
        self.ai = AIClient()

    async def generate_website(
        self,
        business_info: str,
        plan: str,
        design_system: str,
        progress_callback=None
    ) -> str:
        """Generate a React landing page component."""

        async def update(msg):
            if progress_callback:
                await progress_callback(msg)

        await update("Generating React component...")

        # Extract business name
        business_name = "Landing Page"
        for line in business_info.split('\n'):
            if 'name' in line.lower():
                business_name = line.split(':')[-1].strip()
                break

        # Shorter prompt
        prompt = REACT_PROMPT.format(
            business_info=business_info[:2000],
            business_name=business_name
        )

        code = await self.ai.generate_code(prompt, max_tokens=4000, temperature=0.4)
        code = self._clean_code(code)

        await update("React component generated!")
        logger.info(f"Generated React: {len(code)} chars")

        return code

    def _clean_code(self, code: str) -> str:
        """Clean generated code."""
        # Remove markdown
        if "```jsx" in code:
            code = code.split("```jsx", 1)[-1]
        if "```javascript" in code:
            code = code.split("```javascript", 1)[-1]
        if "```" in code:
            code = code.split("```")[0]

        code = code.strip()

        # Ensure it starts with import
        if not code.startswith("import"):
            if "import" in code:
                code = code[code.index("import"):]

        return code
