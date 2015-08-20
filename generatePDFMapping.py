'''
Create a mapping file (pmid -> file_path) for all pdfs stored
in 'pmc_pdfs' folder
'''
import os
import cPickle as pickle
from utils import data_folder, pickle_folder

id2path = dict()
for root, dirs, files in os.walk(data_folder + 'pmc_pdfs/'):
    for f in files:
        pmid = f.split('.')[0]
        ext = f.split('.')[1]
        if ext != 'pdf':
            continue
        path = root + '/' + f
        id2path[pmid] = path
pickle.dump(id2path, open(pickle_folder + 'pmid_to_pdf.pickle', 'wb'))
