from flask import Blueprint, jsonify

api = Blueprint('api', __name__)


@api.route("/api/latest")
def index():
    return jsonify({
        "windows": {
            "version": "1.0.6.25",
            "url": "http://server.com/app.exe",
        },
        "windows-test": {
            "version": "2.0",
            "url": "http://server.com/devapp.exe",
        },
        "android": {
            "url": "https://play.google.com/store/apps/details?id=app"
        },
    })