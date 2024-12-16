from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/bookstore"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"


# Create the database tables
with app.app_context():
    db.create_all()


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


if __name__ == "__main__":
    app.run(debug=True)
