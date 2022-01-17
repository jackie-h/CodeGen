import json
import glob
import os
import gzip

#Utility to create a file in the format expected by Transcoder

file_name = "slang.000.json"
fh = open(file_name, "w")
#fh = gzip.open("slang.000.json.gz", "wb")

path = ''
for filename in glob.glob(os.path.join(path, '*.s')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        contents = f.read()
        fh.write(json.dumps({"repo_name": "test", "ref": "test", "path": filename, "content": contents}))
        fh.write('\n')

fh.close()

with open(file_name, 'rb') as orig_file:
    with gzip.open(file_name + ".gz", 'wb') as zipped_file:
        zipped_file.writelines(orig_file)