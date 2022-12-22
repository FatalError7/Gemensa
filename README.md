# Gemensa
Gestione Prenotazioni Mensa
Unimensa is a Progressive Web App made by **Luciano d'Agostino** for the project of Web Technologies (University of Naples Parthenope).

The purpose of the PWA is to facilitate a company in the management of reservations for access to the canteen, also incorporating the successful use of the meal and, if necessary, generating the report for accounting.

## The functionalities of the user's account:
* View reservations
* Add a reservation
* Modify a reservation
* Delete a reservation

## The functionalities of the canteen's account:
* Confirm access to the canteen for the booked person
* Get a report of each day
* See how many meals he will have to prepare thanks to the updated data

## The functionalities of the admin's account:
* Manage various accounts


## How to install Gemensa?
1. Create a virtual environment(venv) by terminal: **> py -m venv venv**
2. Move to the folder venv/Scripts: **> cd venv/Scripts**
3. Now activate the virtual environment writing in the terminal "activate": **> activate**
4. Go to project folder and install requirements by requirements.txt file: **> pip install -r requirements.txt**
5. Make sure the python interpreter is configured correctly.
6. Install MongoDB for your operating system.
7. Populate the database with the main accounts by running the "InitDb.py" script in the "ScriptDb" folder
8. To run the application you can use the command: **> flask run -h 0.0.0.0**
9. The app is ready
