from bs4 import BeautifulSoup


class TableParser:
    """
    Parser for extracting information from the HTML file of CDSR tables.

    Example file:
    fullbatch/200.aa/tables.1
    """

    def __init__(self):
        pass

    def parse(self, filename):
        html = open(filename).read()
        soup = BeautifulSoup(html, 'html.parser')
        # doi
        meta_div = soup.find('div', {'id': 'articleMeta'})
        doi = meta_div.find('p', {'id': 'doi'}).text
        # article title
        title = soup.find('h1', {'class': 'articleTitle'}).text
        ret = {}
        fulltext_div = soup.find(id='mrwFulltext')
        sections = fulltext_div.find_all('div', class_='emrw-table')
        if len(sections) == 0:  # no sections
            return doi, title, ret
        # find the section for "included studies"
        included_div = None
        for sec in sections:
            sec_title = sec.find('div', {'class': 'title'}).text
            if sec_title.startswith('Characteristics of included studies'):
                included_div = sec
                break
        if included_div is None:    # no "included studies"
            return doi, title, ret
        tables_div = included_div.findAll('div', {'class': 'table-container'})
        assert len(tables_div) == 1
        tables_div = tables_div[0]
        tables = tables_div.findAll('div', {'align': 'center'})

        for i in xrange(0, len(tables), 2):
            ref = tables[i].text
            data = tables[i+1].find('tr').find_next_sibling('tr')
            rows = data.find_all('tr')
            isROB = -1
            robs = []
            for j in xrange(0, len(rows), 2):
                row = rows[j]
                if isROB < 0:
                    if row.find('td').text == 'Risk of bias':
                        isROB = 0
                else:
                    if isROB < 1:
                        isROB += 1
                    else:
                        rob = row.find_all('td')
                        rob = [s.text for s in rob]
                        assert len(rob) == 3
                        robs.append(rob)
            ret[ref] = robs
        return doi, title, ret


def dumpAsPickle():
    import cPickle as pickle
    import os
    from utils import data_folder, pickle_folder
    cdsr_data_folder = data_folder + 'fullbatch/'
    result = {}
    p = TableParser()
    for folder in os.listdir(cdsr_data_folder):
        print '=' * 80
        print folder
        review_count = 0
        for f in os.listdir(cdsr_data_folder + folder + '/'):
            if f.startswith('tables'):
                review_count += 1
                ret = p.parse(cdsr_data_folder + folder + '/' + f)
                result[ret[0]] = ret
                if review_count % 10 == 0:
                    print review_count
        print review_count
    pickle.dump(result, open(pickle_folder + 'tables_all.pickle', 'wb'))


if __name__ == "__main__":
    dumpAsPickle()
