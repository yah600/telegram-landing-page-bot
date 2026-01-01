# Telegram Business Research Agent

AI agent that researches businesses and generates website prompts for Figma Make or v0.

## Setup

### 1. Create a Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow prompts to name your bot
4. Copy the API token

### 2. Install Dependencies

```bash
cd /Users/justinleanca/Documents/GitHub/telegram-research-agent
pip3 install -r requirements.txt
```

### 3. Set Environment Variables

```bash
export TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 4. Run the Bot

```bash
python3 agent.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start`
3. Send business information (name, description, target audience, etc.)
4. Wait for research to complete
5. Use `/v0` or `/figma` to generate website prompts

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Start new session |
| `/help` | Show help |
| `/v0` | Generate v0.dev prompt |
| `/figma` | Generate Figma Make prompt |
| `/status` | Check session status |
| `/clear` | Clear session |
