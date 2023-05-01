from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import Flask

db = SQLAlchemy()
DB_NAME = 'datebase.db'


class Account(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email, post=[]):
        self.name = name
        self.email = email
        self.post = post


users = Blueprint("users", __name__, static_folder="static", template_folder="template")


@users.route("/")
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
        return redirect(url_for("users.account"))
    else:
        if "account" in session:
            flash("all-ready loggen in", "info")
            return redirect(url_for("users.account"))

        return render_template('login2.html')


@users.route("/account", methods=["POST", "GET"])
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


@users.route("/logout")
def logout():
    if "account" in session:
        usr = session["account"]
        flash(f"You have benn logged out of account {usr} .", "info")
    session.pop("account", None)
    session.pop("post", None)
    return redirect(url_for("public.home"))


@users.route("/view")
def view():
    return render_template("view.html", values=Account.query.all())
