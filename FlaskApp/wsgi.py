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
        parser.clear()

        filename = UPLOAD_FOLDER + '/' + filename

        html = parser.get_html(filename)


        #return render_template('result.html', html=html)
        return html

    if request.method == 'POST':
        # for key in request.form:
        #     print key, request.form[key]

        result = parser.put_results(request.form)

        return result





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
