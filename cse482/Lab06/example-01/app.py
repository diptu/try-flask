from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect,
    url_for,
    make_response,
)
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)


# Load environment variables from config.env file
load_dotenv("config.env")

# Access the variables
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("TRACK_MODIFICATIONS")


# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(
        db.Enum(
            "Fantasy",
            "Science fiction",
            "Mystery",
            "Horror",
            "Romance",
            "Historical fiction",
            "Biography",
            "History",
            "Self-help",
            "Travel",
            "Cookbook",
        ),
        nullable=False,
    )
    year_published = db.Column(
        db.Integer, default=datetime.utcnow().year, nullable=False
    )
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


# Create the database tables
with app.app_context():
    db.create_all()


# @app.route("/setCookie")
def set_cookie(name, value):
    response = make_response("Cookie is set")
    response.set_cookie(name, value)
    return response


# Home route
@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)


# Create a new book
@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title")
    author = request.form.get("author")
    genre = request.form.get("genre")
    remember_me = request.form.get("remember")
    print(f"remember_me: {remember_me}")
    new_book = Book(title=title, author=author, genre=genre)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for("index"))


# Update a book
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    book = Book.query.get(id)
    if request.method == "POST":
        book.title = request.form.get("title")
        book.author = request.form.get("author")
        book.genre = request.form.get("genre")
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", book=book)


# Delete a book
@app.route("/delete/<int:id>")
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html", title="about")


if __name__ == "__main__":
    app.run(debug=True)
