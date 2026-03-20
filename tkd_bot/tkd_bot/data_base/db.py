import sqlite3

conn = sqlite3.connect('coaches.db', check_same_thread=False)
cursor = conn.cursor()

conn2 = sqlite3.connect('reservation.db', check_same_thread=False)
cursor2 = conn2.cursor()
