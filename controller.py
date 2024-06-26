from flask import (render_template, request, make_response, session, redirect,
                   url_for, flash)
from main import app
from model import User, Profiles, Message, check_login
from const import SITEMENU


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # реализовать проверку данных

        # новая реализация записи данных в БД
        u = User()
        u_id = u.write_data_to_db(email=request.form['email'],
                                  password=request.form['password'])
        p = Profiles()
        p.write_data_to_db(name=request.form['name'],
                           old=request.form['old'],
                           city=request.form['city'],
                           user_id=u_id)

    return render_template('registration.html',
                           title='Регистрация новых пользователей',
                           menu=SITEMENU)


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    if 'userLogged' in session:
        return redirect(url_for('app_pers.personal_site'))

    if request.method != 'POST':
        return render_template('authorization.html',
                               title='Авторизация пользователей',
                               menu=SITEMENU)

    if check_login(request.form['email'], request.form['password']):
        session.permanent = True  # указываем браузеру что сессию сохраняем
        session['userLogged'] = request.form['email']  # запись в куки
        return redirect(url_for('app_pers.personal_site'))
    else:
        flash({
            'title': "Неверный логин или пароль",
            'message': "Попробуйте ещё раз ввести логин и пароль"},
            'error')

    return render_template('authorization.html',
                           title='Авторизация пользователей',
                           menu=SITEMENU)


@app.route('/index')
@app.route('/')
def index():
    session.permanent = True  # указываем браузеру что сессию сохраняем
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1

    if 'data' in session:
        session['data'][1] += 1
        session.modified = True  # работает и без этой строчки ...
    else:
        session['data'] = [1, 2, 3, 4]

    return render_template('index.html',
                           title='О сайте!',
                           menu=SITEMENU,
                           visits=session['visits'], data=session['data'])


@app.route('/about')
def about():
    content = render_template('about.html',
                              title='О нас!',
                              menu=SITEMENU)
    res = make_response(content, 200)
    res.headers['Content-Type'] = 'text/html'
    res.headers['Server'] = 'flask'
    return res


@app.errorhandler(404)
def page_not_found(error):
    log = '-'
    if request.cookies.get('logged_key'):
        log = request.cookies.get('logged_key')

    text = f'<p>logged_key: {log} </p>'
    content = render_template('404.html',
                              title='Страницы не существует!',
                              menu=SITEMENU,
                              cookie=text)

    res = make_response(content, 404)
    res.set_cookie('logged_key', 'yes', max_age=1 * 24 * 60 * 60)
    return res


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # реализовать проверку данных

        # реализация записи данных в БД
        m = Message()
        m.write_data_to_db(email=request.form['email'],
                           name=request.form['name'],
                           msg=request.form['message'])

    return render_template('contact.html',
                           title='Обратная связь', menu=SITEMENU)
