# models\usuario.py

from flask import request, url_for
import requests
from sql_alchemy import banco

MAILGUN_DOMAIN = 'MEU_DOMINIO.ORG'
MAILGUN_API_KEY = 'MINHA_CHAVE_API'
FROM_TITLE = 'TITULO_EMAIL'
FROM_EMAIL = 'EMAIL'

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, email, senha, ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado
    
    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return requests.post('https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages', 
                    auth =('api', MAILGUN_API_KEY),
                    data={'from': '{FROM_TITLE} <{FROM_EMAIL}>',
                          'to': self.email,
                          'subject': 'Confirmação de Cadastro',
                          'text': 'Confirme seu cadastro clicando no link a seguir: {link}',
                          'html': '<html><p>\
                          Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR EMAIL</a>\
                          </p></html>'
                          })
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
            }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()