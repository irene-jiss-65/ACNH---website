from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "ACNHPopularVillagers.db"

@app.route("/")
def render_home():
    return render_template("index.html")

@app.route("/villagers")
def render_webpage():
    query = "SELECT Name, Species, Personality, Birthday FROM popular_villagers"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query)
    villager_list = cur.fetchall()
    con.close()
    print(villager_list)
    return render_template("villagers.html", villager=villager_list)



def create_connection(db_file):
    """
    Create a connection to the database
    :parameter  db_file - the name of the file
    :returns    connection - a connection to the database"""

    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)