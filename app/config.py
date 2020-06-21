"""Конфигурации для проекта"""
from os import urandom


class Config:
    """Основной общий класс конфигурации"""
    SECRET_KEY = urandom(16)
    CDN_HTTPS = True
    CDN_TIMESTAMP = False
    CDN_DOMAIN = 'cdnjs.cloudflare.com'
    CDN_ENDPOINTS = ['ajax/libs/jquery/3.5.1/jquery.slim.min.js',
                     'ajax/libs/twitter-bootstrap/5.0.0-alpha1/js/bootstrap.min.js',
                     'ajax/libs/twitter-bootstrap/5.0.0-alpha1/css/bootstrap.min.css']


class ProductionConfig(Config):
    """Класс для работы приложения в Production"""
    DEBUG = False
    ASSETS_DEBUG = False
    TESTING = False
    CDN_DEBUG = False
    JSONIFY_PRETTYPRINT_REGULAR = False


class DevelopmentConfig(Config):
    """Класс для работы приложения в разработке"""
    DEBUG = True
    ASSETS_DEBUG = True
    TESTING = False
    CDN_DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR = True
