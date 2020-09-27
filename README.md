# Project 1
This submission contains code to build a book search and review website using HTML, PostgreSQL, flask and python.


Application.py:
This is the main python file than contains all the flask routes for the web application. The main routes include: login, search, bookpage (containing book information and reviews), logout, and the API response.  

Templates Folder:
Contains all the HTML files used in application.py. All of the html files extend base.html (except for base.html!).

import.py:
Converts the CSV file to a readable format and was then inserted into the booklist table.


Other Key things:
-The app routes for '/' and '/login' contain the same code.
-There's no file for creating the reviews and accounts tables because I have just manually created them in Adminer.
-Some of what has been imported was not used in the code.
