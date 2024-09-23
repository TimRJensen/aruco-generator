from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.index import Index, aruco_dicts
    app.register_blueprint(Index)
    
    return app
