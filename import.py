import os, csv


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
#------------------------------
def main():
    #Reading the csv file and uploading it to the booklist table
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader: # loop gives each column a name
        if "isbn" in isbn:
            continue #skips the title row to avoid error.
        print(f"Added {title} by{author}, with isbn {isbn}, published {year}.")

        db.execute("INSERT INTO booklist (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year":year}) # substitute values from CSV line into SQL command, as per this dict
    db.commit() 

if __name__=="__main__":
    main()
