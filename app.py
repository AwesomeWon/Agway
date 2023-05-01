from flask import Flask
from views import views
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.secret_key = "Ilove2rob"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    post = db.Column(db.String(10000))

    def __init__(self, name, email):
        self.name = name
        self.email = email


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000)
