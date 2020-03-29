from getpass import getpass
import sys

from webapp import create_app
from webapp.user.models import db, User

app = create_app()

with app.app_context():
    username = input('Введите имя:')

    if User.query.filter(User.username == username).count():
        print('Пользователь с таким именем уже существует')
        sys.exit(0)

    password1 = getpass('Введите пароль')
    password2 = getpass('Повторите пароль')

    if not password1 == password2:
        print('Пароли не одинаковые')
        sys.exit(0)

# >>> admin = User(username='admin', email='admin@example.com')
# >>> guest = User(username='guest', email='guest@example.com')
    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))