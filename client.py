""" Client
Enrique Martinez
Palworld Breeding Calculator

Program Description: This is a Palworld Breeding calculator. This client will access the api urls (API endpoints on the
API side) and return the child associated with the given parents. For example, if I were to input Lamball and Cattiva,
it would return Lamball. The program is order sensitive, so it will not give you the child if it is in the incorrect
order or misspelled. It can also print the table of pals incase the user does not already know what pals exist in the
game. Finally, it will also automatically save the successful combinations to a separate table called "saved_combos".
This is for the user to be able to look back at the pals they have already created. Last semester, I had a lot of
trouble with scope, and required a lot of help with my project. This semester, I did this on my own to see if I could
complete it.
"""
import requests
from pals import Pal


# Calling API (server) from the client
def call_api_service():
    # Get the option from the user.
    print("1.) Breed\n2.) List of Pals\n3.) View Saved Combinations\n4.) Terminate\n")
    option = int(input("Please select an option: "))

    # While the client does not wish to terminate, continue
    while option != 4:
        # Match (switch in C/C++)
        match option:
            # Calculate the breed
            case 1:
                input_parent1 = input('Input Parent1: ')
                input_parent2 = input('Input Parent2: ')
                calculate(input_parent1, input_parent2)

            # Print the list of pals to the screen
            case 2:
                print_pals()

            # View the saved combinations.
            case 3:
                print_saved_combos()

            case _:
                print("Please enter one of the provided options.\n")

        # Re obtaining the option from the client
        print("1.) Breed\n2.) List of Pals\n3.) View Saved Combinations\n4.) Terminate\n")
        option = int(input("Please select an option: "))

    print("Goodbye!\n")


# Calls the API to print the list of pals in case the client does not know them
def print_pals() -> None:
    api_url: str = 'http://127.0.0.1:40001/api/pals'

    # The equivalent to connect() in C
    results = requests.get(api_url)

    if results.status_code == 200:
        try:
            for result in results.json():
                print(result)
        except requests.exceptions.JSONDecodeError:
            print(results.text)

    else:
        print(f'Status Code: {results.status_code} | Error Message: {results.text}')


# Calls the API to print the list of Pals we already bred together.
def print_saved_combos() -> None:
    api_url: str = 'http://127.0.0.1:40001/api/saved_combos'

    results = requests.get(api_url)

    if results.status_code == 200:
        try:
            for result in results.json():
                print(result)
        except requests.exceptions.JSONDecodeError:
            print(results.text)
    else:
        print(f'Status Code: {results.status_code} | Error Message: {results.text}')


# Calls the API to print the child
def get_child(pals: Pal) -> None:
    api_url: str = 'http://127.0.0.1:40001/api/get_child'

    results = requests.post(api_url, json=pals.model_dump())

    if results.status_code == 200:
        try:
            child_name = results.json()
            print(f'{child_name}\n')
        except requests.exceptions.JSONDecodeError:
            print(results.text)
    else:
        print(f'Status Code: {results.status_code} | Error Message: {results.text}')


# Calls the function to get the Child of the two parents given by the client
def calculate(Input_Parent1: str, Input_Parent2: str):
    char_request = Pal(parent1=Input_Parent1, parent2=Input_Parent2, child='')
    get_child(char_request)


# Main Function (just calls the api service function).
if __name__ == '__main__':
    # Starts the program and connects to the server. (Where all the work will be done)
    call_api_service()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
