from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Backend API URL
BACKEND_URL = "http://127.0.0.1:9000"


# TASK 1: DISPLAY FRONTEND FORM
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        course = request.form.get("course", "").strip()

        if not name or not email or not course:
            return render_template(
                "index.html",
                error="All fields are required!",
                name=name,
                email=email,
                course=course
            )

        student = {
            "name": name,
            "email": email,
            "course": course
        }

        # Send data to Backend API
        response = requests.post(
            f"{BACKEND_URL}/students",
            json=student
        )

        if response.status_code == 201:
            return redirect(url_for("success"))

        error = response.json().get(
            "error",
            "Unable to submit student data!"
        )

        return render_template(
            "index.html",
            error=error,
            name=name,
            email=email,
            course=course
        )

    return render_template("index.html")


# TASK 2: SUCCESS PAGE
@app.route("/success")
def success():

    return render_template("success.html")


# TASK 3: VIEW DATA FROM BACKEND API
@app.route("/view-data")
def view_data():

    response = requests.get(f"{BACKEND_URL}/api")

    return response.json()


if __name__ == "__main__":
    app.run(port=5000, debug=True)
