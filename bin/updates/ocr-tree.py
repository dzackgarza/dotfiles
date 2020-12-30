#!/usr/bin/env python3
# Walk through directory tree, replacing all files with OCR'd version
# Contributed by DeliciousPickle@github

import logging
import os
import subprocess
import sys
import hashlib
import pickle


script_dir = os.path.dirname(os.path.realpath(__file__))
print(script_dir + '/ocr-tree.py: Start')

if len(sys.argv) > 1:
    start_dir = sys.argv[1]
else:
    start_dir = '.'

if len(sys.argv) > 2:
    log_file = sys.argv[2]
else:
    log_file = script_dir + '/ocr-tree.log'

db_location = '/home/zack/dotfiles/pdf_hash.db'
#hashList = set()
with open(db_location, 'rb') as filehandle:
    hashList= pickle.load(filehandle)

logging.basicConfig(
                level=logging.INFO, format='%(asctime)s %(message)s',
                filename=log_file, filemode='w')

print("Walking directory tree..")
for dir_name, subdirs, file_list in os.walk(start_dir):
    logging.info('\n')
    logging.info(dir_name + '\n')
    os.chdir(dir_name)
    for filename in file_list:
        file_ext = os.path.splitext(filename)[1]
        if file_ext == '.pdf':
            full_path = dir_name + '/' + filename
            #filehash = hashlib.md5(open(full_path,'rb').read()).hexdigest()
            filehash = filename
            print(f"Hashing file {filename}")
            if filehash in hashList:
                print(f"File already hashed: {filename}")
                continue
            print(full_path)
            cmd = ["ocrmypdf",  "--clean", "--skip-text", filename, filename]
            logging.info(cmd)
            print("Running ocrmypdf...")
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = proc.stdout.read()
            if proc.returncode == 6:
                print(f"Already OCR'd: {filename}")
            elif proc.returncode == 0:
                print("OCR complete")
                print(f"Success: {filename}")
            else:
                print(f"Unknown error, file: {filename}")
            hashList.add(filehash)
            with open(db_location, 'wb') as filehandle:
                pickle.dump(hashList, filehandle)
            logging.info(result)
            print("---------------------------------------")
