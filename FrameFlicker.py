import time
import requests
import logging
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


#  LOGGING LEVELS ARE DEBUG (lowest), INFO, WARNING, ERROR, and CRITICAL (highest).
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

API_KEY = ""    
BASE_URL = "http://www.omdbapi.com/"

def search_movies(title):
    url = f"{BASE_URL}?s={title}&type=movie&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            logger.info(f"Found {len(data['Search'])} movies for '{title}'")
            return [
                 {"title": movie["Title"], "year": movie["Year"], "imdb_id": movie["imdbID"]}
                for movie in data["Search"][:5]
            ]
        else:
            logger.warning(f"Search failed: {data.get('Error')}")
            return f"Error: {data.get('Error', 'Unknown error')}"
    except requests.RequestException as e:
        logger.error(f"Search request failed: {e}")
        return f"Error: {str(e)}"

def get_movie_by_title(title, full_plot=False):
    movie_title = open(f"{title}.txt", "w")
    plot = "full" if full_plot else "short"
    url = f"{BASE_URL}?t={title}&plot={plot}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            logger.info(f"Fetched details for '{title}'")
            movie_title.write(f"Title: {data.get('Title', 'N/A')}\n")
            movie_title.write(f"Year: {data.get('Year', 'N/A')}\n")
            movie_title.write(f"Released: {data.get('Released', 'N/A')}\n")
            movie_title.write(f"Genre: {data.get('Genre', 'N/A')}\n")
            movie_title.write(f"Director: {data.get('Director', 'N/A')}\n")
            movie_title.write(f"Actors: {data.get('Actors', 'N/A')}\n")
            movie_title.write(f"Plot: {data.get('Plot', 'N/A')}\n")
            movie_title.write(f"IMDb Rating: {data.get('imdbRating', 'N/A')}\n")
            movie_title.write(f"Runtime: {data.get('Runtime', 'N/A')}\n")
            movie_title.write(f"IMDb ID: {data.get('imdbID', 'N/A')}\n")
            movie_title.close()
            return {
                "title": data.get("Title", "N/A"),
                "year": data.get("Year", "N/A"),
                "released": data.get("Released", "N/A"),
                "genre": data.get("Genre", "N/A"),
                "director": data.get("Director", "N/A"),
                "actors": data.get("Actors", "N/A"),
                "plot": data.get("Plot", "N/A"),
                "imdb_rating": data.get("imdbRating", "N/A"),
                "runtime": data.get("Runtime", "N/A"),
                "imdb_id": data.get("imdbID", "N/A")
            }
        else:
            logger.warning(f"Movie details failed: {data.get('Error')}")
            return f"Error: {data.get('Error', 'Unknown error')}"
    except requests.RequestException as e:
        logger.error(f"Movie details request failed: {e}")
        return f"Error: {str(e)}"

def get_movie_by_imdb_id(imdb_id):
    url = f"{BASE_URL}?i={imdb_id}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        
        # IT IS FOR THE STATUS CODE RETURNING FROM THE API REQUEST
        response.raise_for_status()  
        
        data = response.json()
        if data.get("Response") == "True":
            logger.info(f"Fetched details for IMDb ID '{imdb_id}'")
            return {
                "title": data.get("Title", "N/A"),
                "year": data.get("Year", "N/A"),
                "released": data.get("Released", "N/A"),
                "genre": data.get("Genre", "N/A"),
                "director": data.get("Director", "N/A"),
                "actors": data.get("Actors", "N/A"),
                "plot": data.get("Plot", "N/A"),
                "imdb_rating": data.get("imdbRating", "N/A"),
                "runtime": data.get("Runtime", "N/A"),
                "imdb_id": data.get("imdbID", "N/A")
            }
        else:
            logger.warning(f"IMDb ID lookup failed: {data.get('Error')}")
            return f"Error: {data.get('Error', 'Unknown error')}"
    except requests.RequestException as e:
        logger.error(f"IMDb ID request failed: {e}")
        return f"Error: {str(e)}"

def get_series_episode(series_title, season, episode):
    url = f"{BASE_URL}?t={series_title}&Season={season}&Episode={episode}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            logger.info(f"Fetched episode S{season}E{episode} for '{series_title}'")
            return {
                "series_title": series_title,
                "season": data.get("Season", "N/A"),
                "episode": data.get("Episode", "N/A"),
                "title": data.get("Title", "N/A"),
                "released": data.get("Released", "N/A"),
                "plot": data.get("Plot", "N/A"),
                "imdb_rating": data.get("imdbRating", "N/A")
            }
        else:
            logger.warning(f"Episode lookup failed: {data.get('Error')}")
            return f"Error: {data.get('Error', 'Unknown error')}"
    except requests.RequestException as e:
        logger.error(f"Episode request failed: {e}")
        return f"Error: {str(e)}"

def get_movie_recommendations(genre):
    url = f"{BASE_URL}?s={genre}&type=movie&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            logger.info(f"Fetched {len(data['Search'])} recommendations for genre '{genre}'")
            return [
                {"title": movie["Title"], "year": movie["Year"], "imdb_id": movie["imdbID"]}
                for movie in data["Search"][:5]
            ]
        else:
            logger.warning(f"Recommendations failed: {data.get('Error')}")
            return f"Error: {data.get('Error', 'Unknown error')}"
    except requests.RequestException as e:
        logger.error(f"Recommendations request failed: {e}")
        return f"Error: {str(e)}"

def search_movies_by_year(year):
    url = f"{BASE_URL}?s=movie&type=movie&y={year}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            logger.info(f"Found {len(data['Search'])} movies for year '{year}'")
            return [
                {"title": movie["Title"], "year": movie["Year"], "imdb_id": movie["imdbID"]}
                for movie in data["Search"][:5]
            ]
        else:
            logger.warning(f"Year search failed: {data.get('Error')}")
            return f"Error: {data.get('Error', 'Unknown error')}"
    except requests.RequestException as e:
        logger.error(f"Year search request failed: {e}")
        return f"Error: {str(e)}"

def get_random_popular_movie():
    popular_titles = [
        "The Matrix",
        "Inception",
        "The Godfather",
        "Pulp Fiction",
        "Fight Club",
        "The Shawshank Redemption",
        "Forrest Gump",
        "The Dark Knight",
        "Titanic",
        "Avatar",
        "Interstellar",
        "Parasite"
    ]
    random_number = int(time.time() * 1000) % len(popular_titles)
    title = popular_titles[random_number]
    return get_movie_by_title(title, full_plot=True)

def get_movie_awards(title):
    url = f"{BASE_URL}?t={title}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True":
            return {
                "title": data.get("Title", "N/A"),
                "awards": data.get("Awards", "N/A")
            }
        else:
            return f"Error: {data.get('Error', 'Unknown error')}"
    except requests.RequestException as e:
        logger.error(f"Awards request failed: {e}")
        return f"Error: {str(e)}"

def get_season_details(series_title, season):
    url = f"{BASE_URL}?t={series_title}&Season={season}&apikey={API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "True" and "Episodes" in data:
            logger.info(f"Fetched season {season} details for '{series_title}'")
            return {
                "series_title": series_title,
                "season": data.get("Season", "N/A"),
                "total_episodes": data.get("totalSeasons", "N/A"),
                "episodes": [
                    {"episode": ep["Episode"], "title": ep["Title"], "imdb_rating": ep["imdbRating"]}
                    for ep in data["Episodes"][:5]  # Limit to 5 episodes
                ]
            }
        else:
            logger.warning(f"Season lookup failed: {data.get('Error')}")
            return f"Error: {data.get('Error', 'Unknown error')}"
    except requests.RequestException as e:
        logger.error(f"Season request failed: {e}")
        return f"Error: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    await update.message.reply_text(
        "Welcome to the Frame Flicker Bot! Use these commands:\n"
        "/search <title> - Search for movies\n"
        "/details <title> - Get movie details\n"
        "/id <imdb_id> - Get movie by IMDb ID\n"
        "/episode <series> <season> <episode> - Get series episode details\n"
        "/recommend <genre> - Get movie recommendations by genre\n"
        "/year <year> - Search movies by year\n"
        "/random - Get a random popular movie\n"
        "/awards <title> - Get movie awards\n"
        "/season <series> <season> - Get season details"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if not context.args:
        await update.message.reply_text("Please provide a movie title! Example: /search Matrix")
        return
    title = " ".join(context.args)
    results = search_movies(title)
    if isinstance(results, str):
        await update.message.reply_text(results)
    else:
        response = "Search Results:\n\n" + "\n\n".join(
           [f"- {movie['title']} ({movie['year']}) - {movie['imdb_id']}" for movie in results]
        )
        await update.message.reply_text(response, parse_mode='Markdown')

async def details(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if not context.args:
        await update.message.reply_text("Please provide a movie title! Example: /details The Matrix")
        return
    title = " ".join(context.args)
    movie = get_movie_by_title(title, full_plot=True)
    if isinstance(movie, str):
        await update.message.reply_text(movie)
    else:
        response = (
            f"**Title**: {movie['title']}\n"
            f"**Year**: {movie['year']}\n"
            f"**Released**: {movie['released']}\n"
            f"**Genre**: {movie['genre']}\n"
            f"**Director**: {movie['director']}\n"
            f"**Actors**: {movie['actors']}\n"
            f"**Plot**: {movie['plot']}\n"
            f"**IMDb Rating**: {movie['imdb_rating']}\n"
            f"**Runtime**: {movie['runtime']}"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

        filename = movie['title'] + '.txt'
        with open(filename, 'rb') as file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file,
                filename=filename,
                caption=f"Details for '{movie['title']}'"
            )

async def id(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if not context.args:
        await update.message.reply_text("Please provide an IMDb ID! Example: /id tt0133093")
        return
    imdb_id = context.args[0]
    movie = get_movie_by_imdb_id(imdb_id)
    if isinstance(movie, str):
        await update.message.reply_text(movie)
    else:
        response = (
            f"**Title**: {movie['title']}\n"
            f"**Year**: {movie['year']}\n"
            f"**Released**: {movie['released']}\n"
            f"**Genre**: {movie['genre']}\n"
            f"**Director**: {movie['director']}\n"
            f"**Actors**: {movie['actors']}\n"
            f"**Plot**: {movie['plot']}\n"
            f"**IMDb Rating**: {movie['imdb_rating']}\n"
            f"**Runtime**: {movie['runtime']}"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

async def episode(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if len(context.args) < 3:
        await update.message.reply_text("Please provide series, season, and episode! Example: /episode Breaking Bad 1 1")
        return
    series_title = " ".join(context.args[:-2])
    season, episode_num = context.args[-2], context.args[-1]
    episode_data = get_series_episode(series_title, season, episode_num)
    if isinstance(episode_data, str):
        await update.message.reply_text(episode_data)
    else:
        response = (
            f"**Series**: {episode_data['series_title']}\n"
            f"**Season**: {episode_data['season']}\n"
            f"**Episode**: {episode_data['episode']} - {episode_data['title']}\n"
            f"**Released**: {episode_data['released']}\n"
            f"**Plot**: {episode_data['plot']}\n"
            f"**IMDb Rating**: {episode_data['imdb_rating']}"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    if not context.args:
        await update.message.reply_text("Please provide a genre! Example: /recommend Sci-Fi")
        return
    genre = " ".join(context.args)
    results = get_movie_recommendations(genre)
    if isinstance(results, str):
        await update.message.reply_text(results)
    else:
        response = f"Recommendations for '{genre}':\n" + "\n".join(
            [f"- {movie['title']} ({movie['year']}) - {movie['imdb_id']}" for movie in results]
        )
        await update.message.reply_text(response)

async def year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a year! Example: /year 1999")
        return
    year = context.args[0]
    results = search_movies_by_year(year)
    if isinstance(results, str):
        await update.message.reply_text(results)
    else:
        response = f"Movies from {year}:\n" + "\n".join(
            [f"- {movie['title']} ({movie['year']}) - {movie['imdb_id']}" for movie in results]
        )
        await update.message.reply_text(response)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie = get_random_popular_movie()
    if isinstance(movie, str):
        await update.message.reply_text(movie)
    else:
        response = (
            f"**Random Popular Movie**\n"
            f"**Title**: {movie['title']}\n"
            f"**Year**: {movie['year']}\n"
            f"**Released**: {movie['released']}\n"
            f"**Genre**: {movie['genre']}\n"
            f"**Director**: {movie['director']}\n"
            f"**Actors**: {movie['actors']}\n"
            f"**Plot**: {movie['plot']}\n"
            f"**IMDb Rating**: {movie['imdb_rating']}\n"
            f"**Runtime**: {movie['runtime']}"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

async def awards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a movie title! Example: /awards The Godfather")
        return
    title = " ".join(context.args)
    awards_data = get_movie_awards(title)
    if isinstance(awards_data, str):
        await update.message.reply_text(awards_data)
    else:
        response = (
            f"**Awards for {awards_data['title']}**\n"
            f"**Awards**: {awards_data['awards']}"
        )
        await update.message.reply_text(response, parse_mode='Markdown')

async def season(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Please provide series and season! Example: /season Breaking Bad 1")
        return
    series_title = " ".join(context.args[:-1])
    season_num = context.args[-1]
    season_data = get_season_details(series_title, season_num)
    if isinstance(season_data, str):
        await update.message.reply_text(season_data)
    else:
        response = (
            f"**Series**: {season_data['series_title']}\n"
            f"**Season**: {season_data['season']}\n"
            f"**Total Seasons**: {season_data['total_episodes']}\n"
            f"**Episodes**:\n" + "\n".join(
                [f"- Ep {ep['episode']}: {ep['title']} (IMDb: {ep['imdb_rating']})" for ep in season_data['episodes']]
            )
        )
        await update.message.reply_text(response)


application = Application.builder().token("7384931567:AAGtuTeoMZz0V0ZIwnAlUQdsGOz323Vs3c8").build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("search", search))
application.add_handler(CommandHandler("details", details))
application.add_handler(CommandHandler("id", id))
application.add_handler(CommandHandler("episode", episode))
application.add_handler(CommandHandler("recommend", recommend))
application.add_handler(CommandHandler("year", year))
application.add_handler(CommandHandler("random", random))
application.add_handler(CommandHandler("awards", awards))
application.add_handler(CommandHandler("season", season))
logger.info("Bot started")
application.run_polling()
