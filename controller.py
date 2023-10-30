from flask import Flask, render_template, jsonify, request

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


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return jsonify({'error': 'No file part in upload request'})

    file = request.files['fileInput']

    if file.filename == '':
        return jsonify({'error': 'No selected file in upload request'})

    if not file.filename.endswith('.bpmn'):
        return jsonify({'error': 'Invalid file extension in upload request'})

    if file:
        print('file submitted: ', file.filename)
        return 'file received: ' + file.filename


if __name__ == '__main__':
    print('Application is running!')
    app.run(host='0.0.0.0', debug=True)
