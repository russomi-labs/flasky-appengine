__author__ = 'mirusso'
import logging

import os
from app import create_app


flask_config = os.getenv('FLASK_CONFIG') or 'default'

logging.info('main.py loaded with {} config.'.format(flask_config))

app = create_app(config_name=flask_config)
