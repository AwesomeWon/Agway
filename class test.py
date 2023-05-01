# Class test
listOfPeople = []
userList = []


class Person:
    def __init__(self, name, info='no info', images=['graphics/Awgay flag.PNG'], auther='unknown', date='00/00/0000'):
        self.name = name
        self.info = info
        self.auther = auther
        self.date = date
        self.imagelist = images
        listOfPeople.append(self)

    def displayInfo(self):
        print("name = " + str(self.name))
        print("info = " + str(self.info))
        print("images = " + str(self.imagelist))
        print("auther = " + str(self.auther))
        print("date = " + str(self.date))


class User:
    def __init__(self, agwayenName, email, password, posts=[]):
        self.name = agwayenName
        self.email = email
        self.password = password
        self.posts = posts
        userList.append(self)

    def displayInfo(self):
        print("user")
        print("    user name = " + str(self.name))
        print("    email = " + str(self.email))
        print("    password = " + str(self.password))
        for post in range(0, len(self.posts)):
            if isinstance((self.posts[post]), str):
                print("    post " + str(post + 1) + " = " + self.posts[post])
            elif isinstance((self.posts[post]), Person):
                printed = self.posts[post]
                print("    post " + str(post + 1) + " = " + str(printed.name))
            else:
                print("    post " + str(post + 1) + " = " + str(self.posts[post]))


def pick(picked, Type):
    if Type == 'person':
        classInstance = Person('person', info='this is a very intresting person')
        for number in range(0, len(listOfPeople)):
            example = listOfPeople[number]
            if example.name == picked:
                classInstance = listOfPeople[number]
    elif Type == 'user':
        classInstance = User('exampleUser', 'user@example.com', 'examplePassword')
        for number in range(0, len(userList)):
            example = userList[number]
            if example.name == picked:
                classInstance = userList[number]
    else:
        classInstance = 'eror'
    return classInstance


thomas = Person('Thomas', 'thomas is cool', ['graphics/Thomas-thumbsUp'], 'Thomas', '04/19/2023')
hugh = Person('Hugh')
usersList = [thomas, hugh, 'mika', 123]
user = User('user', 'user@gmail.com', '12345', posts=usersList)
for n in range(0, len(listOfPeople)):
    print(str(n + 1) + " - " + str(listOfPeople[n].name))
tag = 'Thomas'

user.displayInfo()
display = pick(tag, 'person')
display.displayInfo()
