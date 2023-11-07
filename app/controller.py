import io
from dataclasses import asdict

from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

import analyzer
import storage

app = Flask(__name__)

app.secret_key = 'super-secret-key'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return storage.get_app_user_by_id(int(user_id))


@app.route("/")
@login_required
def hello():
    results = storage.get_all_results()
    return render_template('home.html', results=results, user_name=current_user.name)


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
        return jsonify(analyzer.analyze_file(file))


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
    print('received signup request:', name, email, password)
    is_user_created = storage.save_app_user(name, email, password)
    if is_user_created:
        return redirect(url_for('login'))
    else:
        flash('Email address already exists!')
        return redirect(url_for('signup'))


@app.route('/login', methods=['POST'])
def post_login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    print('received login request:', email, password)

    user = storage.get_app_user_by_credentials(email, password)
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
