data_folder = '/home/cul226/data/cochrane/'
pickle_folder = data_folder + 'pickles/'

d2idx = {'allocation concealment': 0,
         'random sequence generation': 1,
         'incomplete outcome data': 2,
         'selective reporting': 3,
         'blinding of participants and personnel': 4,
         'blinding of outcome assessment': 5}


def get_all_pmids():
    '''
    Get all Pubmed ID in our collected CDSR dataset
    '''
    import cPickle as pickle
    pmids = set()
    ref2pmid = pickle.load(open(pickle_folder + 'ref2pmid.pickle', 'rb'))
    for doi in ref2pmid:
        for ref in ref2pmid[doi]:
            for id in ref2pmid[doi][ref]:
                if id != -1:
                    pmids.add(id)
    return pmids


def get_pmid_to_text():
    '''
    This function assumes that 'pdftotext.py' is used to get texts.
    '''
    import cPickle as pickle
    import os
    pmid2pdf = pickle.load(open(pickle_folder + 'pmid_to_pdf.pickle', 'rb'))
    pmid2txt = dict()
    for pmid in pmid2pdf:
        txt = '.'.join(pmid2pdf[pmid].split('.')[:-1]) + '.txt'
        if os.path.isfile(txt):
            pmid2txt[pmid] = txt
    return pmid2txt


def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    print longest_common_substring('abc dsi', 'abc d ')
