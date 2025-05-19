import mariadb  # the database (must be downloaded aswell) (Azure data studio is not a command prompt download)
import asyncio  # must be downloaded to be used. (command prompt "pip install asyncio")
from hypercorn.config import Config  # Both this and the one below it must be downloaded
from hypercorn.asyncio import serve  # (command prompt "pip install hypercorn")
from fastapi import FastAPI  # Must be downloaded (command prompt "pip install fastapi")
from starlette.responses import RedirectResponse
from pals import Pal

# https://fastapi.tiangolo.com/
app = FastAPI(title="Palworld API")  # The server name

# Global Vars for the database connection (Change these depending on your machine.)
# If you did not have a previous database installed already, leave them as is.
userName = "root"
password = ""

# The information used to connect this API to the mariadb database
mariadb_con = mariadb.connect(
    user = userName,
    password = password,
    host="127.0.0.1",
    port=3306,
    database="Palworld_Info",
)
cur = mariadb_con.cursor()  # Cursor that points to the information above


@app.get('/', include_in_schema=False)
def get_default_page():
    return RedirectResponse(url='/docs')


# Uses SQL to print the pals table from the Azure Data Studio
# (SQL because that is the language the database is built in)
def get_pals_from_db(table_name: str):
    query: str = f'SELECT * FROM {table_name};'

    cur.execute(query)
    results = cur.fetchall()

    return results


# Uses SQL to print the saved combos table from the Azure Data Studio
# (SQL because that is the language the database is built in)
def get_saved_combos_from_db(table_name: str):
    query: str = f'SELECT * FROM {table_name};'

    cur.execute(query)
    results = cur.fetchall()

    return results


# Find the Child of the given parents
def get_child_from_db(pals: Pal):
    # Declare Variables and queries
    p1_failure: str = "Parent 1 does not exist, or is misspelled.\n"
    p2_failure: str = "Parent 2 does not exist, or is misspelled.\n"
    child_failure: str = "There is no record of those two pals breeding together.\nPlease input a different one.\n"
    parent1_query: str = f" SELECT Id FROM `pals` WHERE Pal_Name = '{pals.parent1}'"
    parent2_query: str =  f" SELECT Id FROM `pals` WHERE Pal_Name = '{pals.parent2}'"

    cur.execute(parent1_query)
    parent1_id = cur.fetchone()[0]

    if not parent1_id == 'NoneType':
        cur.execute(parent2_query)
        parent2_id = cur.fetchone()[0]

        if not parent2_id == 'NoneType':
            child_query: str = f" SELECT Child_Id FROM `relationships` WHERE Parent1_Id = '{parent1_id}' AND Parent2_Id = '{parent2_id}'"

            cur.execute(child_query)
            child_id: int = cur.fetchone()[0]

            if not child_id == 'NoneType':
                name_query: str = f"SELECT Pal_Name FROM `pals` WHERE Id = '{child_id}'"
                cur.execute(name_query)
                child_name = cur.fetchone()[0]
                pals.child = child_name

                save_to_db(pals)
                return child_name

            else:
                return child_failure

        else:
            return p2_failure
    else:
        return p1_failure


# Function to auto save the pals to the table
def save_to_db(pals: Pal):
    insert_stmt: str = f""" 
            INSERT INTO `saved_combos` (Parent1, Parent2, Child) VALUES ('{pals.parent1}', '{pals.parent2}', '{pals.child}')
            """
    cur.execute(insert_stmt)
    mariadb_con.commit()


# Calling the function to print the pals from the database (API endpoint)
@app.get('/api/pals')
def get_pals_list():
    return get_pals_from_db('pals')


# Calling the function to print the saved combinations from the database (API endpoint)
@app.get('/api/saved_combos')
def get_saved_combos():
    return get_saved_combos_from_db('saved_combos')


# Calling the function to print the combination when given parent 1 and 2
@app.post('/api/get_child')
def find_child(pals: Pal):
    return get_child_from_db(pals)


if __name__ == '__main__':
    config = Config()
    config.bind = ['localhost:40001']

    # Running the server and addresses the calls as entered
    asyncio.run(serve(app, config))
