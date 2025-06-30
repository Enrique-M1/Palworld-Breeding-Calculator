import mariadb  # Importing the database that holds the information.
from _shared.DBSettings import Settings


# Global Vars for the database connection (Change these depending on your machine.)
# If you did not have a previous database installed already, leave them as is.
DB_USER = Settings.getDBUsername()
DB_PASS = Settings.getDBPassword()

mariadb_con = mariadb.connect( #put your user and password for your database below here.
    user = DB_USER,
    password = DB_PASS,
    host="127.0.0.1",
    port=3306,
    database="Palworld-Breeding-Info", #In your database. you WILL need to add this.
)
cur = mariadb_con.cursor()

# Create the database
def create_database(db_name: str):
    mariadb_connect = mariadb.connect( #put your user and password for your database below here.
        user = DB_USER,
        password = DB_PASS,
        host="127.0.0.1",
        port=3306
    )

    cursor = mariadb_connect.cursor()
    query = f"CREATE DATABASE '{db_name}';"
    cursor.execute(query)
    print(cursor.statement)

    cursor.close()
    mariadb_connect.close()

# Printing the table that is given as argument
def print_from_table(table_name: str):
    query: str = f'SELECT * FROM {table_name};'

    cur.execute(query)
    results = cur.fetchall()

    for result in results:
        print(result)

#Creating the Breeding Table
def create_relationship_table():
    stmt = "CREATE TABLE Relationships"

if __name__ == '__main__':
    db = "Palworld-Info"