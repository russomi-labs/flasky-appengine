__author__ = 'mirusso'
import logging

import os
from app import create_app


config = os.getenv('FLASK_CONFIG') or 'default'

logging.info('main.py loaded with {} config.'.format(config))

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
