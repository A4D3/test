from app import app
from flask import render_template, redirect
from flask import url_for, request, flash
from app.forms import RegisterForm, MyLoginForm, TaskForm
from app.models import User
from flask_login import login_required, login_user, logout_user, current_user

#Création d'une liste de tous les utilisateurs et initialisation de l'admin
users = []
users.append(User(0))
users[0].setUsername("admin")
users[0].setPasswd("2020%dmr")
users[0].changeAdmin()

#Global variables that keeps the current user
#Because I had some troubles with current_user (didn't keep the datas up-to-date)
actual_user = users[0]

################################################################################
#In case of a Error 404
@app.errorhandler(404)
def notFound(error):
    return render_template('error.html')

################################################################################
@app.route('/login', methods=['get', 'post'])
def login():

    global actual_user
    global users

    if current_user.is_authenticated:
        return redirect(url_for('menu'))

    form = MyLoginForm()
    if form.validate_on_submit():
        user_found = False;

        #Trouver l'utilisateur
        for n in range(len(users)):
            if users[n].getUsername() == form.username.data :
                user_found = True
                id = n

        if user_found:

            #Vérifier que c'est le bon mdp
            if form.password.data == users[id].getPasswd():

                #Vérifier que l'utilisateur n'est pas bloqué
                if not users[id].getBlocked():

                    #Mise-à-jour de l'utilisateur actuel
                    actual_user = users[id]

                    user = User(id)
                    login_user(user)
                    return redirect(url_for('menu'))
                else:
                    return render_template('my_login_form.html', form = form, message = "Votre compte est bloqué.")
            else:
                return render_template('my_login_form.html', form = form, message = "Mauvais mot de passe.")
        else:
            return render_template('my_login_form.html', form = form, message = "Mauvais Username.")
    else:
        return render_template('my_login_form.html', form = form, message = "")

################################################################################
# Log out user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('menu'))

################################################################################
@app.route('/register', methods=['get', 'post'])
def register():

    global actual_user
    global users

    form = RegisterForm()
    if form.validate_on_submit():

        #Vérifier que l'username n'est pas déjà utilisé
        for user in users:
            if user.getUsername() == form.username.data:
                return render_template('register.html', form = form, message = "Cet username est déjà utilisé.")

        #Vérifier que les 2 mdp correspondent
        if(form.password.data == form.passwordVerification.data):

            #Vérifier que les inputs ne sont pas juste des espaces
            if notOnlySpaces(form.name.data) and notOnlySpaces(form.surname.data) and notOnlySpaces(form.birth.data) and notOnlySpaces(form.username.data):
                #Enregistrer le nouvel utilisateur
                id = len(users)
                users.append(User(id))
                users[id].setName(form.name.data)
                users[id].setSurname(form.surname.data)
                users[id].setBirth(form.birth.data)
                users[id].setUsername(form.username.data)
                users[id].setPasswd(form.password.data)

                #Login du nouvel utilisateur
                user = User(id)
                actual_user = users[id]
                login_user(user)
                return redirect(url_for('menu'))

            else:
                return render_template('register.html', form = form, message = "Ecrire juste des espaces n'est pas valable.")

        else:
            return render_template('register.html', form = form, message = "Les mots de passe ne correspondent pas.")

    else:
        return render_template('register.html', form = form, message = "")

################################################################################
@app.route("/")
@login_required
def menu():

    global actual_user

    return render_template('menu.html', user = actual_user)

################################################################################
@app.route("/add",methods=['get','post'])
@login_required
def add():

    global actual_user

    form = TaskForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        deadline = form.deadline.data

        #Vérifier que les inputs ne sont pas juste des espaces
        if notOnlySpaces(name) and notOnlySpaces(description) and notOnlySpaces(deadline):

            #Ajouter la nouvelle tâche
            task = {'name' : name,
                    'description' : description,
                    'deadline' : deadline,
                    'done' : False}

            actual_user.addTask(actual_user.getId(), task)
            actual_user.addNTasksNotDone()

            return redirect(url_for('menu'))

        else:
            return render_template('add.html', form = form, message = "Ecrire juste des espaces n'est pas valable.", user = actual_user)
    else:
        return render_template('add.html', form = form, message = "", user = actual_user)

################################################################################
@app.route('/edit/<int:key>',methods=['get','post'])
@login_required
def edit(key):

    global actual_user

    form = TaskForm()
    #Vérifie que la clé existe dans les tâches
    if key in actual_user.getTasks():

        if form.validate_on_submit():

            name = form.name.data
            description = form.description.data
            deadline = form.deadline.data

            #Vérifier que les inputs ne sont pas juste des espaces
            if notOnlySpaces(name) and notOnlySpaces(description) and notOnlySpaces(deadline):

                #Modifier la tâche
                task = {'name' : name,
                        'description' : description,
                        'deadline' : deadline,
                        'done' : actual_user.getTasks()[key]['done']}

                actual_user.editTask(key, task)

                return redirect(url_for('menu'))

            else:
                return render_template('edit.html', form = form, message = "Ecrire juste des espaces n'est pas valable.", user = actual_user, key = key)
    else:
        return redirect(url_for('menu'))

    return render_template('edit.html', form = form, message = "", user = actual_user, key = key)

################################################################################
@app.route('/delete/<int:key>')
@login_required
def delete(key):

    global actual_user

    #Vérifie que la clé existe dans les tâches
    if key in actual_user.getTasks():

        #Si la tâche était pas encore done, diminué de 1 le nombre de tâches not done
        if not actual_user.getTasks()[key]['done']:
            actual_user.substractNTasksNotDone()

            #Supprimer la tâche
        actual_user.deleteTask(key, None)
    return redirect(url_for('menu'))

################################################################################
@app.route('/done/<int:key>')
@login_required
def done(key):

    global actual_user

    #Vérifie que la clé existe dans les tâches
    if key in actual_user.getTasks():
        isDone = actual_user.getTasks()[key]['done']

        #Garde le nombre de tâches not done à jour
        if isDone:
            actual_user.addNTasksNotDone()
        else:
            actual_user.substractNTasksNotDone()

        #Passe la tâche en done ou not done, dépendant de son état de départ
        actual_user.doneTask(key, not isDone)

    return redirect(url_for('menu'))

################################################################################
@app.route('/adminGestion')
@login_required
def adminGestion():

    global actual_user
    global users

    #Vérifier que c'est bien un admin sur la page
    if actual_user.getAdmin():
        return render_template('adminGestion.html', user = actual_user, users = users)
    else:
        return redirect(url_for('menu'))

################################################################################
@app.route('/blocked/<int:key>')
@login_required
def block(key):
    global actual_user
    global users

    #Vérifier que c'est bien un admin sur la page
    if actual_user.getAdmin():

        #Bloquer l'utilisateur
        users[key].setBlocked()
        return redirect(url_for('adminGestion'))
    else:
        return redirect(url_for('menu'))

################################################################################
###############################Utils############################################
################################################################################

#Vérifie qu'un string n'est pas composé que d'espaces
def notOnlySpaces(string):

    for key in range(len(string)):
        if string[key] != " ":
            return True

    return False
