# -*- coding: utf-8 -*-
import sqlite3


def check_city(city: str):
    db = sqlite3.connect('db/cities.db')
    c = db.cursor()
    # c.execute("INSERT INTO list_of_cities VALUES ('moscow', 'http://doodoo.com')")
    info = c.execute(f"SELECT * FROM list_of_cities WHERE name = '{city}'")
    db.commit()
    if info.fetchone() is None:
        db.close()
        return 1
    else:
        db.close()
        return 0

def select_city_from_list(mode: str, city=None) -> str:
    db = sqlite3.connect('db/cities.db')
    c = db.cursor()
    if mode == 'get_url':
        c.execute(f"SELECT url FROM list_of_cities WHERE name = '{city}'")
        db.commit()
        url = c.fetchone()[0]
        db.close()
        return url
    elif mode == 'get_cities':
        cities = c.execute(f"SELECT name FROM list_of_cities")
        db.commit()
        for city in cities:
            print(city[0].capitalize())


def update_cities_in_list(name: str, url: str):
    db = sqlite3.connect('db/cities.db')
    c = db.cursor()
    c.execute(f"INSERT OR REPLACE INTO list_of_cities (name, url) VALUES('{name}', '{url}')")
    db.commit()
    db.close()
