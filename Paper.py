import re


class Paper:

    def __init__(self, pmid, rob):
        self.pmid = pmid
        self.rob = rob

    def extractQuotes(self):
        quotes = {}
        double_quote = re.compile('\"(.+?)\"')
        for d in self.rob:
            label = self.rob[d][0]
            comment = self.rob[d][1]
            quote_sents = double_quote.findall(comment)
            if len(quote_sents) > 0:
                quotes[d] = (label, quote_sents)
        self.quotes = quotes
