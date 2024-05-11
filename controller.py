from werkzeug.security import generate_password_hash
from flask import render_template, request
from main import app
from model import User, Profiles, Message

menu = {'/': 'Главная страница сайта',
        '/about': 'О нас',
        '/contact': 'Обратная связь',
        '/registration': 'Регистрация',
        }


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

        # старая раелазация
        # try:
        #     hash = generate_password_hash(request.form['password'])
        #     u = User(email=request.form['email'], psw=hash)
        #     db.session.add(u)
        #     db.session.flush()
        #
        #     p = Profiles(name=request.form['name'], old=request.form['old'],
        #                  city=request.form['city'], user_id=u.id)
        #     db.session.add(p)
        #     db.session.commit()
        # except:
        #     db.session.rollback()
        #     print('Ошибка добавления данных в базу данных')

    return render_template('registration.html',
                           title='Регистрация новых пользователей',
                           menu=menu)


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', title='О сайте!',
                           menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='О нас!',
                           menu=menu)


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
                           title='Обратная связь', menu=menu)
