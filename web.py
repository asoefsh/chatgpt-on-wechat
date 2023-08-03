import json
import subprocess
from flask import Flask, render_template, request, Response, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "allinai0720"  # Replace "your_secret_key" with a secret key for session

# Load the config.json content
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

# Sample username and password (replace with your own credentials)
USERNAME = "65294002@qq.com"
PASSWORD = "65294002"

def is_authenticated():
    return session.get("authenticated", False)

@app.route("/", methods=["GET", "POST"])
def login():
    if is_authenticated():
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username == USERNAME and password == PASSWORD:
            session["authenticated"] = True
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid username or password. Please try again."

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    session.pop("username", None)
    return redirect(url_for("login"))
    
@app.route("/home")
def home():
    if not is_authenticated():
        return redirect(url_for("login"))

    return render_template("index.html", username=session.get("username", ""))


@app.route("/config", methods=["GET", "POST"])
def index():
    if not is_authenticated():
        return redirect(url_for("login"))


    if request.method == "POST":
        config_data["allinai_model_id"] = request.form.get("allinai_model_id")
        config_data["ad_message"] = request.form.get("ad_message")
        config_data["single_chat_prefix"] = [prefix.strip() for prefix in request.form.get("single_chat_prefix").split(",")]
        config_data["single_chat_reply_prefix"] = request.form.get("single_chat_reply_prefix")
        config_data["group_chat_prefix"] = [prefix.strip() for prefix in request.form.get("group_chat_prefix").split(",")]
        config_data["group_name_white_list"] = [group.strip() for group in request.form.get("group_name_white_list").split(",")]
        config_data["group_chat_in_one_session"] = [group.strip() for group in request.form.get("group_chat_in_one_session").split(",")]
        config_data["max_daily_replies"] = int(request.form.get("max_daily_replies"))
        config_data["max_minute_replies"] = int(request.form.get("max_minute_replies"))
        config_data["add_friend_msg"] = request.form.get("add_friend_msg")
        # Add other form fields for other environment variables

        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file, indent=4, ensure_ascii=False)
        # Return a JSON response indicating success
        return jsonify({"message": "保存成功!\n注:保存后需要去【扫码/管理】页面重启系统，重启后需要重新微信扫码登录即可生效。"})

    return render_template("config.html", config_data=config_data)


@app.route("/log")
def show_log():
    if not is_authenticated():
        return redirect(url_for("login"))

    try:
        with open("nohup.out", "r", encoding="utf-8") as log_file:
            log_content = log_file.read()
        return render_template("log.html", log_content=log_content)
    except FileNotFoundError:
        return "No log file found."

@app.route("/admin")
def show_admin_log():
    if not is_authenticated():
        return redirect(url_for("login"))

    try:
        with open("nohup.out", "r", encoding="utf-8") as log_file:
            log_content = log_file.read()
        return render_template("log2.html", log_content=log_content)
    except FileNotFoundError:
        return "No log file found."

@app.route("/execute_script", methods=["POST"])
def execute_script():
    if not is_authenticated():
        return redirect(url_for("login"))

    script_name = request.json.get("script")
    if not script_name:
        return "No script name provided.", 400

    if script_name == "start":
        script_path = "scripts/start.sh"
    elif script_name == "shutdown":
        script_path = "scripts/shutdown.sh"
    else:
        return f"Invalid script: {script_name}", 400

    try:
        subprocess.run(["sh", script_path], check=True)
        return f"您已成功关闭数字分身系统!"
    except subprocess.CalledProcessError as e:
        # return f"Error executing {script_name}.sh: {e}", 500
        return f"数字分身系统已处于关闭状态，无法再次关闭。", 500

@app.route("/restart_script", methods=["POST"])
def restart_script():
    if not is_authenticated():
        return redirect(url_for("login"))

    script_name = request.json.get("script")
    if not script_name:
        return "No script name provided.", 400

    if script_name == "start":
        script_path = "scripts/start.sh"
    elif script_name == "shutdown":
        script_path = "scripts/shutdown.sh"
    else:
        return f"Invalid script: {script_name}", 400

    try:
        subprocess.run(["sh", script_path], check=True)
        return f"您已成功重启数字分身系统！5秒钟后点击刷新按钮即可扫码登陆。"
    except subprocess.CalledProcessError as e:
        # return f"Error executing {script_name}.sh: {e}", 500
        return f"您已成功重启数字分身系统！5秒钟后点击刷新按钮即可扫码登陆。", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=23456)