import sqlite3

connection = sqlite3.connect('sekurrity.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE entrances (face_id integer, date text, time text, floor integer)")
cursor.execute("CREATE TABLE faces (id integer primary key, name text, classification integer, encoding text)")
connection.commit()
