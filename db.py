#db.py
import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            print("i am here")
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn


def get_data():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM spiteam;')
        data = cursor.fetchall()
        if result > 0:
            got_songs = jsonify(data)
        else:
            got_songs = 'No Data in DB.'
    conn.close()
    print(data)
    return data

def add_data(data):
    conn = open_connection()
    with conn.cursor() as cursor:
        for index, row in data.iterrows():
            cursor.execute('INSERT INTO spiteam (rankteam, offe, def, spi, team, confed) VALUES(%s, %s, %s, %s, %s, %s)', (int(row["rank"]), float(row["off"]), float(row["def"]), float(row["spi"]), row["name"], row["confed"]))
    conn.commit()
    conn.close()