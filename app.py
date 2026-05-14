# with smart ia duck as helper https://cs50.ai/
from cs50 import SQL
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
)
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, sacar_resultados

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///resultados.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    if not db.execute("SELECT * FROM concursos;"):
        msg = "Please build a database for results"
        return render_template("index.html", msg=msg)
    else:
        msg = "Most recent result is:"

        concurso = db.execute(
            "SELECT concurso FROM concursos ORDER BY concurso DESC LIMIT 1;"
        )[0]["concurso"]
        n1 = db.execute("SELECT n1 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n1"
        ]
        n2 = db.execute("SELECT n2 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n2"
        ]
        n3 = db.execute("SELECT n3 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n3"
        ]
        n4 = db.execute("SELECT n4 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n4"
        ]
        n5 = db.execute("SELECT n5 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n5"
        ]
        n6 = db.execute("SELECT n6 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n6"
        ]

        return render_template(
            "index.html",
            msg=msg,
            concurso=concurso,
            n1=n1,
            n2=n2,
            n3=n3,
            n4=n4,
            n5=n5,
            n6=n6,
        )


@app.route("/build_db", methods=["GET", "POST"])
@login_required
def build_db():
    if request.method == "POST":
        # Ensure ano was submitted
        if not request.form.get("ano"):
            return apology("must provide ano", 403)

        ano = request.form.get("ano")

        sacar_resultados(ano)

        with open("csv/Resultados " + ano + ".csv", "r") as file:
            for line in file:
                if line.startswith("/resultados/"):
                    concurso = line.strip().split("/")[-1]
                else:
                    data = line.strip().split(",")
                    n1 = data[0]
                    n2 = data[1]
                    n3 = data[2]
                    n4 = data[3]
                    n5 = data[4]
                    n6 = data[5]

                    # if not yet there, create
                    db_exists = db.execute(
                        "SELECT concurso FROM concursos WHERE concurso = ?;", concurso
                    )
                    if len(db_exists) == 0:
                        db.execute(
                            "INSERT INTO concursos (concurso, n1, n2, n3, n4, n5, n6) VALUES (?, ?, ?, ?, ?, ?, ?);",
                            concurso,
                            n1,
                            n2,
                            n3,
                            n4,
                            n5,
                            n6,
                        )

        concurso = db.execute(
            "SELECT concurso FROM concursos ORDER BY concurso DESC LIMIT 1;"
        )[0]["concurso"]
        n1 = db.execute("SELECT n1 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n1"
        ]
        n2 = db.execute("SELECT n2 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n2"
        ]
        n3 = db.execute("SELECT n3 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n3"
        ]
        n4 = db.execute("SELECT n4 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n4"
        ]
        n5 = db.execute("SELECT n5 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n5"
        ]
        n6 = db.execute("SELECT n6 FROM concursos WHERE concurso = ?;", concurso)[0][
            "n6"
        ]

        return render_template(
            "index.html",
            msg="Database created, most recent result is:",
            concurso=concurso,
            n1=n1,
            n2=n2,
            n3=n3,
            n4=n4,
            n5=n5,
            n6=n6,
        )

    return render_template("build_db.html")


@app.route("/tops", methods=["GET", "POST"])
@login_required
def tops():
    if request.method == "POST":
        if not request.form.get("tops"):
            return apology("select how many tops you want", 403)

        tops = request.form.get("tops")

        if tops == "6":
            result = db.execute(
                "SELECT number, COUNT(*) as count FROM (SELECT n1 as number FROM concursos UNION ALL SELECT n2 FROM concursos UNION ALL SELECT n3 FROM concursos UNION ALL SELECT n4 FROM concursos UNION ALL SELECT n5 FROM concursos UNION ALL SELECT n6 FROM concursos) AS combined GROUP BY number ORDER BY count DESC LIMIT 6;"
            )
            return render_template("tops.html", tops=tops, result=result)
        elif tops == "10":
            result = db.execute(
                "SELECT number, COUNT(*) as count FROM (SELECT n1 as number FROM concursos UNION ALL SELECT n2 FROM concursos UNION ALL SELECT n3 FROM concursos UNION ALL SELECT n4 FROM concursos UNION ALL SELECT n5 FROM concursos UNION ALL SELECT n6 FROM concursos) AS combined GROUP BY number ORDER BY count DESC LIMIT 10;"
            )
            return render_template("tops.html", tops=tops, result=result)
        elif tops == "20":
            result = db.execute(
                "SELECT number, COUNT(*) as count FROM (SELECT n1 as number FROM concursos UNION ALL SELECT n2 FROM concursos UNION ALL SELECT n3 FROM concursos UNION ALL SELECT n4 FROM concursos UNION ALL SELECT n5 FROM concursos UNION ALL SELECT n6 FROM concursos) AS combined GROUP BY number ORDER BY count DESC LIMIT 20;"
            )
            return render_template("tops.html", tops=tops, result=result)
        elif tops == "50":
            result = db.execute(
                "SELECT number, COUNT(*) as count FROM (SELECT n1 as number FROM concursos UNION ALL SELECT n2 FROM concursos UNION ALL SELECT n3 FROM concursos UNION ALL SELECT n4 FROM concursos UNION ALL SELECT n5 FROM concursos UNION ALL SELECT n6 FROM concursos) AS combined GROUP BY number ORDER BY count DESC LIMIT 50;"
            )
            return render_template("tops.html", tops=tops, result=result)
        elif tops == "all":
            result = db.execute(
                "SELECT number, COUNT(*) as count FROM (SELECT n1 as number FROM concursos UNION ALL SELECT n2 FROM concursos UNION ALL SELECT n3 FROM concursos UNION ALL SELECT n4 FROM concursos UNION ALL SELECT n5 FROM concursos UNION ALL SELECT n6 FROM concursos) AS combined GROUP BY number ORDER BY count DESC;"
            )
            return render_template("tops.html", tops=tops, result=result)
        else:
            return render_template("tops.html")

    else:
        return render_template("tops.html")


@app.route("/frequence", methods=["GET", "POST"])
@login_required
def frequence():
    # find db
    concursos = db.execute("SELECT concurso FROM concursos ORDER BY concurso DESC;")

    if not concursos:
        return apology("must create database", 403)

    # create initial frequence
    frequence = {}

    # get user inputs
    if request.method == "POST":
        # ensure concurso inicial was provided
        if not request.form.get("concurso_inicial"):
            return apology("must provide concurso inicial", 403)
        # ensure concurso final was provided
        if not request.form.get("concurso_final"):
            return apology("must provide concurso final", 403)

        # define variables
        concurso_inicial = request.form.get("concurso_inicial")
        concurso_final = request.form.get("concurso_final")

        try:
            concurso_inicial = int(concurso_inicial)
            concurso_final = int(concurso_final)

        except:
            return apology("not an integer", 403)

        if concurso_final > concurso_inicial:
            return apology("concurso final must be lower", 403)

        gap = concurso_inicial - concurso_final

        # select numbers and concursos
        n_concursos_resultados = db.execute(
            "SELECT concurso, n1, n2, n3, n4, n5, n6 FROM concursos WHERE concurso BETWEEN ? AND ?;",
            concurso_final,
            concurso_inicial,
        )

        # setup dictionaries
        data = {}
        frequence = {number: 0 for number in range(1, 61)}

        #  calculate frequences
        for i in n_concursos_resultados:
            concurso = i["concurso"]
            resultado = [
                int(i["n1"]),
                int(i["n2"]),
                int(i["n3"]),
                int(i["n4"]),
                int(i["n5"]),
                int(i["n6"]),
            ]
            frequence_concurso = {number: 0 for number in range(1, 61)}
            for n in frequence:
                if n in resultado:
                    frequence[n] += 1
                    frequence_concurso[n] += 1

            data[concurso] = frequence_concurso

        frequence = dict(
            sorted(frequence.items(), key=lambda item: item[1], reverse=True)
        )

        return render_template(
            "frequence.html",
            concursos=concursos,
            concurso_inicial=concurso_inicial,
            concurso_final=concurso_final,
            frequence=frequence,
            gap=gap,
        )

    else:
        return render_template(
            "frequence.html", concursos=concursos, frequence=frequence
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmatin was submitted
        if not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Define names
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if username already there

        registered_username = db.execute(
            "SELECT username FROM users WHERE username = ?", username
        )

        if registered_username:
            registered_username = registered_username[0]["username"]
            if username == registered_username:
                return apology("username already exists", 400)

        # Confirm password
        if password != confirmation:
            return apology("password do not match", 400)

        # Create hash for password
        hash = generate_password_hash(password)

        if "agree" in request.form:
            # Store username and hash in db
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )

            return render_template("login.html")
        else:
            return apology("you do not agree", 400)

    return render_template("register.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Edit username and password"""

    id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id=?", id)[0]["username"]

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("new_username"):
            return apology("must provide new username", 400)

        # Ensure password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide password", 400)

        # Ensure password confirmatin was submitted
        if not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        new_username = request.form.get("new_username")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Confirm password
        if new_password != confirmation:
            return apology("password do not match", 400)

        # Create hash for password
        hash = generate_password_hash(new_password)

        db.execute(
            "UPDATE users SET username = ?, hash = ? WHERE id = ?;",
            new_username,
            hash,
            id,
        )

        session.clear()
        return redirect("/login")
    else:
        return render_template("account.html", username=username)


@app.route("/resultados")
@login_required
def resultados():
    concursos = db.execute("SELECT * FROM concursos ORDER BY concurso;")
    # select numbers and concursos
    n_concursos_resultados = db.execute(
        "SELECT concurso, n1, n2, n3, n4, n5, n6 FROM concursos ORDER BY concurso DESC;"
    )
    #  calculate frequences
    for i in n_concursos_resultados:
        concurso = i["concurso"]
        n1 = i["n1"]
        n2 = i["n2"]
        n3 = i["n3"]
        n4 = i["n4"]
        n5 = i["n5"]
        n6 = i["n6"]

    return render_template(
        "resultados.html",
        concursos=n_concursos_resultados,
        concurso=concurso,
        n1=n1,
        n2=n2,
        n3=n3,
        n4=n4,
        n5=n5,
        n6=n6,
    )
