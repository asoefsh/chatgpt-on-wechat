import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio = SocketIO(app)
# Load the config.json content
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        config_data["allinai_api_key"] = request.form.get("allinai_api_key")
        config_data["allinai_model_id"] = request.form.get("allinai_model_id")
        config_data["base_url"] = request.form.get("base_url")
        # Add other form fields for other environment variables

        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file, indent=4)
        return "Config saved successfully!"

    return render_template("index.html", config_data=config_data)

@app.route('/scan')
def scan():
    return render_template("scan.html")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=23456)
