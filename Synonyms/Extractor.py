# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 18:38:01 2019

@author: ATHARVA
"""
import nltk
from nltk.corpus import wordnet,stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
wnl = WordNetLemmatizer()
sr = stopwords.words('english')
class WordExtractor:
    def __init__(self,text):
        self.text = text
        
    @classmethod
    def fromfile(cls,file_path,file_name):
        with open(file_path+file_name+".txt") as f:
            file_text = f.read()
        return(cls(file_text))
        
    def get_tokens(self):
        tokens = []
        only_av = []
        tokes = word_tokenize(self.text)
        for token in tokes:
            if not token in stopwords.words('english'):
                tokens.append(token)
        tags = nltk.pos_tag(tokens)
        req_tags = ['JJ','JJR','JJS','VB','VBD','VBG','VBN','VBP','VBZ']
        for tag_tup in tags:
            if len(tag_tup[0])>4:
                if tag_tup[1] in req_tags:
                    if tag_tup[1][0] == 'J':
                        if tag_tup[1][::-1] == 'S':
                            root_word = wnl.lemmatize(tag_tup[0], 's')
                        else:
                            root_word = wnl.lemmatize(tag_tup[0],'a')
                        only_av.append(root_word)
                    elif tag_tup[1][0] == 'R':
                        root_word = wnl.lemmatize(tag_tup[0],'rs')
                        only_av.append(root_word)
                    elif tag_tup[1][0] == 'V':
                        root_word = wnl.lemmatize(tag_tup[0],'v')
                        only_av.append(root_word)        
        return list(set(only_av))        
