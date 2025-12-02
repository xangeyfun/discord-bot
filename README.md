# Discord Bot

A simple Discord bot made to learn the discord.py library.

## Features

- Simple easy to read code
- Slash command support
- Some basic commands

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
TOKEN=your_bot_token_here
APPLICATION_ID=your_application_id_here
GUILD=your_guild_id_here
ALLOWED_USER_ID=your_user_id_here
```

4. Run the bot:
```bash
python3 bot.py
```

## Commands

- `/ping` - test the bot's latency
- `/calc` - evaluate a simple expression
- `/flip` - flip a coin
- `/github` - link to the source code
- `/rps` - Rock Paper Siccors
- `/random` - Generate a random number
- `/userinfo` - Get info about a user
- `/token` - get the bot token (admin only)

## Requirements

- Python 3.x
- discord.py
- python-dotenv

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
