# this file will create function in order to verify if the user is logged in or not,
# to log in the user, and to log out the user.
from flask import make_response, redirect, url_for, request
import os

def login_user(user):
    # this function will log in the user
    # it will do so by creating a cookie that will be stored in the user's browser

    # create a cookie
    response = make_response(redirect(url_for("main.index")))
    secret = os.urandom(32)
    response.set_cookie(user, secret)
    return response

def logout_user(user):
    # this function will log out the user
    # it will do so by deleting the cookie that is stored in the user's browser
    response = make_response(redirect(url_for("main.index")))
    response.delete_cookie(user)
    return response

def verify_login(user):
    # this function will verify if the user is logged in or not
    # it will do so by checking if the cookie is stored in the user's browser
    cookie = request.cookies.get(user)
    if cookie:
        return True
    else:
        return False