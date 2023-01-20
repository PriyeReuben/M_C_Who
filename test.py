import random
import sqlite3

conn = sqlite3.connect('MC_Who.db')
cur = conn.cursor()



movie_dict = {'Iron Man':371746,
              'The Incredible Hulk':800080,
              'Iron Man 2':1228705,
              'Thor':800369,
              'Captain America: The First Avenger':458339,
              'The Avengers':848228,
              'Iron Man 3':1300854,
              'Thor: The Dark World':1981115}

movie_list = list(movie_dict)

roll = random.randint(0, len(movie_list) - 1)  # random number betweeen 1 and 6
selected_movie = movie_list[roll]
# print(selected_movie)



movie_id = movie_dict[selected_movie]
# print("Movie ID:", movie_id)

cur.execute("""
    SELECT
        actor_id, name
    FROM Cast_Members
    WHERE
        movie_id = (?)
""", (movie_id,))

movie_actors = []  # list of all actors in selected movie

items = cur.fetchall()
for row in items:
    movie_actors.append(row[0])

# print("Movie actors:", sorted(movie_actors))

selected_actors = []  # 10 random actors from the selected movie
while len(selected_actors) < 20:
    roll = random.randint(0, len(movie_actors) - 1)
    if movie_actors[roll] in selected_actors:
        continue
    else:
        selected_actors.append(movie_actors[roll])
# print("Random Actors:", sorted(selected_actors))

possible_movies = []  # all movies from movie_list/movie_dict containing selected actors
for actor_id in selected_actors:  # pick a selected actor
    # print(actor_id)
    # get movies actor was in
    cur.execute("""
        SELECT DISTINCT
            movie_id
        FROM Cast_Members
        WHERE
            actor_id = (?)
    """, (actor_id,))
    items = cur.fetchall()
    for row in items:
        if row[0] in possible_movies:
            continue
        elif int(row[0]) not in list(movie_dict.values()):
            # print(row[0], "not in", list(movie_dict.values()))
            continue
        else:
            possible_movies.append(row[0])
print(possible_movies)

