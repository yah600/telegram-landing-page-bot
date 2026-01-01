#!/usr/bin/env python3
"""
Telegram Business Research Agent

Receives business info via Telegram, performs deep research using Groq (free),
and generates website creation prompts for Figma Make or v0.
"""

import asyncio
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
from duckduckgo_search import DDGS

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store conversation state per user
user_sessions = {}


class BusinessResearchAgent:
    """Agent that researches businesses and generates website prompts."""

    def __init__(self):
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"  # Free, powerful model

    def web_search(self, query: str, max_results: int = 10) -> str:
        """Perform web search using DuckDuckGo (free)."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))

            if not results:
                return "No search results found."

            formatted = []
            for r in results:
                formatted.append(f"**{r['title']}**\n{r['body']}\nURL: {r['href']}\n")

            return "\n".join(formatted)
        except Exception as e:
            logger.error(f"Search error: {e}")
            return f"Search failed: {str(e)}"

    async def research_business(self, business_info: str) -> dict:
        """
        Perform deep research on a business and generate insights.
        """
        # Step 1: Extract key info and search queries
        extraction_prompt = f"""Analyze this business info and extract:
1. Business name
2. Industry/niche
3. Location (if mentioned)
4. 3 search queries to research competitors and industry trends

Business info: {business_info}

Respond in this format:
BUSINESS_NAME: [name]
INDUSTRY: [industry]
LOCATION: [location or "not specified"]
SEARCH_1: [first search query]
SEARCH_2: [second search query]
SEARCH_3: [third search query]"""

        extraction = self.groq.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": extraction_prompt}],
            max_tokens=500
        )

        extracted = extraction.choices[0].message.content

        # Step 2: Perform web searches
        search_results = []
        lines = extracted.split('\n')
        for line in lines:
            if line.startswith('SEARCH_'):
                query = line.split(':', 1)[-1].strip()
                if query:
                    logger.info(f"Searching: {query}")
                    results = self.web_search(query, max_results=5)
                    search_results.append(f"### Search: {query}\n{results}")

        web_research = "\n\n".join(search_results) if search_results else "No web research performed."

        # Step 3: Deep analysis with all gathered info
        research_prompt = f"""You are a business research expert. Analyze the following business information and web research to provide comprehensive insights.

## BUSINESS INFO PROVIDED:
{business_info}

## EXTRACTED INFO:
{extracted}

## WEB RESEARCH RESULTS:
{web_research}

Based on all this information, provide a detailed analysis:

## 1. Business Overview
- Industry classification and market positioning
- Target market and demographics
- Unique value proposition
- Key competitors identified from research

## 2. Brand Analysis
- Suggested brand personality (professional, playful, luxurious, etc.)
- Color psychology recommendations with specific hex codes
- Typography style suggestions
- Visual style direction

## 3. Website Requirements
- Essential pages needed
- Key features and functionality
- Call-to-action priorities
- Content sections to include

## 4. User Experience Insights
- Primary user goals
- User journey considerations
- Trust signals needed
- Mobile-first considerations

## 5. Industry Best Practices
- What successful competitors do well (based on research)
- Common patterns in this industry
- Current trends to incorporate
- Things to avoid

## 6. Competitive Insights
- Key differentiators to highlight
- Gaps in competitor offerings
- Opportunities for this business

Provide detailed, actionable insights that can be used to create an effective website."""

        response = self.groq.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": research_prompt}],
            max_tokens=4096
        )

        return {
            "research": response.choices[0].message.content,
            "business_info": business_info,
            "web_research": web_research
        }

    async def generate_website_prompt(self, research_data: dict, platform: str = "v0") -> str:
        """
        Generate a detailed website creation prompt for Figma Make or v0.
        """
        if platform.lower() == "figma":
            platform_instructions = """Generate a prompt for Figma Make that:
- Describes the exact layout and component structure
- Specifies design tokens (colors, spacing, typography)
- Includes component hierarchy and naming
- Provides detailed styling instructions
- Uses Figma-specific terminology"""
        else:  # v0
            platform_instructions = """Generate a prompt for v0.dev that:
- Describes the React/Next.js components needed
- Specifies Tailwind CSS styling preferences
- Includes responsive design requirements
- Provides clear visual hierarchy instructions
- Uses shadcn/ui components where appropriate"""

        generation_prompt = f"""Based on this business research, create a comprehensive website generation prompt.

## RESEARCH DATA:
{research_data['research']}

## ORIGINAL BUSINESS INFO:
{research_data['business_info']}

## PLATFORM REQUIREMENTS:
{platform_instructions}

Create an extremely detailed prompt that will generate a professional, conversion-optimized website. The prompt should be:

### 1. HIGHLY SPECIFIC - Include exact details about:
- Page structure and sections
- Visual hierarchy
- Color palette with hex codes
- Typography choices (font families, sizes, weights)
- Spacing and layout (use specific values)
- Interactive elements
- Animations/transitions
- Image placeholders and descriptions

### 2. CONVERSION-FOCUSED - Emphasize:
- Clear call-to-actions with specific text
- Trust signals (testimonials, badges, guarantees)
- Social proof sections
- Contact/lead capture forms
- Value proposition visibility above the fold

### 3. BRAND-ALIGNED - Reflect:
- The business personality throughout
- Industry expectations
- Target audience preferences
- Competitive differentiation

### 4. TECHNICALLY COMPLETE - Specify:
- All pages needed (list each one)
- Navigation structure
- Footer content and links
- Mobile responsiveness breakpoints
- Accessibility considerations

Format the output as a single, copy-paste ready prompt for {platform}. Start the prompt with "Create a..." and make it comprehensive enough to generate a complete, professional website."""

        response = self.groq.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": generation_prompt}],
            max_tokens=8000
        )

        return response.choices[0].message.content


# Initialize the agent
agent = None


def get_agent():
    global agent
    if agent is None:
        agent = BusinessResearchAgent()
    return agent


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    user_sessions[user_id] = {"state": "waiting_for_info", "data": {}}

    welcome_message = """🚀 Welcome to the Business Website Prompt Generator!

I'll help you create a perfect website prompt for Figma Make or v0.

**How it works:**
1. Send me information about your business
2. I'll perform deep web research on your industry
3. You'll receive a detailed prompt to generate your website

**What to include:**
- Business name and description
- Products/services offered
- Target audience
- Any existing branding (colors, style preferences)
- Website goals (leads, sales, information)
- Competitors or websites you like

Send me your business information to get started!"""

    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """**Commands:**
/start - Start a new research session
/v0 - Generate prompt for v0.dev
/figma - Generate prompt for Figma Make
/status - Check current session status
/clear - Clear current session and start over

**Tips for best results:**
- Be detailed about your business
- Include your target audience
- Mention any style preferences
- Share competitor websites you like

**Powered by:**
- Groq (Llama 3.3 70B) - Free AI
- DuckDuckGo - Free web search"""

    await update.message.reply_text(help_text, parse_mode='Markdown')


async def clear_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear the user's session."""
    user_id = update.effective_user.id
    user_sessions[user_id] = {"state": "waiting_for_info", "data": {}}
    await update.message.reply_text("✅ Session cleared! Send me new business information to start fresh.")


async def generate_v0_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a v0 prompt from researched data."""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id, {})

    if "research" not in session.get("data", {}):
        await update.message.reply_text("❌ No research data found. Please send your business information first!")
        return

    await update.message.reply_text("⏳ Generating v0 prompt... This may take a moment.")

    try:
        prompt = await get_agent().generate_website_prompt(session["data"]["research"], "v0")

        # Split long messages if needed (Telegram has 4096 char limit)
        if len(prompt) > 4000:
            chunks = [prompt[i:i+4000] for i in range(0, len(prompt), 4000)]
            await update.message.reply_text("**✅ v0.dev Website Prompt:**\n\n(Split into parts due to length)")
            for i, chunk in enumerate(chunks):
                await update.message.reply_text(f"**Part {i+1}:**\n\n{chunk}")
        else:
            await update.message.reply_text(f"**✅ v0.dev Website Prompt:**\n\n{prompt}")
    except Exception as e:
        logger.error(f"Error generating v0 prompt: {e}")
        await update.message.reply_text(f"❌ Error generating prompt: {str(e)}")


async def generate_figma_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a Figma Make prompt from researched data."""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id, {})

    if "research" not in session.get("data", {}):
        await update.message.reply_text("❌ No research data found. Please send your business information first!")
        return

    await update.message.reply_text("⏳ Generating Figma Make prompt... This may take a moment.")

    try:
        prompt = await get_agent().generate_website_prompt(session["data"]["research"], "figma")

        if len(prompt) > 4000:
            chunks = [prompt[i:i+4000] for i in range(0, len(prompt), 4000)]
            await update.message.reply_text("**✅ Figma Make Website Prompt:**\n\n(Split into parts due to length)")
            for i, chunk in enumerate(chunks):
                await update.message.reply_text(f"**Part {i+1}:**\n\n{chunk}")
        else:
            await update.message.reply_text(f"**✅ Figma Make Website Prompt:**\n\n{prompt}")
    except Exception as e:
        logger.error(f"Error generating Figma prompt: {e}")
        await update.message.reply_text(f"❌ Error generating prompt: {str(e)}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming business information."""
    user_id = update.effective_user.id
    message_text = update.message.text

    # Initialize session if needed
    if user_id not in user_sessions:
        user_sessions[user_id] = {"state": "waiting_for_info", "data": {}}

    session = user_sessions[user_id]

    await update.message.reply_text(
        "📥 Received your business information!\n\n"
        "🔍 Starting deep research...\n"
        "• Analyzing your business\n"
        "• Searching competitors & trends\n"
        "• Gathering industry insights\n\n"
        "⏳ This typically takes 30-60 seconds. Please wait."
    )

    try:
        # Perform research
        research_data = await get_agent().research_business(message_text)

        # Store research results
        session["data"]["research"] = research_data
        session["state"] = "research_complete"

        # Send research summary
        research_summary = research_data["research"]

        if len(research_summary) > 4000:
            chunks = [research_summary[i:i+4000] for i in range(0, len(research_summary), 4000)]
            await update.message.reply_text("**✅ Research Complete!**\n\n(Results split into parts)")
            for i, chunk in enumerate(chunks):
                await update.message.reply_text(f"**Part {i+1}:**\n\n{chunk}")
        else:
            await update.message.reply_text(f"**✅ Research Complete!**\n\n{research_summary}")

        await update.message.reply_text(
            "**🎯 Next Steps:**\n"
            "• Use /v0 to generate a prompt for v0.dev\n"
            "• Use /figma to generate a prompt for Figma Make\n"
            "• Use /clear to start over with new business info"
        )

    except Exception as e:
        logger.error(f"Error during research: {e}")
        await update.message.reply_text(
            f"❌ Error during research: {str(e)}\n\n"
            "Please try again or use /clear to start over."
        )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current session status."""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id, {})

    if not session or session.get("state") == "waiting_for_info":
        await update.message.reply_text("📭 No active research. Send me business information to get started!")
    elif session.get("state") == "research_complete":
        await update.message.reply_text(
            "✅ Research complete and ready!\n\n"
            "Use /v0 or /figma to generate your website prompt."
        )


def main() -> None:
    """Start the bot."""
    # Check for required environment variables
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    groq_key = os.getenv("GROQ_API_KEY")

    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("\nTo get a token:")
        print("1. Message @BotFather on Telegram")
        print("2. Send /newbot and follow the prompts")
        print("3. Copy the token and set it:")
        print("   export TELEGRAM_BOT_TOKEN='your-token-here'")
        return

    if not groq_key:
        print("❌ Error: GROQ_API_KEY environment variable not set!")
        print("\nTo get a FREE Groq API key:")
        print("1. Go to https://console.groq.com")
        print("2. Sign up (free)")
        print("3. Create an API key")
        print("4. Set it:")
        print("   export GROQ_API_KEY='your-key-here'")
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_session))
    application.add_handler(CommandHandler("v0", generate_v0_prompt))
    application.add_handler(CommandHandler("figma", generate_figma_prompt))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    print("🚀 Bot starting... Press Ctrl+C to stop.")
    print("✅ Using Groq (Llama 3.3 70B) - FREE")
    print("✅ Using DuckDuckGo for web search - FREE")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
