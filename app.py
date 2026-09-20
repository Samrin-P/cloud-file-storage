from flask import Flask, redirect, url_for, render_template, request   
import sqlite3
import os

app = Flask(__name__)

DATABASE = "database.db"


def create_database():
    connection = sqlite3.connect(DATABASE, timeout=10)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            connection = sqlite3.connect(DATABASE, timeout=10)
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )

            connection.commit()
            connection.close()

            return "Registration successful!"

        except sqlite3.IntegrityError:
            return "This email is already registered. Please use another email."

        except sqlite3.OperationalError:
            return "Database is busy. Please stop the server and try again."

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect(DATABASE, timeout=10)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )

        user = cursor.fetchone()

        connection.close()

        if user:
            return redirect(url_for("dashboard"))
        else:
            return "Invalid email or password!"

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if request.method == "POST":

        file = request.files["file"]

        if file:
            upload_folder = "uploads"

            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            file.save(os.path.join(upload_folder, file.filename))

            return "File uploaded successfully!"

    return render_template("dashboard.html")

@app.route("/download/<filename>")
def download_file(filename):
    from flask import send_from_directory
    return send_from_directory("uploads", filename, as_attachment=True)


if __name__ == "__main__":
    create_database()
    app.run(debug=True, use_reloader=False)


    