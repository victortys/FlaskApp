# third-party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from celery import Celery
from flask_migrate import Migrate

# local imports
from config import app_config, Config

# Database initialisation
db = SQLAlchemy()

# Flask-Mail initialisation
mail = Mail()

# Bootstrap initialisation
bootstrap = Bootstrap()

# # Celery initialisation
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    bootstrap.init_app(app)
    mail.init_app(app)
    celery.conf.update(app.config)

    migrate = Migrate(app, db)

    with app.app_context():
        db.init_app(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .events import events as events_blueprint
    app.register_blueprint(events_blueprint)

    from .recipients import recipients as recipients_blueprint
    app.register_blueprint(recipients_blueprint)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404
    return app
