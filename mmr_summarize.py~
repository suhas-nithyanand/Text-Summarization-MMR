import os
import math
import process_text
import sentence
import nltk


class document_similarity(object):  
    def __init__(self):
        self.text = process_text.process_text()
        

    '''Function to compute the TF-IDF values for all words in a document cluster'''

    def TFs(self, sentences):
        tfs = {}

        for sent in sentences:
            wordFreqs = sent.getWordFreqs()

            for word in wordFreqs.keys():
                if tfs.get(word, 0) != 0:
                    tfs[word] = tfs[word] + wordFreqs[word]
                else:
                    tfs[word] = wordFreqs[word]
        return tfs
            
            
    
    '''Function to compute the term frequency for a word in a given sentence'''
   
    def TFw(self, word, sentence):
        return sentence.getWordFreqs().get(word, 0)

    
    ''' Function to compute the IDF value of a given word'''
    
    def IDFs(self, sentences):
        
        N = len(sentences)
        idf = 0
        idfs = {}
        words = {}
        w2 = []

        for sent in sentences:
            for word in sent.getStemmedWords():
                if sent.getWordFreqs().get(word, 0) != 0:
                    words[word] = words.get(word, 0)+ 1
                    
                    
        for word in words:
            n = words[word]
            try:
                w2.append(n)
                idf = math.log10(float(N)/n)
            except ZeroDivisionError:
                idf = 0
            idfs[word] = idf
                
        return idfs


    ''' Function to calculate the IDF values for all the words in a document cluster '''
   
    def IDF(self, word, idfs):
        return idfs[word]


    
    '''Function to compute the similarity score between 2 sentences'''

    def sim(self, sentence1, sentence2, idfs):

        numerator = 0
        denom1 = 0
        denom2 = 0

        for word in sentence2.getStemmedWords():
            numerator += self.TFw(word, sentence2) * self.TFw(word, sentence1) * self.IDF(word, idfs) ** 2

        for word in sentence1.getStemmedWords():
            denom2 += (self.TFw(word, sentence1) * self.IDF(word, idfs)) ** 2
                
        for word in sentence2.getStemmedWords():
            denom1 += (self.TFw(word, sentence2) * self.IDF(word, idfs)) ** 2

        try:
            return numerator / (math.sqrt(denom1) * math.sqrt(denom2))

        except ZeroDivisionError:
            return float("-inf")



''' Class to provide summary building functionality. It uses a Maximum Marginal Relevance
 algorithim to select the best n sentences in a document clusters'''


class mmr_summarize(object):
   
    def __init__(self):
        self.text = process_text.process_text()
        self.sim = document_similarity()


    
    '''Function to compute every word's TF.IDF value in a given cluster'''

    def TF_IDF(self, sentences, idfs):
        tfs = self.sim.TFs(sentences)
        
        retval = {}

        for word in tfs:
            tf_idfs=  tfs[word] * idfs[word]        

            if retval.get(tf_idfs, None) == None:
                retval[tf_idfs] = [word]
            else:
                retval[tf_idfs].append(word)

        return retval


       
    ''' Function to build a query by selecting n words with the highest TF.IDF values '''
   

    def makeQuery(self, n, sentences, idfs):
        scored_words = self.TF_IDF(sentences, idfs)
        best_words = self.getBestWords(n, scored_words)
        return sentence.sentence("query", best_words, [])


    
    ''' Function to build a list of the n best words in a cluster'''
    
    def getBestWords(self, n, scored_words):

        best_scores  = scored_words.keys()
        best_scores.sort()
        best_words = []

        for i in range(-1, -n, -1):
            
            words = scored_words[best_scores[i]]
            for word in words:
                if i >-n:
                    best_words.append(word)
                    i = i-1
        return best_words


   
    ''' Function to get the single Best matching sentence '''
  
    def getBestSentence(self, sentences, query, idfs):

        best_sent = None
        prev = float("-inf")
        
        for sent in sentences:
            similarity = self.sim.sim(sent, query, idfs)

            if similarity > prev:
                best_sent = sent
                prev = similarity
                    
        sentences.remove(best_sent)
        return best_sent



    '''Function to find n sentences with the best MR values'''

    def makeSummary(self, gamma, sentences, query, best_sentence, idfs, summary_length ):
        selected_sentences = [best_sentence]
        summary = [best_sentence]
        
        for i in range(summary_length):
            best_line = None
            prev = float("-inf")
            
            for sent in sentences:
                curr = self.MR(gamma, sent, query, idfs, selected_sentences)
                if curr > prev:
                    prev = curr
                    best_line = sent    
            selected_sentences += [best_line]
            sentences.remove(best_line)
            
        return selected_sentences
            
            
    ''' Function to compute the MR value for a given sentence'''

    def MR(self, gamma, sent, query , idfs, selected_sentences):
        
        left_of_minus = gamma * self.sim.sim(sent, query, idfs)
        
        right_values = [float("-inf")]
        
        for selected_sentence in selected_sentences:
            right_values.append( (1 - gamma) * self.sim.sim(sent, selected_sentence, idfs))
            
        right_of_minus = max(right_values)
        
        return left_of_minus - right_of_minus

        
 
    '''Function to make a summary'''

    def main(self, n, summary_lentgh, cluster_path):

        sentences =  self.text.openDirectory(cluster_path)
        idfs = self.sim.IDFs(sentences)
       
        # build a query
        query = self.makeQuery(n, sentences, idfs)
        best_sentence = self.getBestSentence(sentences, query, idfs)
        summary = self.makeSummary(0.5, sentences, query, best_sentence, idfs, 4)
        
        return summary

