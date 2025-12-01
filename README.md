# Discord Bot

A simple Discord bot with slash commands built using python.

## Features

- Slash commands support
- Hello command
- Ping command to check bot latency

## Setup

1. Clone this repository:
```bash
git clone https://github.com/xangeyfun/discord-bot.git
cd discord-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your bot credentials:
```
BOT_TOKEN=your_bot_token_here
APPLICATION_ID=your_application_id_here
```

4. Run the bot:
```bash
python3 bot.py
```

## Commands

- `/hello` - Say hello to the bot
- `/ping` - Check the bot's latency

## Requirements

- Python 3.x
- discord.py
- python-dotenv

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
