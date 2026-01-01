#!/usr/bin/env python3
"""
Landing Page Maker - Telegram Bot

Fully automated: Business brief → Research → Generate → Deploy → Live URL
"""

import asyncio
import os
import io
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(
    WAITING_NAME,
    WAITING_WEBSITE,
    WAITING_INDUSTRY,
    WAITING_TARGET,
    WAITING_OFFER,
    WAITING_GOAL,
    WAITING_TONE,
    WAITING_COLORS,
    WAITING_EXAMPLES,
    WAITING_ADDITIONAL,
    PROCESSING
) = range(11)

# Store user sessions
user_sessions = {}

# Lazy load modules
_generator = None
_code_generator = None
_deployer = None
_verifier = None


def get_generator():
    global _generator
    if _generator is None:
        from generators import LandingPageGenerator
        _generator = LandingPageGenerator()
    return _generator


def get_code_generator():
    global _code_generator
    if _code_generator is None:
        from code_generator import CodeGenerator
        _code_generator = CodeGenerator()
    return _code_generator


def get_deployer():
    global _deployer
    if _deployer is None:
        from deployer import CloudflareDeployer
        _deployer = CloudflareDeployer()
    return _deployer


def get_verifier():
    global _verifier
    if _verifier is None:
        from deployer import SiteVerifier
        _verifier = SiteVerifier()
    return _verifier


# ============== COMMAND HANDLERS ==============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Welcome message with options."""
    user_id = update.effective_user.id
    user_sessions[user_id] = {"mode": None, "data": {}}

    deployer = get_deployer()
    deploy_status = "✅" if deployer.is_configured else "❌"

    keyboard = [
        [InlineKeyboardButton("📝 Paste Everything", callback_data="mode_freeform")],
        [InlineKeyboardButton("💬 Guided Questions", callback_data="mode_guided")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome = f"""🚀 **Landing Page Maker**

Send me your business info and I'll create a **live website** for you!

**Fully Automated Pipeline:**
1. 🔍 Research your industry & competitors
2. 📋 Create conversion-focused plan
3. 🎨 Design system & branding
4. 💻 Generate full website code
5. 🌐 Deploy to Cloudflare Pages
6. 🔗 Send you the live URL

**Status:**
• DeepSeek (code): ✅
• Groq (research): ✅
• Cloudflare: {deploy_status}

**Choose input method:**"""

    await update.message.reply_text(welcome, reply_markup=reply_markup, parse_mode='Markdown')
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help."""
    help_text = """**Commands:**
/start - Create new landing page
/status - Check session
/clear - Clear session

**What to provide:**
• Business name & website
• Industry/niche
• Target customer
• Main offer/product
• Page goal (leads, sales, bookings)
• Brand tone & colors

**What you get:**
• PLAN.md - Page blueprint
• DESIGN_SYSTEM.md - Visual guide
• index.html - Full website code
• **LIVE URL** - Deployed website!

**Powered by:**
DeepSeek + Groq + Cloudflare (all free)"""

    await update.message.reply_text(help_text, parse_mode='Markdown')


async def clear_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Clear user session."""
    user_id = update.effective_user.id
    user_sessions[user_id] = {"mode": None, "data": {}}
    await update.message.reply_text("✅ Session cleared. Use /start to begin.")
    return ConversationHandler.END


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show session status."""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id, {})

    if not session.get("data"):
        await update.message.reply_text("📭 No active session. Use /start to begin.")
    else:
        url = session.get("deployed_url", "Not deployed yet")
        await update.message.reply_text(f"Session active.\nLast URL: {url}")


# ============== MODE SELECTION ==============

async def mode_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle mode selection."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    mode = query.data

    if mode == "mode_freeform":
        user_sessions[user_id] = {"mode": "freeform", "data": {}}
        await query.edit_message_text(
            "📝 **Paste your business info:**\n\n"
            "Include as much as possible:\n"
            "• Business name & website URL\n"
            "• Industry/niche\n"
            "• Target customer\n"
            "• What you sell/offer\n"
            "• Goal (leads, sales, bookings)\n"
            "• Brand tone (professional, fun, etc.)\n"
            "• Colors (if you have them)\n"
            "• Sites you like the style of\n\n"
            "**Send it all in one message:**",
            parse_mode='Markdown'
        )
        return PROCESSING

    elif mode == "mode_guided":
        user_sessions[user_id] = {"mode": "guided", "data": {}}
        await query.edit_message_text(
            "💬 **Guided Mode**\n\n"
            "I'll ask questions one by one.\n"
            "Type 'skip' to skip any question.\n\n"
            "**Question 1/10:** What is your business name?",
            parse_mode='Markdown'
        )
        return WAITING_NAME

    return ConversationHandler.END


# ============== GUIDED MODE ==============

async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["business_name"] = update.message.text
    await update.message.reply_text("**Q2/10:** Website URL? (or 'skip')", parse_mode='Markdown')
    return WAITING_WEBSITE

async def receive_website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["website"] = update.message.text
    await update.message.reply_text("**Q3/10:** What industry/niche?", parse_mode='Markdown')
    return WAITING_INDUSTRY

async def receive_industry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["industry"] = update.message.text
    await update.message.reply_text("**Q4/10:** Who is your target customer?", parse_mode='Markdown')
    return WAITING_TARGET

async def receive_target(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["target_customer"] = update.message.text
    await update.message.reply_text("**Q5/10:** What do you sell/offer?", parse_mode='Markdown')
    return WAITING_OFFER

async def receive_offer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["main_offer"] = update.message.text
    await update.message.reply_text("**Q6/10:** Goal of the page? (leads, sales, bookings)", parse_mode='Markdown')
    return WAITING_GOAL

async def receive_goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["page_goal"] = update.message.text
    await update.message.reply_text("**Q7/10:** Brand tone? (professional, friendly, luxurious, playful)", parse_mode='Markdown')
    return WAITING_TONE

async def receive_tone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["brand_tone"] = update.message.text
    await update.message.reply_text("**Q8/10:** Brand colors? (e.g., 'blue #1a73e8, white')", parse_mode='Markdown')
    return WAITING_COLORS

async def receive_colors(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["colors"] = update.message.text
    await update.message.reply_text("**Q9/10:** Sites you like the style of?", parse_mode='Markdown')
    return WAITING_EXAMPLES

async def receive_examples(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["example_sites"] = update.message.text
    await update.message.reply_text("**Q10/10:** Anything else important?", parse_mode='Markdown')
    return WAITING_ADDITIONAL

async def receive_additional(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if update.message.text.lower() != 'skip':
        user_sessions[user_id]["data"]["additional"] = update.message.text

    data = user_sessions[user_id]["data"]
    brief = "\n".join([f"{k}: {v}" for k, v in data.items() if v])

    await update.message.reply_text("✅ Got it! Starting generation...")
    await process_and_deploy(update, context, brief)
    return ConversationHandler.END


# ============== MAIN PROCESSING ==============

async def handle_freeform(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle free-form input."""
    user_id = update.effective_user.id
    session = user_sessions.get(user_id, {})

    if session.get("mode") != "freeform":
        await update.message.reply_text("Use /start to begin.")
        return ConversationHandler.END

    brief = update.message.text
    await process_and_deploy(update, context, brief)
    return ConversationHandler.END


async def process_and_deploy(update: Update, context: ContextTypes.DEFAULT_TYPE, brief: str) -> None:
    """Full pipeline: research → plan → code → deploy → send URL."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    status_msg = await update.message.reply_text(
        "🚀 **Starting Full Pipeline**\n\n"
        "⏳ Step 1/6: Analyzing business info...",
        parse_mode='Markdown'
    )

    async def update_status(step: int, msg: str):
        try:
            await status_msg.edit_text(
                f"🚀 **Building Your Website**\n\n"
                f"{'✅' if step > 1 else '⏳'} Step 1/6: Analyze business\n"
                f"{'✅' if step > 2 else '⏳' if step >= 2 else '⬜'} Step 2/6: Research industry\n"
                f"{'✅' if step > 3 else '⏳' if step >= 3 else '⬜'} Step 3/6: Create plan\n"
                f"{'✅' if step > 4 else '⏳' if step >= 4 else '⬜'} Step 4/6: Design system\n"
                f"{'✅' if step > 5 else '⏳' if step >= 5 else '⬜'} Step 5/6: Generate code\n"
                f"{'✅' if step > 6 else '⏳' if step >= 6 else '⬜'} Step 6/6: Deploy\n\n"
                f"📍 {msg}",
                parse_mode='Markdown'
            )
        except:
            pass

    try:
        # Step 1-4: Generate plan and design system
        await update_status(1, "Extracting business info...")
        generator = get_generator()

        # Custom progress callback
        current_step = [1]
        async def gen_progress(msg):
            if "research" in msg.lower():
                current_step[0] = 2
            elif "plan" in msg.lower():
                current_step[0] = 3
            elif "design" in msg.lower():
                current_step[0] = 4
            await update_status(current_step[0], msg)

        plan, design_system, _, business_info = await generator.generate_all(brief, gen_progress)

        # Step 5: Generate website code
        await update_status(5, "Generating website with DeepSeek...")
        code_gen = get_code_generator()

        business_text = "\n".join([f"{k}: {v}" for k, v in business_info.items()])

        async def code_progress(msg):
            await update_status(5, msg)

        react_code = await code_gen.generate_website(business_text, plan, design_system, code_progress)

        # Step 6: Deploy to CodeSandbox
        await update_status(6, "Creating CodeSandbox...")

        from codesandbox_deployer import CodeSandboxDeployer
        deployer = CodeSandboxDeployer()

        business_name = business_info.get('business_name', 'Landing Page')
        files = deployer.create_next_project(react_code, business_name)
        deployment = await deployer.deploy(files, business_name)

        sandbox_url = deployment.get("editor_url", "")
        preview_url = deployment.get("preview_url", "")

        # Send files
        await update_status(7, "Sending files...")

        react_file = io.BytesIO(react_code.encode('utf-8'))
        react_file.name = "LandingPage.jsx"
        await context.bot.send_document(chat_id=chat_id, document=react_file, caption="React Component")

        # Final message with links
        await status_msg.edit_text(
            f"React Landing Page Ready!\n\n"
            f"Editor: {sandbox_url}\n\n"
            f"Preview: {preview_url}\n\n"
            f"Use /start to create another."
        )

    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        error_msg = str(e)[:200]
        await status_msg.edit_text(
            f"Error: {error_msg}\n\nPlease try /start again."
        )


# ============== MAIN ==============

def main() -> None:
    """Start the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    cf_token = os.getenv("CLOUDFLARE_API_TOKEN")
    cf_account = os.getenv("CLOUDFLARE_ACCOUNT_ID")

    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not set")
        return

    if not deepseek_key and not groq_key and not gemini_key:
        print("❌ No AI provider configured")
        return

    print("🚀 Starting Landing Page Maker...")
    print(f"   DeepSeek: {'✅' if deepseek_key else '❌'}")
    print(f"   Groq: {'✅' if groq_key else '❌'}")
    print(f"   Gemini: {'✅' if gemini_key else '❌'}")
    print(f"   Cloudflare: {'✅' if (cf_token and cf_account) else '❌'}")

    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(mode_selection, pattern="^mode_"),
        ],
        states={
            WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            WAITING_WEBSITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_website)],
            WAITING_INDUSTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_industry)],
            WAITING_TARGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_target)],
            WAITING_OFFER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_offer)],
            WAITING_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_goal)],
            WAITING_TONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_tone)],
            WAITING_COLORS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_colors)],
            WAITING_EXAMPLES: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_examples)],
            WAITING_ADDITIONAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_additional)],
            PROCESSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_freeform)],
        },
        fallbacks=[CommandHandler("clear", clear_session), CommandHandler("start", start)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("clear", clear_session))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_freeform))

    print("✅ Bot running!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
