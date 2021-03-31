from QuestionMaker import Make,Finder
from sys import argv, exit
from Extractor import WordExtractor
from bs4 import BeautifulSoup
import requests
import os
import random
import re
from nltk.corpus import wordnet ,words,stopwords
from datetime import datetime
import pandas as pd
from Synonym import Generator
word_list = words.words()
sr = stopwords.words('english')
def get_words():
    page = requests.get("https://randomtextgenerator.com/")
    print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    corpus = soup.find_all('textarea', {'id':"generatedtext"})[0].get_text()
    return corpus

def make_tokens(corpus):
    we = WordExtractor(corpus)
    words = we.get_tokens()
    return words

def get_meaning(word):
    page = requests.get("https://www.dictionary.com/browse/"+word)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        meaning  = soup.find_all('span', {'class':"one-click-content css-1p89gle e1q3nk1v4"})[0].get_text()
    except IndexError:
        pass
    try:
        clean_meaning = re.split(';|:',meaning)[0]
    except IndexError:
        clean_meaning = meaning
    if clean_meaning[-1] == ".":
        clean_meaning = clean_meaning[:-1]
    return clean_meaning

class Question:
    def __init__(self):
        self.words = make_tokens(get_words())
        self.quest_dict = {
                "Question":[],
                "Option1":[],
                "Option2":[],
                "Option3":[],
                "Option4":[],
                "Answer":[]
                }
    
    def add_question(self, question,answer,options):
        self.quest_dict["Question"].append(question)
        options_list = ["Option1","Option2","Option3","Option4"]
        random.seed()
        right_op = random.choice(options_list)
        self.quest_dict[right_op].append(answer)
        self.quest_dict["Answer"].append(right_op)
        rem_options = options_list[:]
        rem_options.remove(right_op)
        for index, opt in enumerate(rem_options):
            self.quest_dict[opt].append(options[index])
        
        
        
    def make_question(self):
        words = []
        i = 0
        while i == 0:
            word = random.choice(self.words)
            if word not in words:
                i = 1
        meaning = get_meaning(word)
        question = "Select the word which can be substituted for the given phrase. \n {}.".format(meaning)
        answer = word
        finder = Finder(word)
        _, antonyms, distractors = finder.syn_ants()
        options = []
        if len(antonyms) > 0:
            options.append(antonyms[0])
        if len(distractors) >= 3:
            while len(options) < 3:
                options.append(random.choice(distractors))
        else:
            for dis in distractors:
                options.append(dis)
            while len(options) < 3:
                rand_word = random.choice(word_list)
                if len(rand_word)>5:
                    options.append(rand_word)
        self.add_question(question,answer,options)
    
    def save_questions(self):
        df = pd.DataFrame(self.quest_dict)
        df.to_csv("Questions.csv")
     



def main():
    if len(argv) < 2:
        print("Please enter number of questions for file %s" % argv[0])
        exit(1)
    num_questions = argv[1]
    q = Question()
    for i in range(int(num_questions)):
        q.make_question()
        print("Made {} quesitons.".format(i+1))
    q.save_questions()



if __name__ == "__main__":
    main()

            
        
        
        
    
    