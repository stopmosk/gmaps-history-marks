import random
import googleloc

from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)

messages = ['']
ALLOWED_EXTENSIONS = {'json'}


def allowed_file(filename):
    # Проверка имени файла на нужный тип расширения
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def main_page():
    return render_template('fupload.html')


@app.route('/fupload/', methods=['GET'])
def upload_page():
    return render_template('fupload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'the_file' not in request.files:
            flash('Не указан файл, ататат!')
            return redirect(request.url)
        f = request.files['the_file']

        if f.filename == '':
            flash('Имя файла пустое, азазаз!')
            return redirect(request.url)

        if f and allowed_file(f.filename):
            google_map = googleloc.analyse_map(f)
            return google_map._repr_html_() if google_map != 666 else 'OK 666'
        else:
            flash('ololo')

    return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run(debug=True)
