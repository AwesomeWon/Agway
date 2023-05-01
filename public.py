from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session

public = Blueprint("public", __name__, static_folder="static", template_folder="template")

listOfPeople = []
devs = ["Thomas"]


class Person:
    def __init__(self, name, info='no info', images='images/Awgay flag.PNG', auther='unknown', date='00/00/0000'):
        self.name = name
        self.info = info
        self.auther = auther
        self.date = date
        self.imagelist = images
        if self.name != "Person":
            listOfPeople.append(self)

    def dissplayInfo(self):
        print("name = " + str(self.name))
        print("info = " + str(self.info))
        print("images = " + str(self.imagelist))
        print("auther = " + str(self.auther))
        print("date = " + str(self.date))


def pick(picked):
    classInstance = Person('person', info='this is a very intresting person')
    for number in range(0, len(listOfPeople)):
        example = listOfPeople[number]
        if example.name == picked:
            classInstance = listOfPeople[number]
    return classInstance


infoOnTeddy = 'Ted E is the best and that is true.  Ted E is also the King of all of the Agwayens, with "The hall of ' \
              'Doneys" giving there loyalty to him.'

Thomas = Person('Thomas', 'Thomas is the king of Urigway', 'images/Thomas-thumbsUp.jpeg', 'Thomas', '12/02/2008')
Hugh = Person('Hugh', 'Hugh is the chancellor of Paraguay', 'images/Hugh_cake.jpeg', 'Thomas', '##/09/2005')
Owen = Person('Owen', 'Owen is the viceroy of the Agwayen Bua-bua witch some call "Eastern Australia"',
              'images/Owen.JPG', 'Thomas,', '##/##/####')
Ted_E = Person('Ted_E', infoOnTeddy, 'images/Teddy-head.jpeg', 'Common Fact', 'BC 01/04/2987')


@public.route("/home")
@public.route("/")
def home():
    length = len(listOfPeople)
    info_list = []
    person_list = []
    for n in range(0, length):
        info_list.append(listOfPeople[n].name)
        person_list.append(listOfPeople[n].info)
    return render_template('indez.html', listOfPeople=info_list, listOfInfo=person_list, length=length)


@public.route("/py", methods=["POST", "GET"])
def python():
    if request.method == 'POST':
        code = request.form["code"]
        if code == "Ilove2rob":
            flash("code successfully entered", "message")
        elif code.lower() == "css":
            return redirect(url_for("public.css"))
        elif code == "69" or code == "420":
            return redirect(url_for("public.notFunny"))
        else:
            flash("wrong code", "message")
    return render_template("Python_test.html", devs=devs)


@public.route("/notFunny")
def notFunny():
    return "<h1>you are not funny<h1>"


@public.route("/CSS")
def css():
    return render_template('newHome.html')


@public.route("/info/<name>")
def info(name):
    userView = pick(name)
    return render_template("Person.html",
                           name=userView.name,
                           text=userView.info,
                           imageSRC=userView.imagelist,
                           date=userView.date,
                           auther=userView.auther)
