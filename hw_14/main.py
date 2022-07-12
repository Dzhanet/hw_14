import sqlite3
from flask import Flask, request
from utils import search_by_title, search_by_date, search_by_raiting, search_by_genre
import json

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/movie/<title>/') #возвращает фильмы по названию
def page_index(title):
    result = search_by_title(title=title)
    return result

@app.route('/movie/<year1>/to/<year2>/')  #возвращает фильмы за опред-й промежуток по годам
def search_years(year1,year2):
    result = search_by_date(year1=year1,year2=year2)
    return result

@app.route('/rating/<rating>/') #возвращает фильмы по рейтингу
def search_rating_view(rating):
    result = search_by_raiting(rating=rating)
    return result

@app.route('/genre/<genre>')
def search_genre_view(genre):
    result =search_by_genre(genre)
    return result

if __name__ == "__main__":
    app.run(debug=True)

