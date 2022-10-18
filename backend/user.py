from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

# encryption
from werkzeug.security import generate_password_hash, check_password_hash


user_blueprint = Blueprint('user', __name__)

