from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

FLAG = "flag{byp4ss_http_m3th0d}"


FAKE_USERS = {
    "admin": "password123",
    "testuser": "test123",
}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if "'" in username or "'" in password:
            return render_template("register.html", error="SQL Error: Invalid input detected!")
        if username in FAKE_USERS:
            return render_template("register.html", error="User already exists!")
        FAKE_USERS[username] = password
        return render_template("register.html", success="User registered successfully!")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in FAKE_USERS and FAKE_USERS[username] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password!")

    return render_template("login.html")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session["username"])
    return redirect(url_for("login"))


@app.route("/admin", methods=["GET", "POST", "HEAD", "OPTIONS"])
def admin():
    if request.method == "HEAD":
        response = app.response_class(status=200)
        response.headers["X-Flag"] = FLAG
        return response
    else:
        return render_template("forbidden.html"), 403
        
@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
