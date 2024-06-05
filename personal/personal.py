from flask import (Blueprint, render_template, request, session, redirect,
                   url_for)
from const import SITEMENU

personal = Blueprint('app_pers',
                     __name__,
                     template_folder='templates',
                     static_folder='static')


@personal.route('/', methods=['GET', 'POST'])
def personal_site():
    if 'userLogged' not in session:
        return redirect(url_for('authorization'))

    if request.method == 'POST':
        session.pop('userLogged', None)
        session.permanent = False  # отменяем сохранение сессии в браузере
        return render_template('index.html',
                               title='О сайте!',
                               menu=SITEMENU,
                               visits=session['visits'], data=session['data'])

    return render_template('personal/index.html',
                           title='Ваша персональная страница',
                           menu=SITEMENU)
