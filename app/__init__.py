import os
import cv2, cv2.aruco as aruco # type: ignore
from threading import Timer
from time import sleep
from flask import Flask, request, send_file
from datetime import datetime as dt

def create_app():
    app = Flask(__name__)

    from app.routes.index import Index, aruco_dicts
    app.register_blueprint(Index)
    
    return app
