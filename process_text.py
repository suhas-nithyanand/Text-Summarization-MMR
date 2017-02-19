import nltk
import os
import math
import string
import sentence
import re


class process_text(object):


    ''' Method for file IO processes. Opens a file, Removes HTML tags and tokenizes the file'''

    def processFile(self, file_path_and_name):
        try:
            f = open(file_path_and_name,'r')
            text = f.read()

            text = re.sub('<[^<]+?>', '', text)
            sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                
            lines = sent_tokenizer.tokenize(text.strip())

            text = lines

            sentences = []
            porter = nltk.PorterStemmer()
            
            for sent in lines:
                OG_sent = sent[:]
                sent = sent.strip().lower()
                line = nltk.word_tokenize(sent)
            
                stemmed_sentence = [porter.stem(word) for word in line]
                stemmed_sentence = filter(lambda x: x!='.'and x!='`'and x!=','and x!='?'and x!="'"
                                    and x!='!' and x!='''"''' and x!="''" and x!="'s", stemmed_sentence)
                if stemmed_sentence != []:
                    sentences.append(sentence.sentence(file_path_and_name, stemmed_sentence, OG_sent))
            
            return sentences


        except IOError:
            print 'Oops! File not found',file_path_and_name
            return [sentence.sentence(file_path_and_name, [],[])]


    '''Method to process a document by replacing all versions of a name with the fullest version of the same name '''

    def use_full_names(self, doc):
        names = self.getNames(doc)
        
        for i in range(len(doc)):
            doc[i] = self.getLongName(doc[i], names)
        return doc
        
    ''' Method to get all the named entities in a document '''

    def getNames(self, doc):

        doc = ' '.join(doc).split()
        st = nltk.tag.stanford.NERTagger('C:/Users/tmpasi10/Desktop/ner/classifiers/english.all.3class.distsim.crf.ser.gz',\
                                         'C:/Users/tmpasi10/Desktop/ner/stanford-ner.jar')

        tags = st.tag(doc)
        doc = ' '.join(doc)

        names = []

        flag1 = False 

        for i in range(1, len(tags)):
            tag1 = tags[i-1]
            tag2 = tags[i]
            
            if i+1 < len(tags):
                tag3 = tags[i+1]
                if tag1[1] == 'PERSON' and tag2[1] == 'PERSON' and tag3[1] =='PERSON':
                    name = tag1[0] + ' ' + tag2[0] + ' ' + tag3[0]
                    if doc.find(name) > -1:
                        names.append(name)
                        i = i + 3
                        flag1 = True

            if tag1[1] == 'PERSON' and tag2[1] == 'PERSON' and not flag1 and i<len(tags):
                name = tag1[0] + ' ' + tag2[0]
                if doc.find(name) > -1:
                    names.append(name)
                    i = i + 2
                else:
                    i = i + 1
        return names


    ''' Method to replace all shortened versions of a name with their original long version '''

    def getLongName(self, sentence, names):
        sentence = sentence.split(" ")
        
        i = 0
        while i < len(sentence):
            word1 = sentence[i]
            for name in names:
                flag = False

                if i+1 != len(sentence):
                    word2 = sentence[i+1]
                    _2words = word1 + ' ' + word2
                    if self.begins_or_ends_with(_2words, name) and _2words != name:
                        if i == len(sentence)-2:
                            print sentence[i-1] + ' ' +_2words, name
                            sentence[i] = name
                            sentence = sentence[:i] + [name]
                            flag = True
                           
                        else:
                            temp = _2words + ' ' + sentence[i+2]
                            if temp != name and temp[:len(temp)-1] != name:
                                sentence = sentence[:i] + [name] + sentence[i+2:]
                                flag = True
                                
                if self.begins_or_ends_with(word1, name) and not flag:
                    if i == len(sentence)-1:
                        sentence[i] = name
                       
                    else:
                        if sentence[i+1] != name.split(" ")[1]:
                            sentence[i] = name
            i +=1          
                        
        return ' '.join(sentence)


    ''' Method to check whether a word is part of the begining or ending of a recognized name '''

    def begins_or_ends_with(self, word, name):
        return name[:len(word)] == word or name[len(name)-len(word):] == word



    ''' Method to get a document's file path '''

    def get_file_path(self, file_name):
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if name == file_name:
                    return os.path.join(root,name)
        print "Error! file was not found!!"
        return ""
    

    ''' Method to get all file names from a directory '''

    def get_all_files(self, path = None):
        retval = []
        
        if path == None:
            path = os.getcwd()

        for root, dirs, files in os.walk(path):
            for name in files:
                retval.append(os.path.join(root,name))
        return retval


    ''' Method to open all documents in a given directory '''

    def openDirectory(self, path=None):
        file_paths = self.get_all_files(path)
        
        sentences = []
    
        for file_path in file_paths:        
            sentences = sentences + self.processFile(file_path)
            
        return sentences
