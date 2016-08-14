import glob
import subprocess
from multiprocessing import Process,Manager
    
def run_student_code(filename,return_dict):
    output = subprocess.Popen(["python3", filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].decode("ascii")
    return_dict["output"] = output

with open('correct_output.txt', 'r') as content_file:
    correct_output = content_file.read()

manager = Manager()
return_dict = manager.dict()
for f in glob.glob("submissions/*.py"):
    iscorrect = 1
    sid = f.split("/")[1].split(" ")[0]
    p = Process(target=run_student_code,args=(f,return_dict))
    p.start()
    p.join(1)
    if p.is_alive():
        p.terminate()
        iscorrect = 0
    if return_dict["output"]!=correct_output:
        iscorrect = 0
    if iscorrect:
        print(sid, "correct")
    else:
        print(sid, "not correct")

