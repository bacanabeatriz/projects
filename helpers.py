from bs4 import BeautifulSoup
import csv
import requests

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def sacar_resultados(ano):
    # create filename for results
    filename = "Resultados " + ano

    # get info from web and create a file for it
    # create a file to copy results
    with open("resultados/" + filename, "w") as f:
        site = requests.get("https://www.megasena.com/resultados/ano-" + ano)

        if not site:
            return 404

        soup = BeautifulSoup(site.text, "html.parser")

        for link in soup.find_all("a"):
            href = link.get("href")
            title = link.get("title")
            if "resultados/" in href and "Mega Sena Concurso" in title:
                f.write(href + "\n")
                ball = link.find_next(class_="ball")
                count = 0
                while ball is not None and count < 6:
                    f.write(ball.text + " ")
                    ball = ball.find_next(class_="ball")
                    count += 1
                f.write("\n")

    with open("resultados/Resultados " + ano, "r") as file:
        concurso = 0
        numeros = " "
        for line in file:
            # Split the line into fields
            data = line.strip().split(" ")

            # find concursos
            if line.startswith("/resultados/"):
                concurso = line.strip().split("/")[-1]
            else:
                numeros = data
    with open("csv/" + filename + ".csv", "w", newline="") as file2:
        writer = csv.writer(file2)

        with open("resultados/Resultados " + ano, "r") as file3:
            for line in file3:
                # Split the line into fields
                data = line.strip().split(" ")
                writer.writerow(data)
