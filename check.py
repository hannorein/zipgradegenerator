import glob
import subprocess
import csv
from multiprocessing import Process,Manager

def getStudentData(sid):
    with open('PSCB57H3-2016-F-2.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if sid==row[0]:
                return row
    
def runStudentCode(filename,return_dict):
    output = subprocess.Popen(["python3", filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].decode("ascii")
    return_dict["output"] = output

with open('correct_output.txt', 'r') as cf:
    correct_output = cf.read()

manager = Manager()
return_dict = manager.dict()
with open('quiz.csv', 'w') as csvfile:
    for f in glob.glob("submissions/*.py"):
        notcorrect = None
        if "output" in return_dict:
            del return_dict["output"]
        with open(f, 'r') as cf:
            sf = cf.read()
        if "import" in sf:
            notcorrect = "Import statement used"
        sid = f.split("/")[1].split(" ")[0]
        p = Process(target=runStudentCode,args=(f,return_dict))
        p.start()
        p.join(1)
        if p.is_alive():
            p.terminate()
            notcorrect = "Execution time too long"
        if notcorrect is None:
            if return_dict["output"]!=correct_output:
                notcorrect = "Output not correct"
        data = getStudentData(sid)
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        if notcorrect is None:
            ok = "1"
            notcorrect = ""
        else:
            ok = "0"

        row = [sid,ok,notcorrect,data[1],data[11]]
        print(", ".join(row))
        writer.writerow(row)


