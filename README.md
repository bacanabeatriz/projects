# FINAL PROJECT CS50: best numbers to play
#### Video Demo:  <https://youtu.be/Nky8S8mtEmk>
#### Description:

This project was written using flask, SQL, werkzeug.security and BeautifulSoup, css, html.

CS50 rubber duck was used in this project as a guide in understanding concepts and debugging the code.

The original idea is to get the results of a popular lottery in Brazil called megasena, get the numbers by year, be able to find the top numbers, also be able to know how often this number shows up between a set of rounds identified by their numbers.

The first screen is a log in page, with option to Register. The register also has a button to commit for terms and conditions. Almost the same as finance pset with some improvments.

After log in, buttons on top screen are: Build db, Tops, Frequence, Results, Account and Log Out.

Account and log out manage the user account for change username and/or password.

In the body of the home page we can see the most recent numbers of the last concurso on the body or a message asking to build a database.

The option for creating the Build db button is that the user can choose which year they want to look at.

The database is built using results that are public and offered in the megasena website whith results from 1996 until today. To be able to access the page and get the information to populate a csv file, Beautiful Soup was used to compose the name of the website and to clean the information. The function sacar_resultados that does it is in helpers file.

The app.py build_db route get the users input for the year they want and creates a new file in a folder called csv where the data is stored inside the program. It does a series of queries in sqlite3 to find the most recent numbers at home page. It also ensures that no duplicated data gets in the concursos table at resultados db. The option for creating a local db is for the case that internet fails or the data becomes unavaible for other reasons.

The tops button show a list of number, top 6, 10, 20, 50 or all. The app route run a series of queries that shows up the results in a table rendered in html. So the user can see which numbers wore more common in all database.

The frequence button leads to a page where the user can select a concurse number from the most recent to the oldest availble in the database. If they want more year, they can build more years in database.

The concurso numbers are loaded in a dropdown menu, making it easier for the user to select. The results in the html table show how often each of 1 to 60 numbers appeared in this set in a ordered table that runs from the biggest frequence to the smaller.

The last button Resultados show all results available in database ordered from the most recent to the oldest.
