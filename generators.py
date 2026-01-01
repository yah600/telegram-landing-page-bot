"""
Document generators for PLAN.md, DESIGN_SYSTEM.md, and BUILD_PROMPT.txt
"""

import logging
from typing import Dict, Tuple
from ai_client import AIClient
from research import WebResearcher
from prompts import (
    EXTRACT_BUSINESS_INFO_PROMPT,
    GENERATE_PLAN_PROMPT,
    GENERATE_DESIGN_SYSTEM_PROMPT,
    GENERATE_BUILD_PROMPT_PROMPT
)

logger = logging.getLogger(__name__)


class LandingPageGenerator:
    """Generates landing page documents from business briefs."""

    def __init__(self):
        self.ai = AIClient()
        self.researcher = WebResearcher()

    async def extract_business_info(self, user_input: str) -> Dict:
        """Extract structured business info from free-form input."""
        prompt = EXTRACT_BUSINESS_INFO_PROMPT.format(user_input=user_input)
        response = await self.ai.generate(prompt, max_tokens=1000, temperature=0.3)

        # Parse the structured response
        info = {}
        for line in response.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                if value and value.upper() != "NOT PROVIDED":
                    info[key] = value

        return info

    async def perform_research(self, business_info: Dict) -> Dict:
        """Perform web research on the business."""
        logger.info("Starting web research...")

        research = self.researcher.research_business({
            "name": business_info.get("business_name", ""),
            "website": business_info.get("website", ""),
            "industry": business_info.get("industry", ""),
            "location": business_info.get("location", "")
        })

        logger.info(f"Research complete. Sources found: {len(research.get('sources', []))}")
        return research

    async def generate_plan(self, business_info: Dict, research: Dict) -> str:
        """Generate PLAN.md document."""
        logger.info("Generating PLAN.md...")

        # Format business info as text
        business_text = "\n".join([
            f"**{k.replace('_', ' ').title()}**: {v}"
            for k, v in business_info.items()
        ])

        # Format research for prompt
        research_text = self.researcher.format_research_for_prompt(research)

        prompt = GENERATE_PLAN_PROMPT.format(
            business_info=business_text,
            research=research_text
        )

        # Generate plan
        plan = await self.ai.generate(prompt, max_tokens=8000, temperature=0.7)

        logger.info("PLAN.md generated")
        return plan

    async def generate_design_system(self, business_info: Dict) -> str:
        """Generate DESIGN_SYSTEM.md document."""
        logger.info("Generating DESIGN_SYSTEM.md...")

        # Format business info
        business_text = "\n".join([
            f"**{k.replace('_', ' ').title()}**: {v}"
            for k, v in business_info.items()
        ])

        prompt = GENERATE_DESIGN_SYSTEM_PROMPT.format(
            business_info=business_text,
            tone=business_info.get("brand_tone", "professional"),
            industry=business_info.get("industry", "general"),
            target=business_info.get("target_customer", "general audience")
        )

        design_system = await self.ai.generate(prompt, max_tokens=4000, temperature=0.6)

        logger.info("DESIGN_SYSTEM.md generated")
        return design_system

    async def generate_build_prompt(self, plan: str, design_system: str) -> str:
        """Generate BUILD_PROMPT.txt document."""
        logger.info("Generating BUILD_PROMPT.txt...")

        prompt = GENERATE_BUILD_PROMPT_PROMPT.format(
            plan=plan,
            design_system=design_system
        )

        build_prompt = await self.ai.generate(prompt, max_tokens=6000, temperature=0.5)

        logger.info("BUILD_PROMPT.txt generated")
        return build_prompt

    async def generate_all(self, user_input: str, progress_callback=None) -> Tuple[str, str, str, Dict]:
        """
        Generate all three documents from user input.

        Args:
            user_input: The user's business brief
            progress_callback: Optional async function to call with progress updates

        Returns:
            Tuple of (plan, design_system, build_prompt, business_info)
        """
        async def update(msg):
            if progress_callback:
                await progress_callback(msg)

        # Step 1: Extract business info
        await update("📋 Analyzing your business brief...")
        business_info = await self.extract_business_info(user_input)
        await update(f"✅ Extracted info for: {business_info.get('business_name', 'your business')}")

        # Step 2: Perform research
        await update("🔍 Researching your industry and competitors...")
        research = await self.perform_research(business_info)
        source_count = len(research.get('sources', []))
        await update(f"✅ Research complete ({source_count} sources found)")

        # Step 3: Generate PLAN.md
        await update("📝 Writing PLAN.md (landing page blueprint)...")
        plan = await self.generate_plan(business_info, research)
        await update("✅ PLAN.md complete")

        # Step 4: Generate DESIGN_SYSTEM.md
        await update("🎨 Creating DESIGN_SYSTEM.md (visual direction)...")
        design_system = await self.generate_design_system(business_info)
        await update("✅ DESIGN_SYSTEM.md complete")

        # Step 5: Generate BUILD_PROMPT.txt
        await update("🛠️ Writing BUILD_PROMPT.txt (vibecoding prompt)...")
        build_prompt = await self.generate_build_prompt(plan, design_system)
        await update("✅ BUILD_PROMPT.txt complete")

        return plan, design_system, build_prompt, business_info

    def close(self):
        """Clean up resources."""
        self.researcher.close()
