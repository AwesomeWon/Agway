from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import Flask
from public import public
from users import users

testing = True
db = SQLAlchemy()
DB_NAME = 'datebase.db'

views = Blueprint('views', __name__)

listOfPeople = []

app = Flask(__name__)
app.register_blueprint(public, url_prefix="")
app.register_blueprint(users, url_prefix="/user")
app.secret_key = "Ilove2rob"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)
db.init_app(app)


class Person:
    def __init__(self, name, info='no info', images=['graphics/Awgay flag.PNG'], auther='unknown', date='00/00/0000'):
        self.name = name
        self.info = info
        self.auther = auther
        self.date = date
        self.imagelist = images
        listOfPeople.append(self)

    def dissplayInfo(self):
        print("name = " + str(self.name))
        print("info = " + str(self.info))
        print("images = " + str(self.imagelist))
        print("auther = " + str(self.auther))
        print("date = " + str(self.date))


class Account(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email, post=[]):
        self.name = name
        self.email = email
        self.post = post


with app.app_context():
    db.create_all()


def pick(picked):
    classInstance = Person('person', info='this is a very intresting person')
    for number in range(0, len(listOfPeople)):
        example = listOfPeople[number]
        if example.name == picked:
            classInstance = listOfPeople[number]
    return classInstance


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


Thomas = Person('Thomas', 'Thomas is the king of Urigway', ['graphics/Thomas-thumbsUp.jpeg'], 'Thomas', '12/08/2008')


devs = ["Thomas"]


@app.route("/")
def home():
    length = len(listOfPeople)
    info_list = []
    person_list = []
    for n in range(0, length):
        info_list.append(listOfPeople[n].name)
        person_list.append(listOfPeople[n].info)
    return render_template('indez.html', listOfPeople=info_list, listOfInfo=person_list, length=length)


@app.route("/py", methods=["POST", "GET"])
def python():
    if request.method == 'POST':
        code = request.form["code"]
        if code == "Ilove2rob":
            flash("code successfully entered", "message")
        elif code.lower() == "css":
            return redirect(url_for("css"))
        elif code == "69" or code == "420":
            return redirect(url_for("notFunny"))
        else:
            flash("wrong code", "message")
    return render_template("Python_test.html", devs=devs)


@app.route("/notFunny")
def notFunny():
    return "<h1>you are not funny<h1>"


@app.route("/CSS")
def css():
    return render_template('newHome.html')


@app.route("/view")
def view():
    return render_template("view.html", values=Account.query.all())


@app.route("/data")
def get_data():
    data = request.json
    return jsonify(data)


@app.route("/info/<name>")
def info(name):
    userView = pick(name)
    return render_template("Python_test.html", name=userView.name, text=userView.info, imageSRC=userView.imagelist,
                           date=userView.date, auther=userView.auther)


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


@app.route("/user/<usr>", methods=["POST", "GET"])
def user(usr):
    return render_template('user.html', user=usr)


@app.route("/login2", methods=["POST", "GET"])
def login2():
    if request.method == 'POST':
        session.permanent = True
        account = request.form["nm"]
        session["account"] = account

        found_account = Account.query.filter_by(name=account).first()
        if found_account:
            session["email"] = found_account.email
        else:
            usr = Account(account, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login successful", "info")
        return redirect(url_for("account"))
    else:
        if "account" in session:
            flash("all-ready loggen in", "info")
            return redirect(url_for("account"))

        return render_template('login2.html')


@app.route("/account", methods=["POST", "GET"])
def account():
    # post = None
    email = None
    if "account" in session:
        usr = session["account"]

        if request.method == "POST":
            print(str(request.form))
            email = request.form["email"]
            session["email"] = email
            found_account = Account.query.filter_by(name=usr).first()
            found_account.email = email
            db.session.commit()
            flash("changes made", "info")
        else:
            if "email" in session:
                email = session["email"]

        # return render_template('user.html', user=usr, post=post, email=email)
        return render_template('user.html', user=usr, email=email)
    else:
        flash("Not logged in", "error")
        return redirect(url_for("home"))


@app.route("/logout")
def logout():
    if "account" in session:
        usr = session["account"]
        flash(f"You have benn logged out of account {usr} .", "info")
    session.pop("account", None)
    session.pop("post", None)
    return redirect(url_for("home"))


if __name__ == '__main__':
    if testing:
        app.run(debug=True, port=8000)
    else:
        app.run(debug=False)
