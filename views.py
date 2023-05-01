from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from datetime import timedelta
from flask import Flask
from public import public
from users import users

testing = True

views = Blueprint('views', __name__)

listOfPeople = []

app = Flask(__name__)
app.register_blueprint(public, url_prefix="")
app.register_blueprint(users, url_prefix="/users")
app.secret_key = "Ilove2rob"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)
from users import db
db.init_app(app)


def imageTranslater(wantedTranslated, from_list):
    image = "default"
    for keys, values in from_list.items():
        if wantedTranslated == keys:
            image = values
    return image


def have(dic_from, values_keys):
    if values_keys == "keys":
        new_dic = list(dic_from.keys())
    elif values_keys == "values":
        new_dic = list(dic_from.values())
    else:
        new_dic = dic_from
    return new_dic


@app.route("/data")
def get_data():
    data = request.json
    return jsonify(data)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["email"]
        return redirect(url_for("views.user", usr=user))
    else:
        return render_template('login.html')


@app.route("/signIn", methods=["POST", "GET"])
def signIn():
    if request.method == "POST":
        email = request.form["email"]
        session["used"] = email
        return redirect(url_for("used"))
    else:
        return render_template('signIn.html')


if __name__ == '__main__':
    if testing:
        app.run(debug=True, port=8000)
    else:
        app.run(debug=False)
    with app.app_context():
        db.create_all()
