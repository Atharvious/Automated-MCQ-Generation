import os
import re
import pandas as pd
from Extractor import WordExtractor
import requests
from bs4 import BeautifulSoup
import random
import nltk
from nltk.corpus import words
from nltk.corpus import wordnet as wn
word_list = words.words()
from sys import argv,exit


def get_words():
    page = requests.get("https://randomtextgenerator.com/")
    print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    corpus = soup.find_all('textarea', {'id':"generatedtext"})[0].get_text()
    we = WordExtractor(corpus)
    words = we.get_tokens()
    return words

def find_example(word):
    url = "https://www.thesaurus.com/browse/{}".format(word)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    req_content = soup.find_all('p')
    example = [x.get_text() for x in req_content][0]
    return example
    
def syn_ants(word):
        synonyms = []
        antonyms = []
        discs = []
        page = requests.get("https://www.thesaurus.com/browse/"+word)
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
        self.words = get_words()
        self.quest_dict = {
                "Question":[],
                "Option1":[],
                "Option2":[],
                "Option3":[],
                "Option4":[],
                "Answer":[],
                "Solution":[]
                }
        
    def add_question(self, question,answer,options,solution):
        self.quest_dict["Question"].append(question)
        self.quest_dict["Solution"].append(solution)
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
        if not self.words:
            self.words = get_words()
        else:
            random.seed()
            word = random.choice(self.words).lower()
            self.words.remove(word)
        try:
            example = find_example(word)
            question = example.replace(word,"_____",1)
            answer = word
            flag = 0
            p_tag = nltk.pos_tag([word])[0][1]
            if p_tag[0] == "V" and p_tag[-1] == "D":
                flag = 1
            meaning = get_meaning(word)
            solution = "{} means {}".format(word,meaning)
            options = []
            distractors,antonyms,_ = syn_ants(word)
            options = []
            if len(antonyms) > 0:
                antonym = antonyms[0]
                if flag == 1:
                    if antonym[-1] == "e":
                        antonym = antonym + "d"
                    else:
                        antonym = antonym + "ed"
                options.append(antonym)
            if len(distractors) >= 3:
                while len(options) < 3:
                    random.seed()
                    rand_dis = random.choice(distractors)
                    if flag == 1:
                        if rand_dis[-1] == "e":
                            rand_dis = rand_dis + "d"
                        else:
                            rand_dis = rand_dis + "ed"
                    options.append(rand_dis)
            else:
                for dis in distractors:
                    if flag == 1:
                        if dis[-1] == "e":
                            dis = dis + "d"
                        else:
                            dis = dis + "ed"
                    options.append(dis)
                while len(options) < 3:
                    rand_word = random.choice(word_list)
                    if len(rand_word)>5 and nltk.pos_tag([rand_word])[0][1] == p_tag:
                        options.append(rand_word)
            self.add_question(question,answer,options,solution)
        except Exception:
            print(Exception)
            pass
        
            
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
        print("Made {} questions.".format(i+1))
    q.save_questions()



if __name__ == "__main__":
    main()
