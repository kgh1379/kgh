import os
import sys
import glob
import csv

def process_batch(batch_dirs, csv_writer):
    for dirname in batch_dirs:
        if not os.path.isdir(dirname):
            continue
        # Assuming get_studyinfo is modified to return a list of tuples
        study_infos = get_studyinfo(dirname)
        for study_info in study_infos:
            csv_writer.writerow(study_info + (dirname,))

def main(basepath, csvpath):
    all_dirs = glob.glob(os.path.join(basepath, '*'))
    batch_size = 50  # Adjust based on testing and system capability

    with open(csvpath, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['StudyID', 'PatientID', 'PatientName', 'StudyDate', 'Directory Path'])

        for i in range(0, len(all_dirs), batch_size):
            batch_dirs = all_dirs[i:i+batch_size]
            process_batch(batch_dirs, csv_writer)
            print(f"Processed batch {i//batch_size + 1}/{(len(all_dirs) + batch_size - 1)//batch_size}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} [external hard disk location] [CSV file name to be output]")
        sys.exit(1)

    basepath = os.path.abspath(sys.argv[1])
    csvpath = sys.argv[2]
    main(basepath, csvpath)