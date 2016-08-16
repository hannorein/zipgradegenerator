import os
from flask import Flask, flash, abort, render_template, send_from_directory, request, redirect, Response, make_response, url_for
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
import math

class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

UPLOAD_FOLDER = "/home/rein/git/zipgradegenerator/uploads"
ALLOWED_EXTENSIONS = set(['py','py3'])
app = FlaskApp(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    deadline = datetime.strptime("2016-09-09 17:00:00 EST", "%Y-%m-%d %H:%M:%S %Z")
    time_difference = deadline-datetime.now() 
    minutes = int(math.floor(time_difference.total_seconds() / 60.))
    if minutes<0:
        return '''
        <!doctype html>
        <title>No success</title>
        <h1>Deadline passed. </h1>
        '''


    if request.method == 'POST':
        print(request)
        # Student id
        if 'sid' not in request.form:
            return '''
            <!doctype html>
            <title>No success</title>
            <h1>Student id invalid. Please try again.</h1>
            '''
        sid = request.form['sid']
        try:
            sidi = int(sid)
        except:
            return '''
            <!doctype html>
            <title>No success</title>
            <h1>Student id invalid. Should be 10 digits. Please try again.</h1>
            '''
        if len(sid) != 10: 
            return '''
            <!doctype html>
            <title>No success</title>
            <h1>Student id invalid. Enter all 10 digits. Please try again.</h1>
            '''
        if not sid.isdigit(): 
            return '''
            <!doctype html>
            <title>No success</title>
            <h1>Student id invalid. Please try again.</h1>
            '''
        # Name
        if 'name' not in request.form:
            return '''
            <!doctype html>
            <title>No success</title>
            <h1>Name invalid. Please try again.</h1>
            '''
        name = request.form['name']
        if len(name) <6: 
            return '''
            <!doctype html>
            <title>No success</title>
            <h1>Name invalid. Please try again.</h1>
            '''
        # File
        file = request.files['file']
        if file.filename == '':
            return '''
            <!doctype html>
            <title>No success</title>
            <h1>No file submitted. Please try again.</h1>
            '''
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(sid+"_"+name+"_"+file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return '''
                <!doctype html>
                <title>Success</title>
                <h1>Upload was successful. Thank you.</h1>
                '''
            else:
                return '''
                <!doctype html>
                <title>No success</title>
                <h1>Please upload a file with a .py extension.</h1>
                '''

    return '''
    <!doctype html>
    <title>Upload assignment</title>
    <h1>Upload assignment 1</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p>File (should have extension .py): <input type=file name=file></p>
      <p>First and last name: <input type="text" name="name"></p>
      <p>Student id (10 digits): <input type="text" name="sid"></p>
      <p><input type=submit value=Submit></p>
      <p>The deadline for this assignment is in '''+"%d"%minutes+''' minutes. Submissions will not be accepted after the deadline.</p>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True,threaded=True)
