import random
import sqlite3
import time

# movies = {} #create_movie_dict()
# roll = 0
# selected_characters = {} #load_actors()
# cast_list = []
# other_movies = {} #other_movies()
# options = []

class Workhorse:

    def __init__(self):
        self.movies = {}  # create_movie_dict()
        self.roll = 0
        self.selected_characters = {}  # load_actors()
        self.cast_list = []
        self.other_movies = {}  # other_movies()
        self.options = []
        self.random_movie_list = []
        self.conn = sqlite3.connect('MCW.db')
        self.cur = self.conn.cursor()

    def create_movie_dict(self):

        conn = sqlite3.connect('MCW.db')
        cur = conn.cursor()
        cur.execute("""
                SELECT
                *
            FROM
                Movies
            WHERE id != 9032400
            """)

        items = cur.fetchall()
        for row in items:
            self.movies[row[0]] = row[1]


        #print("All movies:",movies)
        #return self.movies

    def select_movie(self):
        roll = random.choice(list(self.movies.values()))
        #roll = random.choice(movies)
        #print("Random movie ID:",roll)
        return(roll)

    def load_actors(self, movie_id):
        #conn = sqlite3.connect('MCW.db')
        #cur = conn.cursor()
        self.cur.execute("""
            SELECT
                Credits.actor_id, COUNT(*) AS appearance_count
            FROM
                Credits
            WHERE
                Credits.actor_id IN
                (SELECT
                    Actors.id
                FROM
                    Credits
                    JOIN
                    Actors
                ON
                    Credits.actor_id = Actors.id
                WHERE
                    movie_id = (?)) AND  movie_id != 9032400
            GROUP BY
                Credits.actor_id
            ORDER BY
                COUNT(*) DESC
            LIMIT
                10
        """, (movie_id,))

        items = self.cur.fetchall()
        for row in items:
            self.selected_characters[row[0]] = row[1]


        #print("Top 10 prolific actors:", selected_characters)

    def close_db(self):
        self.conn.close()

    def rename(self):
        conn = sqlite3.connect('MCW.db')
        cur = conn.cursor()
        cur.execute("""
                    ALTER TABLE Actors RENAME COLUMN actor_id TO id;
                """)

    def populate_other_movies(self):
        cast_list = list(self.selected_characters.keys())
        #print("Cast of selected movie:", cast_list)
        #conn = sqlite3.connect('MCW.db')
        #cur = conn.cursor()

        for actor in cast_list:
            self.cur.execute("""
                SELECT
                    movie_id
                FROM
                    Credits
                WHERE
                    Credits.actor_id = (?)       
            """, (actor,))

            items = self.cur.fetchall()
            for movie in items:
                self.other_movies[movie[0]] = self.other_movies.get(movie[0], 0) + 1
        #print("Movies with some prolific actors:", other_movies)

        return self.other_movies

    def fill_bins(self, movie_dict):
        bin_max_25 = []
        bin_max_50 = []
        bin_max_75 = []
        bin_max_100 = []

        #correct_movie = movie_dict.get(self.get_movie_name(movie_id))

        for key,value in movie_dict.items():
            if value == 1 or value == 2:
                bin_max_25.append(key)
            elif value == 3 or value == 4 or value == 5:
                bin_max_50.append(key)
            elif value == 6 or value == 7:
                bin_max_75.append(key)
            elif value == 8 or value == 9:
                bin_max_100.append(key)

        #print("bins", bin_max_25, bin_max_50, bin_max_75, bin_max_100)
        full_bin_list = [bin_max_100, bin_max_75, bin_max_50, bin_max_25]
        return full_bin_list

    def get_movie_name(self, movie_id):
        #conn = sqlite3.connect('MCW.db')
        #cur = conn.cursor()
        self.cur.execute("""
                    SELECT
                        Movies.title
                    FROM
                        Movies
                    WHERE
                        Movies.id = (?) AND  Movies.id != 9032400
                       
                """,(movie_id,))

        items = self.cur.fetchall()
        for row in items:
            return row[0]

    def get_actor_name(self, actor_id):
        self.cur.execute("""
                            SELECT
                                Actors.name
                            FROM
                                Actors
                            WHERE
                                Actors.id = (?)

                        """, (actor_id,))

        items = self.cur.fetchall()
        for row in items:
            return row[0]

    def populate_options(self, movie_id, movie_list):

        correct_movie = movie_id
        self.options.append(correct_movie)


        while len(self.options) < 6: #while the size of the options is less than 6...
            for bin in movie_list: #this goes through the movie_list, which is a list of lists.
                if len(bin) > 0:    #and assuming the current bin is not empty...
                    self.options.append(bin[0]) #then append the first value of the current bin to the options list
                    del(bin[0]) #and remove that value from the bin
                else:
                    pass
        self.options = self.options[0:6]

    def randomize_movie_options(self):
        random.shuffle(self.options)
        self.random_movie_list = self.options
        #print("random movies", self.random_movie_list)

        #random.shuffle(self.selected_characters)
        #print("non-random char list", self.selected_characters)

    # def setup(self):
    #     self.create_movie_dict()
    #     selected_movie = self.select_movie()
    #     self.load_actors(selected_movie)
    #     incorrect_movies = self.populate_other_movies()
    #     movie_bins_list = self.fill_bins(incorrect_movies)
    #
    #     self.populate_options(selected_movie, movie_bins_list)
    #
    #     correct_movie = self.options[0]
    #     self.randomize_movie_options()  # this 'returns' a randomized list (self.random_movie_list)
    #
    #     guess_matrix = []
    #     guess_item = []
    #     for i, movie in enumerate(self.random_movie_list, start=1):
    #         guess_item.append(i)  # the pick number
    #         guess_item.append(movie)  # them movie_id
    #         guess_item.append(self.get_movie_name(movie))  # the title
    #         guess_matrix.append(guess_item)  # add the whole list tot he guess matrix
    #         guess_item = []  # clear out the item list
    #     # print(guess_matrix)
    #
    #     random_actor_list = []
    #     for key, value in self.selected_characters.items():
    #         random_actor_list.append(key)
    #     random.shuffle(random_actor_list)

    def text_game(self):
        self.create_movie_dict()
        selected_movie = self.select_movie()
        self.load_actors(selected_movie)
        incorrect_movies = self.populate_other_movies()
        movie_bins_list = self.fill_bins(incorrect_movies)
        self.populate_options(selected_movie, movie_bins_list)
        #self.print_movies(self.options)
        correct_movie = self.options[0]
        self.randomize_movie_options() #this 'returns' a randomized list (self.random_movie_list)


        guess_matrix = []
        guess_item = []
        for i, movie in enumerate(self.random_movie_list, start = 1):
            guess_item.append(i)   #the pick number
            guess_item.append(movie) # the movie_id
            guess_item.append(self.get_movie_name(movie)) #the title
            guess_matrix.append(guess_item) #add the whole list to the guess matrix
            guess_item = [] #clear out the item list
        #print(guess_matrix)

        random_actor_list = []
        for key,value in self.selected_characters.items():
            random_actor_list.append(key)
        random.shuffle(random_actor_list)



        for actor_id in random_actor_list:
            print(self.get_actor_name(actor_id))  # print actor name
            #random.shuffle(guess_matrix) #not really necessary
            for i, guess in enumerate(guess_matrix):
                print(i+1, ":", guess[2])
            player_guess = input("Pick the correct movie: ")
            if guess_matrix[int(player_guess)-1][1] == correct_movie:
                print("Correct!")
                break
            else:
                print("Wrong!!")
                #guess_matrix[int(player_guess)-1][2]= "Wrong"
        else:
            print("You guessed incorrectly too many times and nobody loves you.")

        #set everything back to blank
        guess_matrix = [] # clear the guess matrix?
        self.selected_characters = {}
        self.movies = {}  # create_movie_dict()
        self.roll = 0
        self.selected_characters = {}  # load_actors()
        self.cast_list = []
        self.other_movies = {}  # other_movies()
        self.options = []
        self.random_movie_list = []

    def print_characters(self, dict):
        for i in dict:
            print("test",self.get_actor_name(i))

    def print_movies(self, iter):
        for i in iter:
            print("test",self.get_movie_name(i))



print("----Select the movie that has the given actors.----")
print("----A new actor will be revealed with every wrong guess.----")
game = Workhorse()
while True:
    game.text_game()
    if input("Do you want to play again? Y/N ").upper() != 'Y':
        break




