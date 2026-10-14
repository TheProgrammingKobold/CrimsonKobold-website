from flask import Flask 
from flask import render_template

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route("/Blog")
def blog():
    return render_template('Blog.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)