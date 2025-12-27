
from flask import Flask, render_template, request, redirect
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        dtype = request.form.get("type")
        quality = request.form.get("quality", "best")

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "noplaylist": True
        }

        if dtype == "mp3":
            ydl_opts["format"] = "bestaudio"
        else:
            ydl_opts["format"] = quality

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Direct URL
            if "url" in info:
                return redirect(info["url"])

            # Fallback
            if "formats" in info and len(info["formats"]) > 0:
                return redirect(info["formats"][-1]["url"])

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
