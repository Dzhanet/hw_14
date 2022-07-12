import json
import sqlite3

from flask import jsonify


def get_value_from_db(sql):
    """Функция, которая возвращает все данные из базы данных"""

    with sqlite3.connect("netflix.db") as connection:
        result = connection.execute(sql).fetchall()

        return result


def search_by_title(title):
    """Функция, которая возвращает самый свежий фильм по названию фильма из БД"""

    sql = f'''
          SELECT *
          FROM netflix
          WHERE title = '{title}'
          ORDER BY release_year DESC
          LIMIT 1
    '''

    result = get_value_from_db(sql)
    for item in result:
        new_result = json.dumps(item[:-1])

    return new_result


def search_by_date(year1, year2):
    """Функция, которая возвращает названия фильмов в диапазоне между year1 и year2"""

    sql = f'''
           SELECT title,release_year
           FROM netflix
           WHERE release_year BETWEEN '{year1}' AND '{year2}'
           LIMIT 100
     '''

    result = get_value_from_db(sql)
    dict_movies = []
    for item in result:
        dict_movies.append(item)

    new_result = json.dumps(dict_movies[:-1])

    return new_result


def search_by_raiting(rating):
    """Функция, которая возвращает фильм по рейтингу"""

    my_dict = {"children": ("G", "G"), "family": ("G", "PG", "PG-13"), "adult": ("R", "NC-17")}

    sql = f'''
           SELECT title,rating,description
           FROM netflix
           WHERE rating in {my_dict.get(rating, "R")}'''

    dict_movies = []
    for item in get_value_from_db(sql=sql):
        dict_movies.append(item)

    new_result = json.dumps(dict_movies[:-1])
    return new_result

def search_by_genre(genre):
    """Функция возвращает фильм по жанру"""

    sql = f'''
          SELECT title,description
          FROM netflix
          WHERE listed_in LIKE '%{genre}'
          ORDER BY release_year DESC
          LIMIT 10
    '''
    dict_movies = []
    for item in get_value_from_db(sql=sql):
        dict_movies.append(item)

    new_result = json.dumps(dict_movies[:-1])
    return new_result

def search_double_name(name1,name2):
    """Функция возвращает актеров, которые играли больше двух раз с введенными актерами"""

    sql = f'''
          SELECT "cast"
          FROM netflix
          WHERE "cast" LIKE '%{name1}%' AND "cast" LIKE '%{name2}%'
          ORDER BY release_year DESC
          LIMIT 10
    '''

    result = get_value_from_db(sql=sql)
    name_dict = {}
    for item in result:
        names = set(dict(item).get("cast").split(",")) - set([name1, name2])

        for name in names:
            name_dict[str(name).strip()] = name_dict.get(str(name).strip(), 0) + 1

    for key,value in name_dict.items():
        if value >= 2:
            print(key)

search_double_name('Rose McIver','Ben Lamb')
