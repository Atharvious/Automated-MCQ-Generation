import requests
from bs4 import BeautifulSoup
from nltk.corpus import wordnet ,words
import random
import pandas as pd
from datetime import datetime

word_list = words.words()
class Finder:
    
    def __init__(self, word):
        self.word = (word.strip()).lower()
    
    def syn_ants(self):
        synonyms = []
        antonyms = []
        discs = []
        page = requests.get("https://www.thesaurus.com/browse/"+self.word)
        soup = BeautifulSoup(page.content, 'html.parser')
        a_tags_syn = soup.find_all('a', {'class':"css-gkae64 etbu2a31"})
        a_tags_ant = soup.find_all('a', {'class':"css-16nmaxb etbu2a31"})
        a_tags_dis = soup.find_all('a', {'class':"css-133coio etbu2a32"})
        for tag in a_tags_syn:
            synonyms.append(tag.get_text())
        for an_tag in a_tags_ant:
            antonyms.append(an_tag.get_text())
        for dis in a_tags_dis:
            discs.append(dis.get_text())
        return synonyms,antonyms,discs
    
class Make(Finder):
    def __init__(self, word):
        self.word = (word.strip()).lower()
        self.synonyms, self.antonyms, self.discs = self.syn_ants()
        self.answer = ''
        self.distractors = []
        self.solution = ''
        self.ans_solution = ''
    
    
    def takesecond(self,elem):
        return elem[1]
    
    def get_solution(self, ans = None):
        if ans is None:
            page = requests.get("https://www.dictionary.com/browse/"+self.word)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                mean  = soup.find_all('span', {'class':"one-click-content css-1p89gle e1q3nk1v4"})[0].get_text()
                self.solution = mean
            except IndexError:
                pass
        else:
            page = requests.get("https://www.dictionary.com/browse/"+ans)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                ans_mean = soup.find_all('span',{'class':"one-click-content css-1p89gle e1q3nk1v4"})[0].get_text()
                self.ans_solution = ans_mean
            except IndexError:
                pass
            
            
    def get_answer(self):
        max_sim = 0
        try:
            word_obj = wordnet.synsets(self.word)[0]
            word_pos = word_obj.name().split(".")[1]
        except IndexError:
            self.answer = ''
            return 0
        for syn in self.synonyms:
            try:
                synsets = wordnet.synsets(syn)
            except IndexError:
                continue
            for synset in synsets:
                name = synset.name().split(".")[0]
                pos = synset.name().split(".")[1]
                if name != self.word and pos == word_pos:
                    path_sim = synset.wup_similarity(word_obj)
                    if path_sim and path_sim >max_sim:
                        max_sim = path_sim
                        self.answer = syn
        return 1
    
    def get_distractors(self):
        syns_with_scores = []
        distractors = []
        try:
            word_obj = wordnet.synsets(self.word)[0]
        except IndexError:
            print("Word not in wordnet")
            self.distractors = []
            return 0
        for syns in self.discs:
            syn_obj = wordnet.synsets(syns)
            for synset in syn_obj:
                name = synset.name().split(".")[0]
                if name != self.word:
                    path_sim = synset.path_similarity(word_obj)
                    if path_sim:
                        syns_with_scores.append((syns,path_sim))
        sorted_syns = sorted(syns_with_scores,key = lambda x: x[1])
        if len(self.antonyms)>0:
            distractors.append(self.antonyms[0])
        if len(sorted_syns)>=3:
            for tuples in sorted_syns:
                if tuples[0] != self.answer and tuples[0] not in distractors:
                    distractors.append(tuples[0])
        elif len(self.discs) > 3:
            distractors = self.discs[:3]
        else:
            distractors = self.discs[:]
        distractors = list(set(distractors))
        if len(distractors)<=3:
            random.seed(datetime.now())
            random.shuffle(word_list)
            to_rem = 3 - len(distractors)
            ran_words = word_list[:to_rem]
            distractors.extend(ran_words)
        self.distractors = distractors[:]
            
               
            
    def make_question(self):
            flag = self.get_answer()
            dis_flag = self.get_distractors()
            self.get_solution()
            self.get_solution(self.answer)
            if len(self.word)== 0 or len(self.answer) == 0 or len(self.distractors) < 3 or len(self.solution) == 0 or len(self.ans_solution) == 0:
                print("Not enough word data, the variables are:")
                self.show()
                return None
            elif (self.word in self.ans_solution) or (self.answer in self.solution): 
                return (self.word,self.answer, self.distractors,self.solution,self.ans_solution )
            else:
                print("Word Meanings are different.")
                return None
            
            
    
    def show(self):
        print("Word {},Answer {}, Options {}.".format(self.word, self.answer,self.distractors))