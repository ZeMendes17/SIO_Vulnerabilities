from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from sqlalchemy import text
from . import db

profile = Blueprint("profile", __name__)


@profile.route("/profile")
@login_required
def perfil():
    return render_template("my-account.html")


@profile.route("/profile/edit", methods=["GET"])
@login_required
def changeProfile():
    return render_template("profile.html")


@profile.route("/profile/edit/<int:id>", methods=["POST"])
@login_required
def changeProfileForm():
    user = User.query.get(id)
    print(user)
