# Book Search/Review Project
## What it is:
The purpose of this project is to showcase my programming skills by creating a local web application similar to Goodreads. The project contains the following elements:
*  Features typical of a book review website. For example, logging in/logging out, searching for books from a database, obtaining APIs for individual books, looking at existing reviews, writing reviews, and rating books.
*  The Goodreads API key and its associated Python code
*  CSS, HTML, CSV files, JSON, Python (Flask), SQL, and Bootstrap 4.

**Demonstration Link:** https://www.youtube.com/watch?v=RhD3aBR1wFE

## The Project Requirements that Were Fulfilled:

1.  **Registration:** 
     *  Users should be able to register for your website, providing (at minimum) a username and password.

2.  **Login:** 
     *  Users, once registered, should be able to log in to your website with their username and password.

3.  **Logout:**
     *  Logged in users should be able to log out of the site.

4.  **Import:** 
     *  books.csv is a spreadsheet of 5000 different books. Each one has an ISBN number, a title, an author, and a publication year. 
     *  In a Python file called import.py separate from your web application, write a program that takes the books and import them into your PostgreSQL database.

5.  **Search:**
     *  Once a user has logged in, they should be taken to a page where they can search for a book.
     *  Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches. 
     *  If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well!

6.  **Book Page:**
     *  When users click on a book from the results of the search page, they should be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.

7.  **Review Submission:**
     *  On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. 
     *  Users should not be able to submit multiple reviews for the same book.

8.  **Goodreads Review Data:**
     *  On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.

9.  **API Access:**
     *  If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score.
