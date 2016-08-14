import glob
from pdfrw import PdfReader, PdfWriter, PageMerge
import subprocess
from shutil import copyfile
from generatezip import  getzipwithstudentid

for f in glob.glob("submissions/*.py"):
    print(f)
    sid = f.split("/")[1].split(" ")[0]
    fm = "submissions_with_bugs/"+f.split("/")[1]
    copyfile(fm,"tmp.py")
    subprocess.Popen(["/Library/TeX/texbin/pdflatex", "source.tex"], stdout=subprocess.PIPE).communicate()[0]
    getzipwithstudentid("zipwithid.pdf",sid)

    writer = PdfWriter()
    writer.addpages(PdfReader("source.pdf").pages)
    writer.addpages(PdfReader("zipwithid.pdf").pages)
    writer.write("printouts/quiz_"+sid+".pdf")

