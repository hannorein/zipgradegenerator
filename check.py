import glob
import subprocess
from multiprocessing import Process,Manager
    
def run_student_code(filename,return_dict):
    output = subprocess.Popen(["python3", filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].decode("ascii")
    return_dict["output"] = output

with open('correct_output.txt', 'r') as cf:
    correct_output = cf.read()

manager = Manager()
return_dict = manager.dict()
for f in glob.glob("submissions/*.py"):
    notcorrect = None
    with open(f, 'r') as cf:
        sf = cf.read()
    if "import" in sf:
        notcorrect = "Import statement used"
    sid = f.split("/")[1].split(" ")[0]
    p = Process(target=run_student_code,args=(f,return_dict))
    p.start()
    p.join(1)
    if p.is_alive():
        p.terminate()
        notcorrect = "Execution time too long"
    if return_dict["output"]!=correct_output:
        notcorrect = "Output not correct"
    print(sid, ", Not good,", notcorrect)


