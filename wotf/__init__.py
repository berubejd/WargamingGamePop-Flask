import os
from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy


# Globally accessible libraries
db = SQLAlchemy()
scheduler = APScheduler()


def create_app(test_config=None):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        app.config.from_object("config.Config")

    else:
        app.config.from_object("config.TestingConfig")

    # Initialize Plugins
    db.init_app(app)
    scheduler.init_app(app)

    # Start the scheduler
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        scheduler.start()

    # Register Blueprints
    from . import routes

    app.register_blueprint(routes.main_bp)
    app.add_url_rule("/", endpoint="index")

    with app.app_context():
        # Setup the database
        from .models import Population_Data

        db.create_all()

        # Schedule tasks
        from . import tasks

    return app
