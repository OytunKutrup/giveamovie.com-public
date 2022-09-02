import config
from flask import Flask, render_template, request, flash
from youtubesearchpython import VideosSearch
from Backend import *
app = Flask(__name__)
app.secret_key = "key"


def get_recommendation_data(movie_name):
    uri = config.NEO4J_URI
    user = "neo4j"
    password = config.NEO4J_API_KEY
    neo4j_app = App(uri, user, password)
    recommended_movies = neo4j_app.get_recommendation(movie_name)
    neo4j_app.close()
    return recommended_movies


def get_movie_names():
    uri = config.NEO4J_URI
    user = "neo4j"
    password = config.NEO4J_API_KEY
    neo4j_app = App(uri, user, password)
    movie_names = neo4j_app.get_names()
    neo4j_app.close()
    return movie_names

def get_trailer(movie_name, year):
    video_search = VideosSearch(movie_name + str(year) + "trailer", limit=1)
    return "https://www.youtube.com/embed/" + video_search.result()['result'][0]['id']


movie_names = get_movie_names()


@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html", movie_names=movie_names)


@app.route("/recommendation1", methods=["POST", "GET"])
def recommendation1():
    if request.method == 'POST':
        input_movie = request.form['movie_input']
        recommended_movies = get_recommendation_data(input_movie)

        if recommended_movies is None:
            rec_movie_name = "Movie not found!"
            return render_template("home.html", name=rec_movie_name, movie_names=movie_names)
        recommended_movie = recommended_movies[0]

        rec_movie_name = recommended_movie.get('title')
        rec_movie_overview = recommended_movie.get('overview')
        rec_movie_runtime = recommended_movie.get('runtime')
        rec_movie_year = recommended_movie.get('year')
        rec_movie_rating = recommended_movie.get('average_rating')
        rec_movie_genres = recommended_movie.get('genres')
        rec_movie_imdb_id = recommended_movie.get('imdb_id')
        imdb_link = "https://www.imdb.com/title/" + rec_movie_imdb_id
        movie_trailer = get_trailer(rec_movie_name, rec_movie_year)
        action = "recommendation2"
        flash("(" + str(recommended_movie.get('year')) + ")")
        flash("min")
        flash("IMDB")


        return render_template("recommendation.html", input_movie=input_movie, name=rec_movie_name,
                               overview=rec_movie_overview, runtime=rec_movie_runtime, year=rec_movie_year,
                               rating=rec_movie_rating, genres=rec_movie_genres, imdb_link=imdb_link, action=action,
                               trailer=movie_trailer, movie_names=movie_names)


@app.route("/recommendation2", methods=["POST", "GET"])
def recommendation2():
    if request.method == 'POST':
        input_movie = request.form['movie_input']
        recommended_movies = get_recommendation_data(input_movie)

        if len(recommended_movies) < 2:
            rec_movie_name = "There is no other recommendations for this movie!"
            return render_template("home.html", name=rec_movie_name, movie_names=movie_names)
        recommended_movie = recommended_movies[1]

        rec_movie_name = recommended_movie.get('title')
        rec_movie_overview = recommended_movie.get('overview')
        rec_movie_runtime = recommended_movie.get('runtime')
        rec_movie_year = recommended_movie.get('year')
        rec_movie_rating = recommended_movie.get('average_rating')
        rec_movie_genres = recommended_movie.get('genres')
        rec_movie_imdb_id = recommended_movie.get('imdb_id')
        imdb_link = "https://www.imdb.com/title/" + rec_movie_imdb_id
        movie_trailer = get_trailer(rec_movie_name, rec_movie_year)
        action = "recommendation3"
        flash("(" + str(recommended_movie.get('year')) + ")")
        flash("min")
        flash("IMDB")

        return render_template("recommendation.html", input_movie=input_movie, name=rec_movie_name,
                               overview=rec_movie_overview, runtime=rec_movie_runtime, year=rec_movie_year,
                               rating=rec_movie_rating, genres=rec_movie_genres, imdb_link=imdb_link, action=action,
                               trailer=movie_trailer, movie_names=movie_names)


@app.route("/recommendation3", methods=["POST", "GET"])
def recommendation3():
    if request.method == 'POST':
        input_movie = request.form['movie_input']
        recommended_movies = get_recommendation_data(input_movie)

        if len(recommended_movies) < 3:
            rec_movie_name = "There is no other recommendations for this movie!"
            return render_template("home.html", name=rec_movie_name, movie_names=movie_names)
        recommended_movie = recommended_movies[2]

        rec_movie_name = recommended_movie.get('title')
        rec_movie_overview = recommended_movie.get('overview')
        rec_movie_runtime = recommended_movie.get('runtime')
        rec_movie_year = recommended_movie.get('year')
        rec_movie_rating = recommended_movie.get('average_rating')
        rec_movie_genres = recommended_movie.get('genres')
        rec_movie_imdb_id = recommended_movie.get('imdb_id')
        imdb_link = "https://www.imdb.com/title/" + rec_movie_imdb_id
        movie_trailer = get_trailer(rec_movie_name, rec_movie_year)
        action = "recommendation4"
        flash("(" + str(recommended_movie.get('year')) + ")")
        flash("min")
        flash("IMDB")
        return render_template("recommendation.html", input_movie=input_movie, name=rec_movie_name,
                               overview=rec_movie_overview, runtime=rec_movie_runtime, year=rec_movie_year,
                               rating=rec_movie_rating, genres=rec_movie_genres, imdb_link=imdb_link, action=action,
                               trailer=movie_trailer, movie_names=movie_names)


@app.route("/recommendation4", methods=["POST", "GET"])
def recommendation4():
    if request.method == 'POST':
        input_movie = request.form['movie_input']
        recommended_movies = get_recommendation_data(input_movie)

        if len(recommended_movies) < 4:
            rec_movie_name = "There is no other recommendations for this movie!"
            return render_template("home.html", name=rec_movie_name, movie_names=movie_names)
        recommended_movie = recommended_movies[3]

        rec_movie_name = recommended_movie.get('title')
        rec_movie_overview = recommended_movie.get('overview')
        rec_movie_runtime = recommended_movie.get('runtime')
        rec_movie_year = recommended_movie.get('year')
        rec_movie_rating = recommended_movie.get('average_rating')
        rec_movie_genres = recommended_movie.get('genres')
        rec_movie_imdb_id = recommended_movie.get('imdb_id')
        imdb_link = "https://www.imdb.com/title/" + rec_movie_imdb_id
        movie_trailer = get_trailer(rec_movie_name, rec_movie_year)
        action = "recommendation5"
        flash("(" + str(recommended_movie.get('year')) + ")")
        flash("min")
        flash("IMDB")
        return render_template("recommendation.html", input_movie=input_movie, name=rec_movie_name,
                               overview=rec_movie_overview, runtime=rec_movie_runtime, year=rec_movie_year,
                               rating=rec_movie_rating, genres=rec_movie_genres, imdb_link=imdb_link, action=action,
                               trailer=movie_trailer, movie_names=movie_names)


@app.route("/recommendation5", methods=["POST", "GET"])
def recommendation5():
    if request.method == 'POST':
        input_movie = request.form['movie_input']
        recommended_movies = get_recommendation_data(input_movie)

        if len(recommended_movies) < 5:
            rec_movie_name = "There is no other recommendations for this movie!"
            return render_template("home.html", name=rec_movie_name, movie_names=movie_names)
        recommended_movie = recommended_movies[4]

        rec_movie_name = recommended_movie.get('title')
        rec_movie_overview = recommended_movie.get('overview')
        rec_movie_runtime = recommended_movie.get('runtime')
        rec_movie_year = recommended_movie.get('year')
        rec_movie_rating = recommended_movie.get('average_rating')
        rec_movie_genres = recommended_movie.get('genres')
        rec_movie_imdb_id = recommended_movie.get('imdb_id')
        imdb_link = "https://www.imdb.com/title/" + rec_movie_imdb_id
        movie_trailer = get_trailer(rec_movie_name, rec_movie_year)
        action = "recommendation1"
        flash("(" + str(recommended_movie.get('year')) + ")")
        flash("min")
        flash("IMDB")
        return render_template("recommendation.html", input_movie=input_movie, name=rec_movie_name,
                               overview=rec_movie_overview, runtime=rec_movie_runtime, year=rec_movie_year,
                               rating=rec_movie_rating, genres=rec_movie_genres, imdb_link=imdb_link, action=action,
                               trailer=movie_trailer, movie_names=movie_names)


if __name__ == "__main__":
    app.run(debug=True)
