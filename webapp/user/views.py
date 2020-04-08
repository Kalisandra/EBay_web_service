from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.user.get_user_token import get_token_url, get_token

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/')
def login():
    if current_user.is_authenticated and current_user.session_id_status \
        and current_user.token is None:
        return redirect(url_for('user.redirect_user'))
    elif current_user.is_authenticated and current_user.token:
        return redirect(url_for('search.search'))
    else:
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт')
            return redirect(url_for('user.redirect_user'))

    flash('Неправильное имя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('user.login'))


@blueprint.route('/get_token')
def redirect_user():
    title = "Привязать аккаунт eBay"
    token_url = get_token_url()
    return render_template('get_token/get_token.html', page_title=title, get_token_url=token_url)


@blueprint.route('/token')
def recieve_user_token():
    # после подтверждения пользователем допуска к своим данным Ebay,
    # он перенаправляется на домашнюю страницу где запускается функция получения токена
    if current_user.is_authenticated and current_user.session_id_status \
        and not current_user.token:
        get_token()
        title = "Вы успешно подключили ваш Ebay-аккаунт"
        return render_template('get_token/get_token_success.html', page_title=title)
    elif current_user.is_authenticated and current_user.token:
        return redirect(url_for('search.search'))
    else:
        redirect(url_for('index'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect('get_token.html')
    form = RegistrationForm()
    title = "Регистрация"
    return render_template('user/registration.html', page_title=title, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error)
                )
    return redirect(url_for('user.register'))
    flash('Пожалуйста, исправьте ошибки в форме')
    return redirect(url_for('user.register'))
