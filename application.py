#URI: postgres://zszqvyfergyvdo:eb1d4ce814801f8b111ac946b1a1a24c22354ce0951ccc0ee528199da0fd2a17@ec2-34-200-72-77.compute-1.amazonaws.com:5432/d9djaumq4kmhi5
#Heroku Password:       eb1d4ce814801f8b111ac946b1a1a24c22354ce0951ccc0ee528199da0fd2a17


import os, csv, requests

from flask import (
    abort,
    Flask,
    flash,
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
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from datetime import datetime

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
#------------------------------------------------------------------

#The login page:
@app.route('/', methods=['GET','POST'])
def login1():
    session.clear()

    if request.method == 'POST':
        username1 = request.form.get("username")
        password1=request.form.get("password")
        user=db.execute("SELECT * FROM accounts WHERE username=:username1;", {"username1": username1}).fetchone()
        if user is not None:
            usernameid=db.execute("SELECT id FROM accounts WHERE username=:username1;", {"username1": username1}).fetchone()
            passwordid=db.execute("SELECT id FROM accounts WHERE password=:password1;", {"password1": password1}).fetchone()

            if usernameid == passwordid:
                session["username"] = user["username"]
                return render_template("search.html")
            elif usernameid != passwordid:
                return render_template("loginnomatch.html")
        elif user is None:
            return render_template("loginnouser.html")
    return render_template("login.html")

#The login page:
@app.route('/login', methods=['GET','POST'])
def login():
    session.clear()

    if request.method == 'POST':
        username1 = request.form.get("username")
        password1=request.form.get("password")
        user=db.execute("SELECT * FROM accounts WHERE username=:username1;", {"username1": username1}).fetchone()
        if user is not None:
            usernameid=db.execute("SELECT id FROM accounts WHERE username=:username1;", {"username1": username1}).fetchone()
            passwordid=db.execute("SELECT id FROM accounts WHERE password=:password1;", {"password1": password1}).fetchone()

            if usernameid == passwordid:
                session["username"] = user["username"]
                return render_template("search.html")
            elif usernameid != passwordid:
                return render_template("loginnomatch.html")
        elif user is None:
            return render_template("loginnouser.html")
    return render_template("login.html")


#The signup/registration page:
@app.route('/registration', methods=['GET','POST'])
def registration():
    if request.method == "POST":
        if request.form.get("password") != request.form.get("confirm"):
            return render_template("signupnomatch.html")
        else:
            username1 = request.form.get("username")
            user=db.execute("SELECT * FROM accounts WHERE username=:username1;", {"username1": username1}).fetchone()
            if user is None:
                password1=request.form.get("password")
                db.execute("INSERT INTO accounts (username, password) VALUES (:username1, :password1)",{"username1": username1, "password1": password1})
                db.commit()
                return render_template("loginaftercreating.html")
            else:
                return render_template("signupuserexists.html")
    else:
        return render_template("signup.html")

#Logout
@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

#Search page
@app.route("/search", methods=['GET','POST'])
def search():
    if not session:
        return render_template("logintosearch.html")
    if request.method == "POST":
        if request.form.get("search"):
            search=request.form.get("search").lower()
            search1= "%"+search+"%"
            books = db.execute("SELECT * FROM booklist WHERE lower(title) LIKE :search OR lower(author) LIKE :search OR lower(isbn) LIKE :search",{"search": search1}).fetchall()
            if books ==[]:
                return render_template("searchresultsnobooks.html", books=books)
            return render_template("searchresults.html", books=books)
    return render_template("search.html")



#Book Page
@app.route("/<string:isbn>", methods=["GET", "POST"])
def bookpage(isbn):
    book1= db.execute("SELECT * FROM booklist WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    if book1 is None:
        abort(404)
    res= requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": goodreads_key, "isbns":isbn})
    stars=[1,2,3,4,5]
    existingreviews=db.execute("SELECT * from reviews WHERE book=:title",{"title": book1[1]}).fetchall()
    if res.status_code==200:
        averagerating=res.json()["books"][0]["average_rating"]
        workratingscount=res.json()["books"][0]["work_ratings_count"]
    else:
        averagerating=["Not Available"]
        workratingscount=["Not Available"]

    if request.method == "POST":
        star =request.form.get('star')
        comment=request.form.get('comment')
        username=session["username"]
        date=datetime.today()
        revdata=db.execute("SELECT * FROM reviews WHERE username=:username AND  book=:title", {"username":username, "title": book1[1]}).fetchall()
        if revdata:
            return render_template("reviewalreadysubmitted.html", existingreviews=existingreviews, book1=book1, isbn=isbn, averagerating=averagerating, workratingscount=workratingscount, stars=stars)
        else:
            db.execute("INSERT into reviews (username, book, comment, date, star) VALUES (:username, :book, :comment, :date, :star)", {"username": username, "book": book1[1], "comment": comment, "date": date, "star": star})
            db.commit()
            return render_template('reviewsubmittedsuccessfully.html', existingreviews=existingreviews, book1=book1, isbn=isbn, averagerating=averagerating, workratingscount=workratingscount, stars=stars)

    return render_template('book.html', existingreviews=existingreviews, book1=book1, isbn=isbn, averagerating=averagerating, workratingscount=workratingscount, stars=stars)

#Returning information when the API is given
@app.route("/api/<isbn>", methods=["GET", "POST"])
def api(isbn):
    book1= db.execute("SELECT * FROM booklist WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    if book1 is None:
        abort(404)
    reviews= db.execute("SELECT * FROM reviews WHERE book=:title", {"title": book1[1]}).fetchall()
    review_count=len(reviews)
    if review_count==0:
        average_score="N/A"
    else:
        avgrating=db.execute("SELECT avg(star) from reviews WHERE book=:title", {"title": book1[1]}).fetchall()
        average_score='%.1f' % int(avgrating[0][0])
    return render_template('apiresponse.html', book1=book1, review_count=review_count, average_score=average_score, reviews=reviews)
