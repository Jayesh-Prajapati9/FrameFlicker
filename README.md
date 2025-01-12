# 🎬 FrameFlicker

A Python-based Telegram bot that helps users discover and fetch information about movies using the IMDb API.

## ✨ Features

- 🔍 Search movies by title
- 📊 Get detailed movie information (rating, year, plot)
- 🎭 Browse movies by genre
- 📈 View IMDb top-rated movies

## 🛠️ Requirements

- Python 3.9+
- `python-telegram-bot`
- `IMDbPY`

## 🚀 Installation

1. Clone this repository

```bash
git clone https://github.com/yourusername/telegram-movie-bot.git
```

2. Install required packages:

```sh
pip install python-telegram-bot imdbpy
```

3. Configure bot token

- Get your bot token from [@BotFather](https://t.me/botfather)
- Replace YOUR_BOT_TOKEN in the code

4. Run the bot:

```sh
pip install python-telegram-bot imdbpy
```

## 📖 Usage

#### The bot supports the following commands:

- `/start` - Get welcome message and instructions
- `/movie <title>` - Search for a specific movie
- `/genre <type>` - Get movie suggestions by genre

Example:

```markdown
/movie Inception
/genre Action
```

## 📜 License

- This project is licensed under the MIT License - see the LICENSE file for details.
