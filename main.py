__author__ = 'mirusso'
import logging
import os

from config import is_deployed
from app import create_app


# if we are deployed to google app engine, then we should use 'production'
if is_deployed:
    flask_config = 'production'
else:
    flask_config = os.getenv('FLASK_CONFIG') or 'default'


logging.info('main.py loaded with {} config.'.format(flask_config))

app = create_app(config_name=flask_config)
