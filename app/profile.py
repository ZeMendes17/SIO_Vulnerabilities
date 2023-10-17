from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User
from . import db
import os

profile = Blueprint("profile", __name__)


@profile.route("/profile")
@login_required
def perfil():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template("my-account.html", user=user)


@profile.route("/profile/<int:id>", methods=["GET"])
@login_required
def changeProfile(id):
    user = User.query.filter_by(id=id).first()
    return render_template("profile.html", user=user)


@profile.route("/profile/<int:id>", methods=["POST"])
@login_required
def changeProfileForm(id):
    user = User.query.filter_by(id=id).first()
    name = request.form.get("name")
    username = request.form.get("username")
    phone = request.form.get("phone")
    image = request.files.get("image")
    currentPassword = request.form.get("currentPassword")
    newPassword = request.form.get("newPassword")
    confirmNewPassword = request.form.get("confirmNewPassword")

    if name:
        user.name = name
    if username:
        user.username = username
    if phone:
        user.phone = phone
    if image:
        try:
            user.image = image.filename
            image.save(os.path.join("static/images", image.filename))
        except:
            flash("Erro ao fazer upload da imagem!", category="danger")
    if currentPassword:
        if user.password == currentPassword:
            if newPassword == confirmNewPassword:
                user.password = newPassword
            else:
                flash("Passwords novas não coincidem!", category="danger")
        else:
            flash("Password atual errada!", category="danger")

    flash("Perfil atualizado com sucesso!", category="success")

    db.session.commit()
    return redirect(url_for("profile.changeProfile", id=id))
