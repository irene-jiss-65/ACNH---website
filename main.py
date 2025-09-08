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
    query = "SELECT Name, Species, VillagerImage FROM popular_villagers"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query)
    villager_list = cur.fetchall()
    con.close()
    print(villager_list)
   # title = name_type.upper()
    return render_template("villagers.html", villager=villager_list)

@app.route("/alldata")
def render_alldata():
    query = "SELECT Name, Species, Personality, Birthday, VillagerImage FROM popular_villagers"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query)
    villager_list = cur.fetchall()
    con.close()
    print(villager_list)
   # title = name_type.upper()
    return render_template("alldata.html", villager=villager_list)

@app.route("/species")
def render_species():
    query = "SELECT Name, Species, VillagerImage FROM popular_villagers"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query)
    villager_data = cur.fetchall()
    con.close()
    print(villager_data)
   # title = name_type.upper() 
    species_dict = {} # Create a dictionary of species
    
    for name, species, image in villager_data:
        if species not in species_dict:
            species_dict[species] = {'villagers': [], 'images': []} # Make a list of names for each species
        species_dict[species]['villagers'].append(name)
        species_dict[species]['images'].append(image) # append each name to specific species
    
    species_dict_zipped = {}
    for species, data in species_dict.items():
        species_dict_zipped[species] = list(zip(data['villagers'], data['images']))



    return render_template("species.html", species_dict = species_dict_zipped)

@app.route("/personality")
def render_personality():
    query = "SELECT Name, Personality, VillagerImage FROM popular_villagers"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query)
    villager_data = cur.fetchall()
    con.close()
    print(villager_data)
   # title = name_type.upper() 
    personality_dict = {} # Create a dictionary of Personalities
    
    for name, personality, image in villager_data:
        if personality not in personality_dict:
            personality_dict[personality] = {'villagers': [], 'images':[]} # Make a list of names for each personality
        personality_dict[personality]['villagers'].append(name)
        personality_dict[personality]['images'].append(image) # append each name to specific species
    
    personality_dict_zipped = {}
    for personality, data in personality_dict.items():
        personality_dict_zipped[personality] = list(zip(data['villagers'], data['images']))

    return render_template("personality.html", personality_dict = personality_dict_zipped)

@app.route('/search', methods=['GET', 'POST'])
def render_search():
    """
    Find all records which contain the search item
    :POST contains the search value
    :returns a rendered webpage"""

    search =request.form['search']
    title = "Search for " + search
    query = "SELECT Name, Personality, Species, Birthday, VillagerImage FROM popular_villagers WHERE " \
            "Name LIKE ? OR Personality LIKE ? OR Species LIKE ? OR Birthday LIKE ? OR VillagerImage Like ?"
    search = "%" + search + "%"
    con=create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search, search, search, search))
    villager_list = cur.fetchall()
    con.close()

    return render_template ("alldata.html", villager=villager_list, title=title)

def get_names(name_type):
    title = name_type.upper()
    query = "SELECT Name, Personality, Species, VillagerImage FROM popular_villagers WHERE Species=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    #Query the Database
    cur.execute(query, (title,))
    name_list = cur.fetchall()
    con.close()
    print(name_list)
    return name_list

#def get_species():
  #  con = create_connection(DATABASE)
   # query = "SELECT DISTINCT Species FROM popular_villagers ORDER BY Species ASC"

    #cur = con.cursor()
    #cur.execute(query)
    #records = cur.fetchall()
    #print(records)
    #for i in range(len(records)):
     #   records[i] = records[i][0]
    #print(records)
    #return records


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


#font-family: 'Ubuntu', 'Lucida Grande', 'Lucida Sans Unicode', 'Geneva', 'Verdana', sans-serif;
