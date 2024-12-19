
from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        ip = request.form.get("ip", "").strip()
        forbidden_chars = [';', '&', '|', '`', '$', '>', '<']
        if any(char in ip for char in forbidden_chars):
            result = "Недопустимый ввод!"
        else:
            result = os.popen(f"ping -c 1 {ip}").read()
        if "cat" in ip:
            result = "Недопустимый ввод. Попробуйте другой IP-адрес."

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
