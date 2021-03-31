import os

from QuestionMaker import Make
from Extractor import WordExtractor
from bs4 import BeautifulSoup
import requests
import random
from datetime import datetime
import pandas as pd

class Generator:
    def __init__(self, file_name):
        self.get_text()
        we = WordExtractor(self.corpus)
        self.words = we.get_tokens()
        self.file_name = file_name
        self.quest_dict = {
            "Question": [],
            "Option1" : [],
            "Option2" : [],
            "Option3" : [],
            "Option4" : [],
            "Right Answer":[],
            "Solution": [],
            "Answer Meaning": []}
        self.made_quests = 0
        
    def get_text(self):
        page = requests.get("https://randomtextgenerator.com/")
        print(page.status_code)
        soup = BeautifulSoup(page.content, 'html.parser')
        corpus = soup.find_all('textarea', {'id':"generatedtext"})[0].get_text()
        self.corpus = corpus

    def make_from_text(self):
        options_list = ["Option1","Option2","Option3","Option4"]
        for word in self.words:
            if self.made_quests >= self.tot_no:
                break
            random.seed(datetime.now())
            q = Make(word)
            quest_opt = q.make_question()
            if not quest_opt is None:
                _,answer, options, solution,ans_solution = q.make_question()
                right_opt = random.choice(options_list)
                rem_list = options_list[:]
                rem_list.remove(right_opt)
                print(right_opt)
                self.quest_dict["Question"].append("Choose the word , which is closest in meaning to - {}".format(word))
                self.quest_dict[right_opt].append(answer)
                for i,opt in enumerate(rem_list):
                    self.quest_dict[opt].append(options[i])
                self.quest_dict["Right Answer"].append(right_opt)
                self.quest_dict["Solution"].append("{} means {}".format(word,solution))
                self.quest_dict["Answer Meaning"].append("{} means {}".format(answer, ans_solution))
                self.made_quests = self.made_quests + 1
                print("Made question {} of {}".format(self.made_quests,self.tot_no))
        if self.made_quests < self.tot_no:
            self.get_text()
            we = WordExtractor(self.corpus)
            self.words = we.get_tokens()
            self.make_from_text()
                
        
        
    def save_data(self):
        df = pd.DataFrame(self.quest_dict)
        try:
            df.to_csv(self.file_name+".csv")
        except PermissionError:
            self.file_name.append("_")
            df.to_csv(self.file_name+"_1.csv")
        
    def run(self, num_questions = None):
        if num_questions:
            self.tot_no = num_questions
        else:
            self.tot_no = len(self.words)
        self.make_from_text()
        self.save_data()