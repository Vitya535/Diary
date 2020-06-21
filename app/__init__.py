"""Инициализация всех частей приложения"""
from locale import LC_ALL
from locale import setlocale

from flask import Flask
from flask_cdn import CDN
from flask_compress import Compress

from app.assets import ASSETS
from app.security import CSP
from app.security import TALISMAN

APP = Flask(__name__)
APP.config.from_object(f'app.config.{APP.config["ENV"]}Config')
setlocale(LC_ALL, '')

ASSETS.init_app(APP)

CDN = CDN(APP)
COMPRESS = Compress(APP)
TALISMAN.init_app(APP, content_security_policy=CSP, force_https=False)

from app.views import *
from app.errors import *
