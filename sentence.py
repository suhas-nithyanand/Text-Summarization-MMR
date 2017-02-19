class sentence(object):
    '''This module is a sentence data structure'''

    def __init__(self, docName, stemmedWords, OGwords):

        self.stemmedWords = stemmedWords
        self.docName = docName
        self.OGwords = OGwords
        self.wordFrequencies = self.sentenceWordFreqs()

    def getStemmedWords(self):
     
        return self.stemmedWords

    def getDocName(self):
        return self.docName
    
    def getOGwords(self):
          return self.OGwords

    def getWordFreqs(self):
        return self.wordFrequencies

    def sentenceWordFreqs(self):

        wordFreqs = {}
        for word in self.stemmedWords:
            if word not in wordFreqs.keys():
                wordFreqs[word] = 1
            else:
                wordFreqs[word] = wordFreqs[word] + 1
                
        return wordFreqs

    
