from flask import Flask
from app.routes import routes
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes) 

    # Start scheduler only if not already running
    if not scheduler.running:
        scheduler.start()

    return app
