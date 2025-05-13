import mariadb  # Importing the database that holds the information.

mariadb_con = mariadb.connect(
    user="root",
    password="",
    host="127.0.0.1",
    port=3306,
    database="Palworld-Breeding-Info",
)
cur = mariadb_con.cursor()

# Create the database
def create_database(db_name: str):
    mariadb_connect = mariadb.connect(
        user="root",
        password="soccerm@n1",
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
    db = "Palworld-Info"  #