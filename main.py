from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
from pathlib import Path
import os
import random

app = Flask(__name__)
app.secret_key = "somethingyoumayguesshoweveritisnotimportant"
FILES_DIR = Path(__name__).parent / "files"
PORT = random.randint(10000, 60000)


def get_filename_list():
    return os.listdir(FILES_DIR)


@app.route("/")
def main():
    kwards = {
        "file_list": get_filename_list()
    }
    return render_template("index.html", **kwards)


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        upload_file = request.files["file"]
        upload_file.save(FILES_DIR / upload_file.filename)
        return redirect(url_for("main"))


@app.route("/download/<filename>")
def download(filename):
    if os.path.exists(FILES_DIR / filename):
        return send_from_directory(FILES_DIR, filename, as_attachment=True)
    else:
        return "File doesn't exist."


@app.route("/delete/<filename>")
def delete(filename):
    if os.path.exists(FILES_DIR / filename):
        os.remove(FILES_DIR / filename)
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
