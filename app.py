import random
import googleloc

from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)

messages = ['']
ALLOWED_EXTENSIONS = {'txt', 'csv', 'json'}


def allowed_file(filename):
    # Проверка имени файла на нужный тип расширения
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def main_page():
    data = [str(i) for i in range(10)]
    fn, ln = '<имя>', '<фамилия>'

    if 'name' in request.args:
        fn = request.args['name']
    if 'lastname' in request.args:
        ln = request.args['lastname']

    page = render_template('index.html', name=fn, lastname=ln, data=data,
                           flag=True)
    return page


@app.route('/data/', methods=['GET'])
def data_page():
    return render_template('data.html', messages=messages)


@app.route('/fupload/', methods=['GET'])
def upload_page():
    return render_template('fupload.html')


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    messages.append(text)

    return redirect(url_for('data_page'))


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


@app.route('/motivation/')
def get_motivation_text():
    text = random.choice(['Тi хуй', 'Тi собака', 'Здохни!111'])
    return render_template('motivation.html', motiv_text=text)


if __name__ == '__main__':
    app.run(debug=True)
