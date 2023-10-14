from sqlite3 import IntegrityError
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from .models import User
from . import db

register = Blueprint("register", __name__)


@register.route("/register")
def regist():
    return render_template("signin.html")


@register.route("/form_signin", methods=["POST"])
def form_signin():
    nome = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    user = request.form["username"]
    key = request.form["password"]
    conf_key = request.form["confirm_password"]

    if key != conf_key:
        flash("Passwords do not match!", "error")
        return redirect(url_for("register.regist"))

    # Crie um novo usuário
    new_user = User(username=user, password=key, name=nome, email=email, phone=phone)

    try:
        # Adicione o usuário ao banco de dados
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main.index"))
    except IntegrityError:
        db.session.rollback()
        flash("Username or email already exists!", "error")
        return redirect(url_for("register.regist"))
