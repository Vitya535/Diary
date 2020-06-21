"""Класс для обработки ошибок в приложении"""

from flask import render_template
from htmlmin import minify

from app import APP


@APP.errorhandler(404)
def not_found_error(error) -> tuple:
    """Класс для обработки ошибки 404 (Not Found)"""
    return minify(render_template('errors/error_404.html', title='404 Not Found')), 404


@APP.errorhandler(500)
def internal_server_error(error) -> tuple:
    """Класс для обработки ошибки 500 (Internal Server Error)"""
    return minify(render_template('errors/error_500.html', title='500 Internal Error')), 500
