from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change_this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patient_tasks.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='regular')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    patient = db.relationship('Patient', backref=db.backref('tasks', lazy=True))

class TaskLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.String(200))
    task = db.relationship('Task', backref=db.backref('logs', lazy=True))
    user = db.relationship('User')

def color_for_deadline(due_date):
    today = datetime.utcnow().date()
    if due_date < today:
        return 'red'
    elif due_date - today <= timedelta(days=7):
        return 'yellow'
    return 'green'

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks, color_for_deadline=color_for_deadline)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    task = Task.query.get_or_404(task_id)
    task.completed = True
    log = TaskLog(task=task, user_id=session['user_id'], comment='completed')
    db.session.add(log)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
