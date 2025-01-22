from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import imdb
import os
import logging

 
# Initialize IMDb instance
ia = imdb.IMDb()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Command handler functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I am your Movie Bot.\n\n"
        "\nCommands:\n"
        "/movie <movie_name> - Get details about a movie\n"
        "\n/genre <genre_name> - Get movie suggestions by genre\n"
        "\n\nExample: /movie Inception or /genre Action"
    )

async def movie_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a movie name after the /movie command.")
        return
    await update.message.reply_text(f"Searching for {context.args[0]}... Please wait.")
    movie_name = ' '.join(context.args)
    try:
        movies = ia.search_movie(movie_name)
        if movies:
            movie = movies[0]
            movie_id = movie.getID()
            movie_details = ia.get_movie(movie_id)

            movie_info = f"Title: {movie_details['title']}\n"
            movie_info += f"Year: {movie_details['year']}\n"
            movie_info += f"Rating: {movie_details.get('rating', 'N/A')}\n"
            movie_info += f"Genres: {', '.join(movie_details.get('genres', []))}\n"
            movie_info += f"Plot: {movie_details.get('plot', ['No plot available'])[0]}\n"
            await update.message.reply_text(movie_info)
        else:
            await update.message.reply_text("Sorry, no movie found with that name.")
    except Exception as e:
        logger.error(f"Error searching for movie: {e}")
        await update.message.reply_text("Oops! Something went wrong while searching for the movie.")

async def suggest_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Please provide a genre after the /genre command. Example: /genre Action"
        )
        return

    genre = ' '.join(context.args).lower()
    genre_map = {
        "action": "Action",
        "comedy": "Comedy",
        "drama": "Drama",
        "romance": "Romance",
        "thriller": "Thriller",
        "horror": "Horror",
        "sci-fi": "Sci-Fi",
        "adventure": "Adventure",
    }

    if genre not in genre_map:
        await update.message.reply_text(
            "Invalid genre. Please choose from: Action, Comedy, Drama, Romance, Thriller, Horror, Sci-Fi, Adventure."
        )
        return

    genre_name = genre_map[genre]
    await update.message.reply_text(f"Fetching popular {genre_name} movies...")

    try:
        top_movies = ia.get_top250_movies()
        suggested_movies = [
            f"{movie['title']} ({movie['year']})"
            for movie in top_movies
            if genre_name in ia.get_movie(movie.getID()).get('genres', [])
        ][:5]  # Limit to 5 suggestions

        if suggested_movies:
            await update.message.reply_text("\n".join(suggested_movies))
        else:
            await update.message.reply_text(f"No popular {genre_name} movies found.")
    except Exception as e:
        logger.error(f"Error suggesting movies by genre: {e}")
        await update.message.reply_text("Oops! Something went wrong while fetching movie suggestions.")

        # Example of setting a timezone
    


def main() -> None:
    """Run the bot."""
    # Replace with your bot token
    token = "7414428296:AAGjNvEhKBCOMmvg7ut2qWWJwwMKibNsDgQ"
    print(f"Bot token: {token}")
    if not token:
        logger.error("Bot token not found. Please set TELEGRAM_BOT_TOKEN environment variable.")
        return
    # Initialize bot with timezone
    application = ApplicationBuilder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movie", movie_search))
    application.add_handler(CommandHandler("genre", suggest_movies))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
