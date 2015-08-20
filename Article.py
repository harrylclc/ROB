class Article:
    """
    Store the metadata of a study.
    """

    def __init__(self, authors=[], title='', journal='', year=-1, vol=-1,
                 page_st=-1, page_ed=-1, extRefs={}, booktitle=''):
        self.authors = authors
        self.title = title
        self.journal = journal
        self.year = year
        self.vol = vol
        self.page_st = page_st
        self.page_ed = page_ed
        self.extRefs = extRefs
        self.booktitle = booktitle

    def getTitle(self):
        if self.title != '':
            return self.title
        else:
            return self.booktitle

    def __repr__(self):
        title = self.title if self.title != '' else self.booktitle
        return str(self.year) + ' ' + title.encode('utf8')
