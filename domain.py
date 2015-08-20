import yaml
import cPickle as pickle
from utils import data_folder, pickle_folder


def export_domains_from_cdsr():
    '''
    Get domains from CDSR first
    '''
    tables_all = pickle.load(open(pickle_folder + 'tables_all.pickle', 'rb'))
    domain_freq = {}
    judgement = set()
    for doi in tables_all:
        print doi.encode('utf8')
        tables = tables_all[doi][2]
        for ref in tables:
            for rob in tables[ref]:
                domain_freq[rob[0]] = domain_freq.get(rob[0], 0) + 1
                judgement.add(rob[1])
    print judgement
    with open(data_folder + 'outputs/domain.csv', 'w') as fout:
        for d in domain_freq:
            fout.write('{}\t{}\n'.format(d.encode('utf8'), domain_freq[d]))


def generate_new_mapping():
    '''
    Generate domain mapping file.

    The mapping is based on
    'https://github.com/ijmarshall/cochrane-nlp/tree/master/data/domain_names.txt'
    and some heuristics
    '''
    existed_map = yaml.load(open(data_folder + 'domain_names.txt', 'rb'))
    print existed_map.keys()
    mapping = dict()
    keys = set()
    for k, l in existed_map.iteritems():
        k = k.lower()
        if k.startswith('other sources of bias'):
            k = 'other sources of bias'
        keys.add(k)
        for d in l:
            d = d.lower()
            if d in mapping:
                if mapping[d] != k:
                    if mapping[d] == 'Uncategorised other':
                        mapping[d] = k
            else:
                mapping[d] = k
    print keys
    domains = dict()
    with open(data_folder + 'outputs/domain.csv') as f:
        for line in f:
            s = line.split('\t')
            domains[s[0].lower()] = domains.get(s[0].lower(), 0) + int(s[1])
    new_mapping = {}
    with open(data_folder + 'outputs/mapped_domains_new.csv', 'w') as f:
        for d in domains:
            v = ''
            if d in mapping:
                v = mapping[d]
            else:
                for k in keys:
                    if d.startswith(k):
                        v = k
                        break
                if v == '':
                    if 'blinding' in d and '(detection bias)' in d:
                        v = 'blinding of outcome assessment'
                    else:
                        if d.startswith('blinding'):
                            v = 'blinding of participants and personnel'
            if v != '':
                new_mapping[d] = v
            line = str(domains[d]) + '\t' + d + '\t' + v + '\n'
            f.write(line)
    pickle.dump(new_mapping, open(pickle_folder + 'domain_mapping.pickle',
                                  'wb'))

if __name__ == '__main__':
    # export_domains_from_cdsr()
    generate_new_mapping()
