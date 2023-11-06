import io

from dataclasses import asdict

from flask import Flask, render_template, jsonify, request, send_file

import main
import storage

app = Flask(__name__)


@app.route("/")
def hello():
    results = storage.get_all_results()
    return render_template('home.html', results=results)


@app.route("/api/history")
def get_history():
    db_results = storage.get_all_results()
    results = [asdict(result) for result in db_results]
    return jsonify(results)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return jsonify({'error': 'No file part in upload request'})

    file = request.files['fileInput']

    filename = file.filename

    if filename == '':
        return jsonify({'error': 'No selected file in upload request'})

    if not filename.endswith('.bpmn'):
        return jsonify({'error': 'Invalid file extension in upload request'})

    if file:
        print('Valid file submitted: ', filename)
        return jsonify(main.analyze_file(file))


@app.route('/download/<int:analysis_id>', methods=['GET'])
def download_analysis_file(analysis_id):
    file = storage.get_analysis_file(analysis_id)
    if file:
        return send_file(
            io.BytesIO(file.data),
            download_name=file.name,
            as_attachment=True
        )
    else:
        return jsonify({'error': 'Analysed file not found'})


if __name__ == '__main__':
    print('Application is running!')
    app.run(host='0.0.0.0', debug=True)
