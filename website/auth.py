from flask import Blueprint, render_template, redirect , url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password.', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html")

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':    
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")

        email_exists = User.query.filter_by(email=email).first()
        usernmae_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email already exits', category='error')
        elif usernmae_exists:
            flash('Username already exists', category='error')
        elif password!=repassword:
            flash('Password do not match!', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(password) <=7 :
            flash('Password should be minimum 8 characters', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))


    return render_template("signup.html")
    
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))