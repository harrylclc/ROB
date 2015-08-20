'''
Convert PDF to text using 'pdftotext' utility from Xpdf

Later this should be replaced by better extraction tool which can
get structural information.
'''
import cPickle as pickle
import os
from utils import pickle_folder

if __name__ == '__main__':
    id2path = pickle.load(open(pickle_folder + 'pmid_to_pdf.pickle', 'rb'))
    for k, id in enumerate(id2path):
        if k % 500 == 0:
            print '=' * 80, k
        path = id2path[id]
        try:
            os.system('pdftotext -enc UTF-8 {}'.format(path))
        except:
            print path
