from main import db, app
from datetime import datetime
from werkzeug.security import generate_password_hash


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True)
    msg = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.id}>'

    def write_data_to_db(self, name: str, email: str, msg: str) -> None:

        try:
            m = Message(name=name, email=email, msg=msg)
            db.session.add(m)
            db.session.commit()
        except Exception as e:
            print('Ошибка класса Message: данные не добавлены в БД')
            print(f'Описание ошибки: {e}')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.id}>'

    def write_data_to_db(self, password: str, email: str) -> int:
        try:
            hash_ = generate_password_hash(password)
            u = User(email=email, psw=hash_)
            db.session.add(u)
            db.session.commit()
            return u.id
        except Exception as e:
            print('Ошибка класса User: данные не добавлены в БД')
            print(f'Описание ошибки: {e}')


class WriteError(Exception):
    pass


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Profiles {self.id}>'

    def write_data_to_db(self, name: str, old: str,
                         city: str, user_id: int) -> None:

        try:
            if user_id is None:
                raise WriteError("Нет id из таблицы User")
            p = Profiles(name=name, old=old, city=city, user_id=user_id)
            db.session.add(p)
            db.session.commit()
        except WriteError:
            print(("Нет id из таблицы User"))
        except Exception as e:
            print('Ошибка класса Profiles: данные не добавлены в БД')
            print(f'Описание ошибки: {e}')


with app.app_context():
    db.create_all()