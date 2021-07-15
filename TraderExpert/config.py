import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('STR_CONN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    URL_HISTORICO_ACOES = os.environ.get('URL_HISTORICO_ACOES')
    KEY_API = os.environ.get('KEY_API')
