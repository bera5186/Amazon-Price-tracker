from flask import Flask, redirect, render_template, session, url_for, request, flash
import requests as r
import time

app = Flask(__name__)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(email, password)
        payload = {"email": email, "password": password}

        response = r.get("http://127.0.0.1:5000/signin", json=payload)
        print(response.status_code)

        if response.status_code == 200:
            userName = r.get("http://127.0.0.1:5000/getuser", json={"email": email})
            print(userName.json()["data"])
            session["username"] = userName.json()["data"]
            session["email"] = email
            return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]

        payload = {"email": email, "username": username, "password": password}

        response = r.post("http://127.0.0.1:5000/signup", json=payload)

        if response.status_code == 201:
            flash(response.json()["message"], "success")
            return redirect(url_for("login"))

        else:
            flash(response.json()["message"], "warning")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login"))
    return "this is dashboard"


@app.route("/loginsucess")
def sucess():
    if "email" in session:
        return render_template("loginsucess.html", user=session["email"])

    return render_template("loginsucess.html")


@app.route("/")
def home():
    if "email" in session:
        print(session["username"])
        return render_template("base.html", user=session["username"])

    return render_template("base.html")


if __name__ == "__main__":
    app.config["SECRET_KEY"] = "this is @$%^&"
    app.run(host="127.0.0.1", port=8000, debug=True)
