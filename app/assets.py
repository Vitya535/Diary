"""Генерация и минификация CSS и JS файлов"""
from flask_assets import Bundle
from flask_assets import Environment

BUNDLES = {
    'calendar_css': Bundle(
        'css/CalendarStyle.css',
        output='gen/main.css',
        filters='cssmin'
    ),
    'scripts_js': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js',
        'js/scripts.js',
        '../templates/scripts_with_jinja2.js',
        output='../templates/main.js',
        filters='jsmin'
    ),
    'errors_css': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/5.0.0-alpha1/css/bootstrap.min.css',
        'css/errors.css',
        output='gen/css/errors.css',
        filters='cssmin'
    ),
    'errors_js': Bundle(
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.slim.min.js',
        'js/errors.js',
        output='gen/js/errors.js',
        filters='jsmin'
    )
}

ASSETS = Environment()
ASSETS.register(BUNDLES)
