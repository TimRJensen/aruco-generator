import os
import cv2, cv2.aruco as aruco # type: ignore
from threading import Thread, Timer
from time import sleep
from flask import Flask, request, send_file
from datetime import datetime as dt

# Order matters
aruco_dicts = [
    aruco.getPredefinedDictionary(aruco.DICT_4X4_1000),
    aruco.getPredefinedDictionary(aruco.DICT_5X5_1000),
    aruco.getPredefinedDictionary(aruco.DICT_6X6_1000),
    aruco.getPredefinedDictionary(aruco.DICT_7X7_1000),
    aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_16h5),
    aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_25h9),
    aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_36h10),
    aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_36h11),
]

def clean_temp(path):
    try:
        os.remove(path)
    except Exception:
        print("[ERR] Failed to delete \"{0}\"".format(path))

def create_app():
    app = Flask(__name__)

    from app.routes.index import Index
    app.register_blueprint(Index)

    @app.get("/q")
    def q():
        n = request.args.get("dict", type=int)
        id = request.args.get("id", type=int)
        size = request.args.get("size", type=int)
        path = os.path.abspath("temp/marker-{0}_{1}.png".format(
            id, 
            dt.now().strftime("%d-%m-%yT%H-%M-%S"))
        )
        print(size)
        cv2.imwrite(path, aruco.drawMarker(aruco_dicts[n], id, size))
        Timer(5, clean_temp, args=[path]).start()
        return send_file(path, mimetype="image/png", etag=True)
    
    return app
