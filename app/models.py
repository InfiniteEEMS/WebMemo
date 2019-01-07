from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from flask_login import UserMixin
from . import db, login_manager
from exceptions import ValidationError



class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    memos = db.relationship('Memo', backref='owner', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'memo_count': self.memos.count()
        }
        return json_user




class Memo(db.Model):

    __tablename__ = 'memos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime, index=True)
    placename = db.Column(db.Text)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def to_json(self):
        json_memo = {
            'url': url_for('api.get_memo', id=self.id, _external=True),
            'body': self.body,
            'time': self.time,
            'title': self.title,
            'placename': self.placename,
            'lat': self.lat,
            'lng': self.lng,
            'user_url': url_for('api.get_user', id=self.user_id, _external=True),
        }
        return json_memo

    @staticmethod
    def from_json(json_memo):
        body = json_memo.get('body')
        time = json_memo.get('time')
        title = json_memo.get('title')
        if body is None or body == '':
            raise ValidationError('memo does not have a body')
        return Memo(body=body,time=time,title=title)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
