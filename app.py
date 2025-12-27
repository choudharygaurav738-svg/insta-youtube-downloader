from flask import Flask, render_template, request, redirect
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format": "best"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # video direct URL
            if "url" in info:
                return redirect(info["url"])

            # fallback (multiple formats case)
            if "formats" in info and len(info["formats"]) > 0:
                return redirect(info["formats"][-1]["url"])

    return render_template("index.html")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
