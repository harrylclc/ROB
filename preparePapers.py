import cPickle as pickle
import re
from Paper import Paper
from utils import pickle_folder, d2idx


def get_judgement_label(s):
    if 'low' in s or 'yes' in s:
        return 1
    if 'high' in s or 'no' in s or 'unclear' in s:
        return 0
    return -1

if __name__ == "__main__":
    tables = pickle.load(open(pickle_folder + 'tables_all.pickle', 'rb'))
    refs = pickle.load(open(pickle_folder + 'references_all.pickle', 'rb'))
    ref2pmid = pickle.load(open(pickle_folder + 'ref2pmid.pickle', 'rb'))
    dmap = pickle.load(open(pickle_folder + 'domain_mapping.pickle', 'rb'))
    papers = []
    for doi in refs:
        if doi not in tables:
            continue
        print doi.encode('utf8')
        sr = refs[doi]
        ref2articles = sr[2]
        ref2ids = ref2pmid[doi]
        ref2rob = tables[doi][2]
        for ref in ref2articles:
            print '=' * 80
            print ref.encode('utf8')
            articles = ref2articles[ref]
            ids = ref2ids[ref]
            if ref not in ref2rob:  # no ROB table for this reference
                continue
            robs = ref2rob[ref]

            # Since there may be multiple articles for a single reference
            # we need to choose the corresponding article for the reference
            article_idx = -1
            if len(articles) == 1:
                article_idx = 0
            else:
                m = re.search('[0-9]?(.+?)([0-9]{4})', ref)
                if m:
                    s = m.group(1).strip().split()
                    name = s[0]
                    if s[0].isupper() and len(s) > 1:
                        name = s[1]
                    print name.encode('utf8')
                    year = m.group(2)
                    for k, a in enumerate(articles):
                        if len(a.authors) == 0:
                            continue
                        first_author = a.authors[0]
                        if first_author.startswith(name) \
                                and str(a.year) == year:
                            article_idx = k
                            break
            if article_idx == -1:
                continue
            pmid = ids[article_idx]
            if pmid == -1:
                continue
            rob_map = {}
            conflict_d = set()
            for rob in robs:
                d = dmap.get(rob[0].lower(), '')
                if d in d2idx and d not in conflict_d:
                    label = get_judgement_label(rob[1].lower())
                    if label == -1:
                        print '=====', 'Invalid label', rob
                        continue
                    if d in rob_map:
                        label_prev = rob_map[d][0]
                        if label_prev != label:
                            rob_map.pop(d)
                            conflict_d.add(d)
                            continue
                        else:
                            rob_map[d] = (label, rob_map[d][1] + ' ' + rob[2])
                    else:
                        rob_map[d] = (label, rob[2])
            p = Paper(pmid=pmid, rob=rob_map)
            p.extractQuotes()
            papers.append(p)
        # break
    pickle.dump(papers, open(pickle_folder + 'papers.pickle', 'wb'))
