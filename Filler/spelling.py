import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests
import random
sr = stopwords.words("english")


def change_spelling(word):
    def change_ie(word):
        if "ie" in word:
            word = word.replace("ie", "ei",1)
        return word
    def replace_similar_sounds(word):
        sim_sounds = {
                "k":"c",
                "s":"c",
                "f":"ph",
                "a":"ae"}
        for key,val in sim_sounds.items():
            if key in word:
                word = word.replace(key,val,1)
                return word
            elif val in word:
                word = word.replace(key,val,1)
                return word
        return word
    
    def remove_vowels(word):
        vowels = ["a","e","i","o","u"]
        present_vows = []
        for v in vowels:
            if v in word:
                present_vowels.append(v)
        if len(present_vows) > 0:
            random.seed()
            rand_vowel = random.choice(present_vows)
            word = word.replace(rand_vowel,"",1)
        return word
    to_select = ["ie", "simsounds","vowels"]
    
    
    


def get_random_words():
    page = requests.get("https://randomtextgenerator.com/")
    print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    corpus = soup.find_all('textarea', {'id':"generatedtext"})[0].get_text()
    tokens = word_tokenize(corpus)
    clean_tokens = []
    for word in tokens:
        if word not in sr and len(word) > 5:
            clean_tokens.append(word)
    return clean_tokens

words = get_random_words()

