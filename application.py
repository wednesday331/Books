#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains book review project Python code to execute with HTML pages."""

import csv,
import os,
import requests

from datetime import datetime
from flask import (
    abort,
    flash,
    Flask,
    logging,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from wtforms import (
    Form, 
    PasswordField,
    StringField, 
    TextAreaField, 
    validators
)

app = Flask(__name__)

app.secret_key = 'secretkey'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
goodreads_key='tLGQQxQlcIbAeYedY1ToHQ'


# The login page from index page:
@app.route('/', methods=['GET','POST'])
def login_1():
    """Enables a person to log in."""
    session.clear()
    if request.method == 'POST':
        username_1 = request.form.get("username")
        password_1=request.form.get("password")
        user=db.execute("""SELECT *
                           FROM accounts
                           WHERE username=:username_1;
                           """, 
                        {"username_1": username_1}).fetchone()
        if user is not None:
            username_id=db.execute("""SELECT id
                                     FROM accounts
                                     WHERE username=:username_1;
                                     """, 
                                  {"username_1": username_1}).fetchone()
            
            password_id=db.execute("""SELECT id
                                  FROM accounts
                                  WHERE password=:password_1;
                                  """, 
                                  {"password_1": password_1}).fetchone()
            if username_id == password_id:
                session["username"] = user["username"]
                return render_template("search.html")
            elif username_id != password_id:
                return render_template("loginnomatch.html")
        elif user is None:
            return render_template("loginnouser.html")
    return render_template("login.html")

# Direct login route:
@app.route('/login', methods=['GET','POST'])
def login():
    """Enables a person to log in."""
    session.clear()
    if request.method == 'POST':
        username_1 = request.form.get("username")
        password_1=request.form.get("password")
        user=db.execute("""SELECT *
                        FROM accounts
                        WHERE username=:username_1;
                        """, 
                        {"username_1": username_1}).fetchone()
        if user is not None:
            username_id=db.execute("""SELECT id
                                  FROM accounts
                                  WHERE username=:username_1;
                                  """, 
                                  {"username_1": username_1}).fetchone()
            password_id=db.execute("""SELECT id
                                  FROM accounts
                                  WHERE password=:password_1;
                                  """, 
                                  {"password_1": password_1}).fetchone()
            if username_id == password_id:
                session["username"] = user["username"]
                return render_template("search.html")
            elif username_id != password_id:
                return render_template("loginnomatch.html")
        elif user is None:
            return render_template("loginnouser.html")
    return render_template("login.html")

# The signup/registration page:
@app.route('/registration', methods=['GET','POST'])
def registration():
    """Enables a person to register an account."""
    if request.method == "POST":
        if request.form.get("password") != request.form.get("confirm"):
            return render_template("signupnomatch.html")
        else:
            username_1 = request.form.get("username")
            user=db.execute("""SELECT *
                            FROM accounts
                            WHERE username=:username_1;
                            """, 
                            {"username_1": username_1}).fetchone()
            if user is None:
                password_1=request.form.get("password")
                db.execute("""INSERT INTO accounts (username, password)
                              VALUES (:username_1, :password_1)
                              """,
                           {"username_1": username_1, "password_1": password_1})                
                db.commit()
                return render_template("loginaftercreating.html")
            else:
                return render_template("signupuserexists.html")
    else:
        return render_template("signup.html")

#Logout
@app.route("/logout")
def logout():
    """Enables a person to logout."""
    session.clear()
    return render_template("logout.html")

#Search page
@app.route("/search", methods=['GET','POST'])
def search():
    """"Contains the different search functionalities."""
    if not session:
        return render_template("logintosearch.html")
    if request.method == "POST":
        if request.form.get("search"):
            search=request.form.get("search").lower()
            search_1= "%"+search+"%"
            books = db.execute("""SELECT *
                               FROM booklist
                               WHERE lower(title)
                               LIKE :search OR lower(author)
                               LIKE :search OR lower(isbn)
                               LIKE :search
                               """,
                               {"search": search_1}).fetchall()
            if books ==[]:
                return render_template("searchresultsnobooks.html", books=books)
            return render_template("searchresults.html", books=books)
    return render_template("search.html")



# Book Page
@app.route("/<string:isbn>", methods=["GET", "POST"])
def book_page(isbn):
    """Retrieves the appropriate page for the book."""
    book_1= db.execute("""SELECT *
                      FROM booklist
                      WHERE isbn=:isbn
                      """, 
                      {"isbn": isbn}).fetchone()
    if book_1 is None:
        abort(404)
    res= requests.get("https://www.goodreads.com/book/review_counts.json", 
                      params={"key": goodreads_key, "isbns":isbn})
    stars=[1,2,3,4,5]
    existing_reviews=db.execute("""SELECT *
                               from reviews
                               WHERE book=:title
                               """,
                               {"title": book_1[1]}).fetchall()
    if res.status_code==200:
        average_rating=res.json()["books"][0]["average_rating"]
        work_ratings_count=res.json()["books"][0]["work_ratings_count"]
    else:
        average_rating=["Not Available"]
        work_ratings_count=["Not Available"]
    if request.method == "POST":
        star =request.form.get('star')
        comment=request.form.get('comment')
        username=session["username"]
        date=datetime.today()
        rev_data=db.execute("""SELECT *
                           FROM reviews
                           WHERE username=:username
                           AND  book=:title
                           """, 
                           {"username":username, "title": book1[1]}
                          ).fetchall()
        if rev_data:
            return render_template("reviewalreadysubmitted.html", 
                                   existing_reviews=existing_reviews, 
                                   book_1=book_1, 
                                   isbn=isbn, 
                                   average_rating=average_rating, 
                                   work_ratings_count=work_ratings_count, 
                                   stars=stars
                                  )
        else:
            db.execute("""INSERT into reviews (username,
                                               book, 
                                               comment, 
                                               date, 
                                               star)
                          VALUES (:username,
                                  :book, 
                                  :comment, 
                                  :date, 
                                  :star)
                       """, 
                       {"username": username,
                        "book": book1[1],
                        "comment": comment,
                        "date": date,
                        "star": star}
                      )
            
            db.commit()
            return render_template('reviewsubmittedsuccessfully.html', 
                                   existing_reviews=existing_reviews, 
                                   book_1=book_1, 
                                   isbn=isbn, 
                                   average_rating=average_rating, 
                                   work_ratings_count=work_ratings_count, 
                                   stars=stars
                                  )
    return render_template('book.html', 
                           existing_reviews=existing_reviews, 
                           book_1=book_1,
                           isbn=isbn, 
                           average_rating=average_rating, 
                           work_ratings_count=work_ratings_count, 
                           stars=stars
                          )

#API function
@app.route("/api/<isbn>", methods=["GET", "POST"])
def api(isbn):
    """Returns information when the API is given."""
    book_1= db.execute("""SELECT *
                      FROM booklist
                      WHERE isbn=:isbn
                      """, 
                      {"isbn": isbn}).fetchone()
    if book_1 is None:
        abort(404)
    reviews= db.execute("""SELECT *
                        FROM reviews
                        WHERE book=:title
                        """, 
                        {"title": book1[1]}).fetchall()
    review_count=len(reviews)
    if review_count==0:
        average_score="N/A"
    else:
        avg_rating=db.execute("""SELECT avg(star) from reviews
                             WHERE book=:title
                             """,
                             {"title": book1[1]}).fetchall()
        average_score='%.1f' % int(avg_rating[0][0])
    return render_template('apiresponse.html', 
                           book_1=book_1, 
                           review_count=review_count, 
                           average_score=average_score, 
                           reviews=reviews
                          )
