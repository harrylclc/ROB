# -*- coding: utf-8 -*-
'''
Link trials in CDSR to Pubmed
'''
from Bio import Entrez
import cPickle as pickle
from utils import pickle_folder


class PubmedSearcher:

    def __init__(self):
        Entrez.email = 'harryliang910708@gmail.com'

    def search(self, query):
        handle = Entrez.esearch(db='pubmed',
                                sort='relevance',
                                retmax='20',
                                retmode='xml',
                                term=query)
        results = Entrez.read(handle)
        handle.close()
        return results

    def fetch_details(self, id_list):
        ids = ','.join(id_list)
        handle = Entrez.efetch(db='pubmed',
                               retmode='xml',
                               id=ids)
        results = Entrez.read(handle)
        handle.close()
        return results

    def summary(self, id_list):
        ids = ','.join(id_list)
        handle = Entrez.esummary(db='pubmed',
                                 id=ids)
        result = Entrez.read(handle)
        handle.close()
        return result

    def getPMID(self, article):
        pmid = -1
        if article.title == '':
            return pmid
        # query by title
        t = article.title.encode('utf8')
        query = t
        ids_title = self.search(query)['IdList']

        if len(ids_title) == 1:
            pmid = ids_title[0]
        else:
            # query by author
            ids_author = None
            if len(article.authors) != 0:
                query = '[AUTH] AND '.join(article.authors)
                query += '[AUTH]'
                ids_author = self.search(query)['IdList']

            if ids_author is not None:
                if len(ids_title) == 0 and len(ids_author) == 1:
                    pmid = ids_author[0]
                if len(ids_title) > 1:
                    common_ids = set(ids_title).intersection(ids_author)
                    if len(common_ids) == 1:
                        pmid = common_ids.pop()
        if pmid != -1:
            linked_t = searcher.summary([str(pmid)])[0]['Title']
            if not linked_t.startswith(t.decode('utf8')):
                pmid = -1
        return pmid


if __name__ == '__main__':
    refs_all = pickle.load(open(pickle_folder + 'references_all.pickle', 'rb'))
    searcher = PubmedSearcher()

    result = dict()
    cnt = 0
    for doi in refs_all:
        print '***', doi.encode('utf8')
        print '{}/{}'.format(cnt, len(refs_all))
        refs = refs_all[doi][2]
        ref2pmid = dict()
        for ref_title in refs:
            print ref_title
            pmid_list = []
            for a in refs[ref_title]:
                pmid = -1
                if 'PubMed' in a.extRefs:
                    pmid = a.extRefs['PubMed'].split('id=')[-1]
                else:
                    pmid = searcher.getPMID(a)
                pmid_list.append(pmid)
            ref2pmid[ref_title] = pmid_list
        result[doi] = ref2pmid
        cnt += 1
    pickle.dump(result, open(pickle_folder + 'ref2pmid.pickle', 'wb'))
