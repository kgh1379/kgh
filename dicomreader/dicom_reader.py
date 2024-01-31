#encoding=utf-8

import os
import sys
import glob

try:
    import dicomsdl as dicom
except ModuleNotFoundError:
    print (">>> dicomsdl을 설치해주세요")
    print (">>> pip install dicomsdl")
    sys.exit()

def get_studyinfo(dirname):
    for root, dnlist, fnlist in os.walk(dirname):
        if dnlist:
            continue

        for fn in fnlist:
            if fn.upper() == 'DIRFILE':
                continue
            fn = os.path.join(root, fn)
            
            df = dicom.open(fn)
            if not df:
                continue
            
            if df.SOPClassUID != '1.2.840.10008.5.1.4.1.1.128':
                continue
            
            PatientID = df.PatientID
            PatientName = df.PatientName
            StudyDate = df.StudyDate
            StudyID = df.StudyID
            
            df.close()
            
            if PatientID and PatientName and StudyDate and StudyID:
                return (StudyID, PatientID, PatientName, StudyDate)
    
    return ("ERROR", "ERROR", "ERROR", "ERROR")

if len(sys.argv) < 3:
    print("python %s [외장하드디스크위치] [출력될 CSV 파일이름]"%(sys.argv[0]))
    print("ex) python %s u: studylist.csv"%(sys.argv[0]))
    sys.exit()

basepath = os.path.abspath(sys.argv[1])
csvpath = sys.argv[2]

fout = open(csvpath, 'w')

print ('StudyID,PatientID,PatientName,StudyDate,Directory Path', file=fout)
for dirname in glob.glob(os.path.join(basepath, '*')):
    if not os.path.isdir(dirname):
        continue
    StudyID, PatientID, PatientName, StudyDate = get_studyinfo(dirname)
    print ('%s,%s,%s,%s,%s'%(StudyID, PatientID, PatientName, StudyDate, dirname), file=fout)

fout.close()