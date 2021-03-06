import os
from werkzeug import security
from flask import Flask, Request, Response, render_template, request, redirect, url_for


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'py'])

application = app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from modules.parser import Parser
parser = Parser()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def first():

    if request.method == 'POST':

        file_func = request.files['file']
        if file_func and allowed_file(file_func.filename):
            filename = file_func.filename
            file_func.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect('/')

        else:
            return redirect('/')

    files = os.listdir('uploads')
    return render_template('first.html', files=files)


@app.route('/result/<filename>', methods=['GET', 'POST'])
def result(filename):

    if request.method == 'GET':
        filename = UPLOAD_FOLDER + '/' + filename
        parser.clear()
        parser.process(filename)
        tags = parser.get_tags()

        return render_template('result.html', html=tags)
        #return html

    if request.method == 'POST':
        # for item in request.form:
        #     print request.form[item]
        refs = []
        for field in parser.fields:
            refs.append('='.join([field, request.form[field]]))

        refs = ' and '.join(refs)

        query_string = 'SELECT * FROM {table} WHERE {refs}'

        result = query_string.format(table=request.form['table'], refs=refs)
        tags = parser.get_tags()
        return render_template('result.html', html=tags, result=result)


from flask import send_from_directory
# Show file content
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route("/files/delete")
@app.route("/files/delete/<file_name>")
def delete_file(file_name=None):
    if file_name:
        print file_name
        os.remove('uploads/' + file_name)

    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run()
