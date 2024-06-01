from flask import Blueprint, render_template
from const import SITEMENU

personal = Blueprint('app_pers',
                     __name__,
                     template_folder='templates',
                     static_folder='static')


@personal.route('/')
def personal_site():
    return render_template('personal/index.html',
                           title='Ваша персональная страница',
                           menu=SITEMENU)
