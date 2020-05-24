import sqlite3

print('EXECUTING DB INSERTS')
connection = sqlite3.connect('db.sqlite3')
with open("./sql/inserts.sql", "r") as file:
    connection.executescript(file.read())
connection.close()
print('-------FINISH-------')
