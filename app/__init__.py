from flask import Flask
from app.models import db
from app.extensions import ma
from app.blueprints.users import users_bp
from app.blueprints.transactions import transactions_bp
from app.blueprints.listings import listings_bp
from app.blueprints.skills import skills_bp


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")


    db.init_app(app)
    ma.init_app(app)



    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
    app.register_blueprint(listings_bp, url_prefix="/listings")
    app.register_blueprint(skills_bp, url_prefix="/skills")
 

    return app