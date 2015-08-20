import csv
from ftplib import FTP
import os
from utils import get_all_pmids

'''
Download PDFs from Pubmed Central Open Access Subset.

For more info:
http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/

For those pdfs which are not covered in this subset,
we manually download them from PMC.
'''


def get_remote_file_path(ftp_file_mapping):
    pmid2path = dict()
    with open(ftp_file_mapping, 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            pmid = row['PMID']
            if len(pmid) == 0:
                continue
            pmid2path[pmid] = row['File']
    return pmid2path


def download(ftp, ftp_path, local_path):
    if os.path.isfile(local_path):
        print 'already exists', local_path
    else:
        with open(local_path, 'wb') as f:
            print "writing file to %s" % local_path
            ftp.retrbinary("RETR " + ftp_path, f.write)

if __name__ == '__main__':
    data_folder = '/home/lc/cochrane/'
    pdf_output_path = data_folder + 'pmc_pdfs/open_access_pdfs/'
    ftp_file_mapping = data_folder + 'file_list.pdf.csv'

    pmids = get_all_pmids()
    lookup = get_remote_file_path(ftp_file_mapping)
    ftp = FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login()

    found = 0
    notfound = 0
    id2pdf = dict()
    for pmid in pmids:
        if pmid in lookup:
            print 'Downloading pmid:{}'.format(pmid)
            ftp_path = 'pub/pmc/' + lookup[pmid]
            local_path = pdf_output_path + pmid + '.pdf'
            download(ftp, ftp_path, local_path)
            id2pdf[pmid] = local_path
            found += 1
        else:
            notfound += 1
    print "done! %d pdfs not found; %d found" % (notfound, found)
