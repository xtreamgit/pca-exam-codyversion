from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

######## Note to Hector: make sure to change the URI to the correct MongoDB Connection.
# Local host connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/examDB"

# Docker container connection
# app.config["MONGO_URI"] = "mongodb://mongo:27017/examDB"
mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Dummy user store
users = {'user@example.com': {'password': 'securepassword'}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('display_question', question_number=1))

    return 'Bad login'

@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

@app.route('/question/<int:question_number>')
# @login_required
def display_question(question_number):
    try:
        question_data = mongo.db.questions.find_one({'number': question_number})
        if not question_data:
            return "Question not found", 404
        return render_template('question.html', question=question_data)
    except Exception as e:
        return f"An error occurred while connecting to the database: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)


















