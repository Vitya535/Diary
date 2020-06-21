"""Инициализация security, необходимого для приложения"""
from flask_talisman import Talisman

CSP = {
    'default-src': '\'self\'',
    'script-src': ['\'self\'', 'https://cdnjs.cloudflare.com'],
    'object-src': ['\'self\'', 'unsafe-eval'],
    'style-src': ['\'self\'', '\'unsafe-inline\'', 'https://cdnjs.cloudflare.com'],
    'img-src': ['\'self\'', 'data: *'],
    'media-src': '\'none\'',
    'frame-src': '\'self\'',
    'font-src': ['\'self\'', 'https://cdnjs.cloudflare.com'],
    'connect-src': '\'self\''
}

TALISMAN = Talisman()
