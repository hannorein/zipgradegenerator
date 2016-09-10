import os
import html
import subprocess
from flask import Flask, request 
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime
import uuid
import math

class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

UPLOAD_FOLDER = "/home/rein/git/zipgradegenerator/uploads"
TEST_UPLOAD_FOLDER = "/home/rein/git/zipgradegenerator/test_uploads"
ALLOWED_EXTENSIONS = set(['py','py3'])
app = FlaskApp(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEST_UPLOAD_FOLDER'] = TEST_UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    deadline = datetime.strptime("2016-09-23 17:00:00 EST", "%Y-%m-%d %H:%M:%S %Z")
    time_difference = deadline-datetime.now() 
    tm = int(math.floor(time_difference.total_seconds() / 60.))
    days = int(math.floor(tm/60./24.))
    hours = int(math.floor(tm/60.-days*24.))
    minutes = int(math.floor(tm-days*24.*60.-hours*60.))
    if time_difference.total_seconds()<0:
        return '''
        <!doctype html>
        <title>No success</title>
        <h1>Deadline passed. </h1>
        '''


    if request.method == 'POST':
        if 'test' not in request.form:
            return '''
            <!doctype html>
            <title>No success</title>
            <h1>Something went wrong. Please try again.</h1>
            '''
        if request.form["test"]=="0":
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
                <h1>Student id invalid. Enter all 10 digits. If your student id has only 9 digits, add a 0 at the beginning. Please try again.</h1>
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
        else:
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
                    filename = str(uuid.uuid4())+".py"
                    file.save(os.path.join(app.config['TEST_UPLOAD_FOLDER'], filename))
                    p = subprocess.Popen(["./run_docker.bash", filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd="/home/rein/git/zipgradegenerator/")
                    out = html.escape(p.communicate()[0].decode("ascii"))
                    return '''
                    <!doctype html>
                    <title>Test result:</title>
                    <h1>Test result:</h1>
                    <pre>'''+out+'''</pre>
                    '''
                else:
                    return '''
                    <!doctype html>
                    <title>No success</title>
                    <h1>Please upload a file with a .py extension.</h1>
                    '''
            return '''
            <!doctype html>
            <title>Testing...</title>
            <h1>Running your python program now...</h1>
            '''

    return '''
    <!doctype html>
    <title>Test/upload assignment</title>
    <h1>Test assignment</h1>
    <p>You can run an automated check before submitting your assignment. Note that this test only checks some of the requirements for the assignment. It is not a guarantee that the assignment will be marked as correct.<p>
    <form action="" method=post enctype=multipart/form-data>
      <p>File (should have extension .py): <input type=file name=file></p>
      <p><input type=submit value=Submit></p>
      <input type="hidden" name="test" value="1">
    </form>
    <h1>Upload assignment</h1>
    <p>The deadline for this assignment is in '''+"%d"%days+''' days, '''+"%d"%hours+''' hours, '''+"%d"%minutes+''' minutes. Submissions will not be accepted after the deadline.</p>
    <form action="" method=post enctype=multipart/form-data>
      <p>File (should have extension .py): <input type=file name=file></p>
      <p>First and last name: <input type="text" name="name"></p>
      <p>Student id (10 digits): <input type="text" name="sid"></p>
      <p><input type=submit value=Submit></p>
      <input type="hidden" name="test" value="0">
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True,threaded=True)
