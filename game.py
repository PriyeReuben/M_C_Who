from workhorse import Workhorse

game = Workhorse()
movies_dictionary = game.create_movie_dict() #create a dictionary of lists
selected_movie = game.select_movie() #randomly select a movie from the dictionary
game.load_actors(selected_movie) #select 10 most prolific actors from the movie
incorrect_movies = game.populate_other_movies() #make a dictionary that contains the other movies and their prolific actor count
movie_bins_list = game.fill_bins(incorrect_movies)
game.populate_options(selected_movie, movie_bins_list)
print(game.options)
print(game.selected_characters)
