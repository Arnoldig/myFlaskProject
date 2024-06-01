from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from personal.personal import personal


app = Flask(__name__)
app.register_blueprint(personal, url_prefix='/personal')
app.config['SECRET_KEY'] = 'f94753a248dce5c430c61430bb034c09d5cc7cb1'
app.permanent_session_lifetime = timedelta(days=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from controller import app

if __name__ == '__main__':
    app.run(debug=True)
