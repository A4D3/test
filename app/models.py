from flask_login import UserMixin
from app import login_manager
from flask_login import login_required, login_user, logout_user, current_user

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = "user" + str(id)
        self.password = self.username + "_secret"
        self.name = ""
        self.surname = ""
        self.birth = ""
        self.blocked = False
        self.tasks = {}
        self.nTasksNotDone = 0
        self.id = 0
        self.admin = False

    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName

    def getSurname(self):
        return self.surname

    def setSurname(self, newSurname):
        self.surname = newSurname

    def getBirth(self):
        return self.birth

    def setBirth(self, newBirth):
        self.birth = newBirth

    def getUsername(self):
        return self.username

    def setUsername(self, newUsername):
        self.username = newUsername

    def getPasswd(self):
        return self.password

    def setPasswd(self, newPasswd):
        self.password = newPasswd

    def getBlocked(self):
        return self.blocked

    def setBlocked(self):
        self.blocked = not self.blocked

    def getTasks(self):
        return self.tasks

    def addTask(self, key, task):
        self.tasks[key] = task
        self.id += 1

    def editTask(self, key, task):
        self.tasks[key] = task

    def deleteTask(self, key, none):
        self.tasks.pop(key, none)

    def doneTask(self, key, bool):
        self.tasks[key]['done'] = bool

    def getNTasksNotDone(self):
        return self.nTasksNotDone

    def addNTasksNotDone(self):
        self.nTasksNotDone += 1

    def substractNTasksNotDone(self):
        self.nTasksNotDone -= 1

    def getId(self):
        return self.id

    def changeAdmin(self):
        self.admin = not self.admin

    def getAdmin(self):
        return self.admin


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
