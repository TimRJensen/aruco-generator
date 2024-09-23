import cv2, cv2.aruco as aruco # type: ignore
import os
from datetime import datetime as dt
from flask import Blueprint, render_template, request, send_file
from threading import Timer

# Order matters
aruco_dicts = [
    (aruco.getPredefinedDictionary(aruco.DICT_4X4_1000), 1000, "4x4 (50, 100, 250, 1000)"),
    (aruco.getPredefinedDictionary(aruco.DICT_5X5_1000), 1000, "5x5 (50, 100, 250, 1000)"),
    (aruco.getPredefinedDictionary(aruco.DICT_6X6_1000), 1000, "6x6 (50, 100, 250, 1000)"),
    (aruco.getPredefinedDictionary(aruco.DICT_7X7_1000), 1000, "7x7 (50, 100, 250, 1000)"),
    (aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_16h5), 30, "AprilTag 16h5 (30)"),
    (aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_25h9), 35, "AprilTag 25h9 (35)"),
    (aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_36h10), 2320, "AprilTag 36h10 (2320)"),
    (aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_36h11), 587, "AprilTag 36h11 (587)"),
]

def clean_temp(path):
    try:
        os.remove(path)
    except Exception:
        print("[ERR] Failed to delete \"{0}\"".format(path))

Index = Blueprint("index", __name__, url_prefix="/")

@Index.get("/")
def index():
    return render_template("index.html", aruco_dicts=[x[2] for x in aruco_dicts])

@Index.get("/q")
def q():
    n = request.args.get("dict", type=int)
    id = request.args.get("id", type=int)
    size = request.args.get("size", type=int)

    if id >= aruco_dicts[n][1]:
        return send_file("static/img/404.png", mimetype="image/png")
    
    path = os.path.abspath("temp/marker-{0}_{1}.png".format(
        id, 
        dt.now().strftime("%d-%m-%yT%H-%M-%S"))
    )
    cv2.imwrite(path, aruco.drawMarker(aruco_dicts[n][0], id, size))
    Timer(5, clean_temp, args=[path]).start()
    return send_file(path, mimetype="image/png")
