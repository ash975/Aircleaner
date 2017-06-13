import json

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from app import User
from app import mongo
from app.util import bson_to_json
from . import users
from app.forms import RegisterForm, LoginForm


# @users.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         username = form.username.data
#         password = form.password.data
#         repeat_password = form.repeat.data
#         if password != repeat_password:
#             flash('两次密码不相同', 'WARNING')
#         elif mongo.db.users.find_one({'email': email}) is not None:
#             flash('该邮箱已被注册', 'WARNING')
#         else:
#             mongo.db.users.insert({'email': email, 'username': username,
#                                    'password': User.gen_password_hash(password)})
#     return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # flash('欢迎使用，请登录', 'WARNING')
    if form.validate_on_submit():
        # db_user = (mongo.db['user_current'].find_one({'username': form.username.data}))
        db_user = (mongo.db['user_current'].find_one({'username': 'aircleaner'}))
        if db_user is not None:
            db_password = db_user.get('password', None)
            if User.verify_password(db_password, form.password.data):
                user = User(db_user['_id'])
                login_user(user)
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('密码错误，请重试', 'WARNING')

    return render_template('login.html', form=form)


# @users.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html')


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))