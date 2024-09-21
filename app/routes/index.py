from flask import Blueprint, render_template

Index = Blueprint("index", __name__, url_prefix="/")

@Index.get("/")
def index():
    return render_template("index.html")
