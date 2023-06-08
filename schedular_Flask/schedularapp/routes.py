from crypt import methods
from nis import cat
import re
from turtle import RawTurtle
from flask import render_template, redirect, flash, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from schedularapp import app, db
from .models import Task, User


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('homepage.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        fetch = User.query.filter(User.email == email).first()
        check = check_password_hash(fetch.password, password)
        if email != "" and check:
            session['user'] = fetch.user_id
            return redirect(url_for('alltask'))
        else:
            flash('username or password incorrect', category='warning')
            return redirect(url_for('home'))

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        pwd = request.form.get('password')
        confirm_pwd = request.form.get('password-2')
        if name and lastname and email and pwd:
            if pwd == confirm_pwd:
                hashpwd = generate_password_hash(pwd)
                insert = User(email = email, firstname = name, lastname = lastname, password = hashpwd)
                db.session.add(insert)
                db.session.commit()
                flash('Account created successfully', category='success')
                return redirect(url_for('notification'))
            else:
                flash('Password must match', category='error')
        else:
            flash('please complete all the fields', category='warning')
            return redirect(url_for('register'))
    else:
        return render_template('signuppage.html')

@app.route('/alltasks/')
def alltask():
    if session.get('user') != None:
        user = db.session.query(User).get(session['user'])
        tasks = Task.query.filter(Task.user_id == session['user']).all()
        return render_template('alltasks.html', tasks = tasks, user = user)
    else:
        return redirect('/')

@app.route('/newtask', methods=['POST', 'GET'])
def newtask():
    if session.get('user') != None:
        if request.method == 'POST':
            title = request.form.get('title')
            notes = request.form.get('note')
            date = request.form.get('date')
            if title and notes and date:
                task = Task(title = title, notes = notes, date = date, user_id = session['user'])
                db.session.add(task)
                db.session.commit()
                flash('Task created successfully', category='success')
                return redirect(url_for('notification'))
            else:
                flash('please complete the fields', category='warning')
                return redirect(url_for('newtask'))
        else:
            user = User.query.get(session['user'])
            return render_template('newtask.html', user = user)
    else:
        return redirect(url_for('home'))

@app.route('/task_details/<id>')
def task_details(id):
    if session.get('user') != None:
        task = Task.query.get(id)
        user = User.query.get(session['user'])
        return render_template('dashboard.html', task = task, user = user)
    else:
        return redirect('/')

@app.route('/notification')
def notification():
    if session.get('user')!= None:
        return render_template('task_notification.html')
    else:
        return render_template('signin_notification.html')

@app.route('/completed/<id>', methods = ['POST', 'GET'])
def completed(id):
    if session.get('user') != None:
        if request.method == 'GET':
            return redirect(url_for('alltask'))
        else:
            update = request.form.get('taskupdate')
            task = Task.query.get(id)
            task.status = update
            db.session.commit()
            return redirect(url_for('alltask'))
    else:
        return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete(id):
    if session.get('user') != None:
        task = Task.query.get(id)
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('alltask'))

@app.route('/signout')
def signout():
    if session.get('user') != None:
        session.pop('user', None)
        return redirect(url_for('home'))
