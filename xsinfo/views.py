from xsinfo import app


@app.route('/')
def index():
    return "home"