import sqlite3
import json
import numpy

connection = sqlite3.connect('sekurrity.db')

def get_cursor():
    return connection.cursor()

def get_face_record(face_id):
    c = get_cursor()
    c.execute("SELECT * from faces where id=?", str(face_id))
    return c.fetchone()

def is_valid_face_id(face_id):
    face = get_face_record(face_id)
    return face is not None

def create_tables():
    create_entrances_table()
    create_faces_table()

def create_entrances_table():
    c = get_cursor()
    c.execute("CREATE TABLE entrances (face_id integer, date text, time text, floor integer)")

def create_faces_table():
    c = get_cursor()
    c.execute("CREATE TABLE faces (id integer primary key, name text, classification integer, encoding text)")

def create_entrance(face_id):
    c = get_cursor()
    c.execute("INSERT INTO entrances VALUES (?, date('now'), datetime('now'), 5)", str(face_id))
    save()

def serialize_encoding(encoding):
    lencoding = regular_list = encoding.tolist()
    sencoding = json.dumps(regular_list)
    return sencoding

def deserialize_encoding(sencoding):
    lencoding = json.loads(sencoding)
    encoding = numpy.ndarray(shape=(128,), dtype='float64', buffer=numpy.array(lencoding))
    return encoding

def create_face(name, classification, encoding):
    c = get_cursor()
    c.execute("INSERT INTO faces (name, classification, encoding) VALUES (?,?,?)", (name, classification, serialize_encoding(encoding)))
    save()

def get_face_encoding(face_id):
    face = get_face_record(face_id)
    if face is None:
        return None
    return deserialize_encoding(face[3])

def has_entered_today(face_id):
    c = get_cursor()
    c.execute("SELECT face_id from entrances WHERE date = date('now') AND face_id = ?", str(face_id))
    entrance_count = len(c.fetchall())
    return entrance_count > 0

def last_entrance(face_id):
    c = get_cursor()
    c.execute("SELECT time from entrances WHERE face_id = ? ORDER BY time DESC LIMIT 1", str(face_id))
    if (len(c.fetchall()) == 0):
        return null;
    record = c.fetchone()
    return record[0]

def save():
    connection.commit()
