from bs4 import BeautifulSoup
from Article import Article


class RefParser:
    """
    Parser for extracting information from the HTML file of CDSR references.

    Example file:
    fullbatch/200.aa/references.1
    """

    def __init__(self):
        pass

    @staticmethod
    def getArticleAttr(soup, className, defaultVal):
        val = soup.find('span', class_=className)
        val = val.text if val is not None else defaultVal
        return val

    def parse(self, filename):
        html = open(filename).read()
        soup = BeautifulSoup(html, 'html.parser')
        # doi
        doi = soup.find('p', {'id': 'doi'}).text
        # article title
        title = soup.find('h1', {'class': 'articleTitle'}).text
        bib_div = soup.find('div', {'class': 'bibliography'})
        ret = {}
        if bib_div is None:
            return doi, title, ret
        included_div = None
        for child in bib_div.children:
            if child['class'][0] == 'bibSection':
                if child.div.text.startswith('References to studies included'):
                    included_div = child
                    break
        if included_div is None:
            return doi, title, {}
        refs = included_div.find_all('div', class_='bibSection')
        for ref in refs:
            ref_title = ref.find('div', class_='headingCont').text
            ref_title = ref_title.split('{')[0].strip()
            plain_div = ref.find('ul', class_='plain')
            if plain_div is None:
                continue
            articles = []
            for article_div in plain_div:
                citation = article_div.cite
                # print citation
                authors = [r.text for r in citation.find_all('span',
                                                             class_='author')]
                # print authors
                art_title = self.getArticleAttr(citation, 'articleTitle', '')
                # print title
                booktitle = self.getArticleAttr(citation, 'bookTitle', '')
                journal = self.getArticleAttr(citation, 'journalTitle', '')
                # print journal
                year = self.getArticleAttr(citation, 'pubYear', -1)
                # print year
                vol = self.getArticleAttr(citation, 'vol', -1)
                page_st = self.getArticleAttr(citation, 'pageFirst', -1)
                page_ed = self.getArticleAttr(citation, 'pageLast', -1)
                extRefs = {}
                if article_div.ul is not None:
                    links = article_div.ul.find_all('a')
                    for link in links:
                        resource = link.text.split('Times Cited')[0].strip()
                        extRefs[resource] = link.get('href')
                # print extRefs
                article = Article(authors=authors,
                                  title=art_title,
                                  booktitle=booktitle,
                                  journal=journal,
                                  year=year,
                                  vol=vol,
                                  page_st=page_st,
                                  page_ed=page_ed,
                                  extRefs=extRefs)
                articles.append(article)
            ret[ref_title] = articles
        return doi, title, ret


def dumpAsPickle():
    import cPickle as pickle
    import os
    from utils import data_folder, pickle_folder
    cdsr_data_folder = data_folder + 'fullbatch/'
    result = {}
    p = RefParser()
    for folder in os.listdir(cdsr_data_folder):
        print '=' * 80
        print folder
        review_count = 0
        for f in os.listdir(cdsr_data_folder + folder + '/'):
            if f.startswith('references'):
                review_count += 1
                ret = p.parse(cdsr_data_folder + folder + '/' + f)
                result[ret[0]] = ret
                if review_count % 10 == 0:
                    print review_count
        print review_count
    pickle.dump(result, open(pickle_folder + 'references_all.pickle', 'wb'))

if __name__ == '__main__':
    dumpAsPickle()
