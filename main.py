"""
This python file displays data about Animal Crossing New Horizons.

Uses Flask to connect to a database
Connects to a popular villager database, displaying the data in various forms
Users view displayed data, navigate pages, search data
and sort the data displayed
"""

from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error


app = Flask(__name__)
DATABASE = "ACNHPopularVillagers.db"


# App route that displays the home page
@app.route("/")
def render_home():
    """Render the home page HTML."""
    return render_template("index.html")


# App route that renders webpage with all the villagers
@app.route("/villagers")
def render_webpage():
    """
    Make a webpage that contains villagers with their name, species and image.

    Fetch the name, species and villagers image from database
    Render an HTML template with the recieved data
    """
    # Query that takes name species and image from database
    query = "SELECT Name, Species, VillagerImage FROM popular_villagers"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query)
    villager_list = cur.fetchall()
    con.close()
    print(villager_list)
    return render_template("villagers.html", villager=villager_list)


# App route that renders webpage with a table of full database
@app.route("/alldata")
def render_alldata():
    """
    Receive all the data in the database.

    Execute a query that fetches all the records
    Return a rendered HTML with all of the data
    """
    # Query that takes all records from database
    query = "SELECT Name, Species, Personality, Birthday, \
          VillagerImage FROM popular_villagers"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query)
    villager_list = cur.fetchall()
    con.close()
    print(villager_list)
    return render_template("alldata.html", villager=villager_list)


# App route that renders webpage that displays each unique species
@app.route("/species")
def render_species():
    """
    Receive the villagers from the database and sort them by species.

    Creates a zip dictionary that links each name and image to the species
    Return a dictionary of species with corresponding name and image
    """
    # Query that takes the name, species and image from database
    query = "SELECT Name, Species, VillagerImage FROM popular_villagers"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query)
    villager_data = cur.fetchall()
    con.close()
    print(villager_data)
    species_dict = {}  # Create a dictionary of species

    for name, species, image in villager_data:
        if species not in species_dict:
            # Make a list of names for each species (empty)
            species_dict[species] = {'villagers': [], 'images': []}

        # Append name and image to corresponding species
        species_dict[species]['villagers'].append(name)
        species_dict[species]['images'].append(image)

    # Zip the dictionary in order to have the correct correspondence
    species_dict_zipped = {}
    for species, data in species_dict.items():
        species_dict_zipped[species] = \
            list(zip(data['villagers'], data['images']))

    return render_template("species.html", species_dict=species_dict_zipped)


# App route that renders a webpage displaying unique personality
@app.route("/personality")
def render_personality():
    """
    Receive the Personality of each villager.

    Make a dictionary that matches each name and image to the personality
    Zip the dictionary
    """
    # Query that takes the name, personality and image from database
    query = "SELECT Name, Personality, VillagerImage FROM popular_villagers"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query)
    villager_data = cur.fetchall()
    con.close()
    print(villager_data)
    personality_dict = {}  # Create a dictionary of personalities

    for name, personality, image in villager_data:
        if personality not in personality_dict:
            # Make a list of names for each personality
            personality_dict[personality] = {'villagers': [], 'images': []}
        # Append each name and image to specific species
        personality_dict[personality]['villagers'].append(name)
        personality_dict[personality]['images'].append(image)

    # Zip dictionary that corresponds the name and image to the personality
    personality_dict_zipped = {}
    for personality, data in personality_dict.items():
        personality_dict_zipped[personality] = \
            list(zip(data['villagers'], data['images']))

    return render_template("personality.html", personality_dict=personality_dict_zipped)


# App route that allows users to search for data
@app.route('/search', methods=['GET', 'POST'])
def render_search():
    """
    Find all records which contain the search item.

    :POST contains the search value
    :returns a rendered webpage
    """
    search = request.form['search']
    title = "Search for " + search

    # Query that takes all records from database
    query = "SELECT Name, Personality, Species, Birthday, VillagerImage \
            FROM popular_villagers WHERE  \
            Name LIKE ? OR Personality LIKE ? OR Species LIKE ? \
            OR Birthday LIKE ? OR VillagerImage Like ?"
    search = "%" + search + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search, search, search, search))
    villager_list = cur.fetchall()
    con.close()

    # User searches something invalid
    no_results = len(villager_list) == 0

    return render_template("alldata.html", villager=villager_list, title=title, no_results=no_results)


# App route that sorts the records in the All Data page - alphabetically
@app.route('/sort')
def render_sortpage():
    """
    Sort out the columns by alphabetical order.

    Allow the user to change the order of the columns (ascending or descending)
    """
    sort = request.args.get('sort')
    order = request.args.get('order', 'asc')

    # Checks to see the current order
    if order == 'asc':
        new_order = 'desc'
    else:
        new_order = 'asc'
    
    # Query that takes all records and orders them
    query = "SELECT Name, Species, Personality, Birthday, VillagerImage \
        FROM popular_villagers ORDER BY " + sort + " " + order

    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute(query)
    villager_list = cur.fetchall()
    con.close()

    return render_template('alldata.html', villager=villager_list, order=new_order, sort=sort)


# Function that gets all the records from database
def get_names(name_type):
    """
    Get a list of villagers.

    Match them to the correct species
    Change all their names to UPPER
    """
    title = name_type.upper()
    query = "SELECT Name, Personality, Species, VillagerImage \
        FROM popular_villagers WHERE Species=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # Query the Database
    cur.execute(query, (title,))
    name_list = cur.fetchall()
    con.close()
    print(name_list)
    return name_list


# Function that takes each unique species from database
def get_species():
    """
    Fetch all of the distinct(unique) species from the database.

    Sort the list alphabeitcally
    Returns the list
    """
    con = create_connection(DATABASE)
    query = "SELECT DISTINCT Species FROM popular_villagers \
        ORDER BY Species ASC"

    cur = con.cursor()
    cur.execute(query)
    records = cur.fetchall()
    print(records)
    for i in range(len(records)):
        records[i] = records[i][0]
    print(records)
    return records


# Function that connects to the database
def create_connection(db_file):
    """
    Create a connection to the database.

    :parameter  db_file - the name of the file
    :returns    connection - a connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
