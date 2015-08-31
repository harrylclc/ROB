from utils import data_folder, pickle_folder, d2idx
import cPickle as pickle

if __name__ == "__main__":
    papers = pickle.load(open(pickle_folder + 'papers.pickle', 'rb'))
    sents = [[] for i in xrange(len(d2idx))]
    for p in papers:
        if len(p.quotes) > 0:
            for d in p.quotes:
                idx = d2idx[d]
                sents[idx].extend(p.quotes[d][1])
    for d in d2idx:
        with open(data_folder + 'outputs/' + d + '.sents', 'w') as f:
            for sent in sents[d2idx[d]]:
                f.write(sent.encode('utf8') + '\n')
