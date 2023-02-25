from flask import Flask, render_template
import methods
import helpers

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def main(name=None):
    return render_template("main.html", name=name)

@app.route("/api/yt/<query>", methods=["POST"])
def yt_call(query: str):
    tags = methods.request_youtube(query)
    return ", \n".join(helpers.top_tags(tags))