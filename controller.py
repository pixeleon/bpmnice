from flask import Flask, render_template, jsonify

import main

app = Flask(__name__)


@app.route("/")
def hello():
    results = main.load_results()
    return render_template('home.html', results=results)


@app.route("/api/history")
def get_history():
    results = main.load_results()
    return jsonify(results)


if __name__ == '__main__':
    print('Application is running!')
    app.run(host='0.0.0.0', debug=True)
