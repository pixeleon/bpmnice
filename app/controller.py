import io
import os
import pandas
from dataclasses import asdict

from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

import analyzer
import repository

DATA_EXPORT_FILENAME = 'analysis_results'
CSV_FILE_EXTENSION = '.csv'
XLSX_FILE_EXTENSION = '.xlsx'
CSV_MIMETYPE = 'text/csv'
XLS_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_APP_SECRET_KEY')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


def create_results_data_frame(results):
    return pandas.DataFrame(
        [(x.id, x.filename, x.total_tasks, x.invalid_tasks, x.score, x.created_time) for x in results],
        columns=['ID', 'Filename', 'Total tasks', 'Invalid tasks', 'Model score', 'Created at']
    )


@login_manager.user_loader
def load_user(user_id):
    return repository.get_app_user_by_id(int(user_id))


@app.route("/")
@login_required
def hello():
    results = repository.get_all_results(current_user.id)
    return render_template('home.html', results=results, user_name=current_user.name)


@app.route("/api/history")
def get_history():
    db_results = repository.get_all_results(current_user.id)
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
        user_id = current_user.id
        print('Valid file submitted: ', filename)
        return jsonify(analyzer.analyze_file(file, user_id))


@app.route('/download/<int:analysis_id>', methods=['GET'])
def download_analysis_file(analysis_id):
    file = repository.get_analysis_file(analysis_id)
    if file:
        return send_file(
            io.BytesIO(file.data),
            download_name=file.name,
            as_attachment=True
        )
    else:
        return jsonify({'error': 'Analysed file not found'})


@app.route('/export_csv', methods=['GET'])
def export_csv():
    data = repository.get_all_results(current_user.id)
    data_frame = create_results_data_frame(data)
    export_file = io.BytesIO()
    data_frame.to_csv(export_file, index=False, encoding='utf-8')
    export_file.seek(0)
    return send_file(
        export_file,
        as_attachment=True,
        mimetype=CSV_MIMETYPE,
        download_name=DATA_EXPORT_FILENAME + CSV_FILE_EXTENSION
    )


@app.route('/export_xls', methods=['GET'])
def export_data():
    data = repository.get_all_results(current_user.id)
    data_frame = create_results_data_frame(data)
    export_file = io.BytesIO()
    with pandas.ExcelWriter(export_file, engine='openpyxl') as writer:
        column_widths = {'A': 4, 'B': 40, 'C': 15, 'D': 15, 'E': 15, 'F': 16}
        data_frame.to_excel(writer, index=False, sheet_name='History')
        worksheet = writer.sheets['History']
        for column, width in column_widths.items():
            worksheet.column_dimensions[column].width = width
    export_file.seek(0)
    return send_file(
        export_file,
        as_attachment=True,
        mimetype=XLS_MIMETYPE,
        download_name=DATA_EXPORT_FILENAME + XLSX_FILE_EXTENSION
    )


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def post_signup():
    name = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    is_user_created = repository.save_app_user(name, email, password)

    if is_user_created:
        user = repository.get_app_user_by_credentials(email, password)
        login_user(user, remember=False)
        return redirect(url_for('hello'))
    else:
        flash('This email address already in use!')
        return redirect(url_for('signup'))


@app.route('/login', methods=['POST'])
def post_login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = repository.get_app_user_by_credentials(email, password)
    if not user:
        flash('Please check your login details and try again!')
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    return redirect(url_for('hello'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    print('Application is running!')
    app.run(host='0.0.0.0', debug=True)
