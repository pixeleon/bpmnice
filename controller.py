from flask import Flask, render_template, jsonify

app = Flask(__name__)

RESULTS = [
    {
        'id': 1,
        'score': 0.66,
        'filename': 'model1_ex.bpmn',
        'totalTasks': 15,
        'invalidTasks': 5
    },
    {
        'id': 2,
        'score': 0.8,
        'filename': 'model1_ex.bpmn',
        'totalTasks': 15,
        'invalidTasks': 3
    },
    {
        'id': 3,
        'score': 1.0,
        'filename': 'model3.bpmn',
        'totalTasks': 11,
        'invalidTasks': 11
    }
]


@app.route("/")
def hello():
    return render_template('home.html', results=RESULTS)


@app.route("/api/history")
def get_history():
    return jsonify(RESULTS)


if __name__ == '__main__':
    print('Wow!')
    app.run(host='0.0.0.0', debug=True)
