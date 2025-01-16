import imdb 

k = imdb.IMDb()

movies = k.search_movie('Game Changer')
finalListOfMovies = movies[:5]

if not finalListOfMovies:
    print("Sorry, no movie found with that name.")
    exit()
    
for i,j in enumerate(finalListOfMovies):
    
    movieId=j.getID()
    movie = k.get_movie(movieId)
    print("Movie No : ",i+1)
    print("Title : ",j)
    print("Genres: "+",".join(movie['genres']))
    print("Year : ",movie['year'])
    print("Rating : ",movie['rating'])
    print("Plot : ",movie['plot'][0])
    print("Cast : ",movie['cast'][0])
    print("Director : ",movie.get('directors'))
    print("\n\n")