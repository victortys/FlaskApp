import os

from app import celery, create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
app.app_context().push()