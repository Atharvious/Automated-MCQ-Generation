import random 
import pandas as pd
from sys import argv,exit
import math
class Circle:
    def __init__(self, radius):
        self.r = radius
        self.area = math.pi * self.r**2
        self.peri = math.pi * self.r * 2

class Rectangle:
    def __init__(self,length,breath):
        self.l = length
        self.b = breath
        self.peri = 2 * (self.l + self.b)
        self.area = self.l * self.b 

class Square():
    def __init__(self, side):
        self.l = side
        self.area = self.l **2
        self.peri = 4 * self.l
        
def make_shape(shape_trigger = 0):
    if shape_trigger == 0:
        random.seed()
        radius = random.randint(5,20)
        shape =Circle(radius)
    elif shape_trigger == 1:
        random.seed()
        length = random.randint(7,25)
        random.seed()
        breath = random.randint(5,20)
        shape = Rectangle(length, breath)
    elif shape_trigger == 2:
        random.seed()
        side = random.randint(5,20)
        shape =Square(side)
    return shape

def make_wrong_options(answer):
    wrong_answers = []
    while len(wrong_answers) < 3:
        random.seed()
        offset = random.randint(2,8)
        random.seed()
        wrong_ans = random.randint(int(answer) - offset, int(answer) + offset)
        if wrong_ans != answer and wrong_ans not in wrong_answers:
            wrong_answers.append(wrong_ans)
    return wrong_answers

class Question:
    def __init__(self):
        self.quest_dict = {
                "Question":[],
                "Option1":[],
                "Option2":[],
                "Option3":[],
                "Option4":[],
                "Answer":[],
                "Solution": []}
        self.ans_type = ["Cost", "Attributes"]
    
    
    def add_question(self, question,answer,options,solution):
        self.quest_dict["Question"].append(question)
        options_list = ["Option1","Option2","Option3","Option4"]
        random.seed()
        right_op = random.choice(options_list)
        self.quest_dict[right_op].append(answer)
        self.quest_dict["Answer"].append(right_op)
        self.quest_dict["Solution"].append(solution)
        rem_options = options_list[:]
        rem_options.remove(right_op)
        for index, opt in enumerate(rem_options):
            self.quest_dict[opt].append(options[index])                    
    
    def make_questions(self):
        random.seed()
        shape_trigger = random.randint(0,2)
        random.seed()
        shape_subs = {
                "circle":["circle","circular region","round plate", "circular disc","circular table top", "frisbee", "tire tube", "coin", "chapati"],
                "rectangle":["rectangle","eraser","book", "park", "duster","monitor screen","rectangular table top"]
                  }  

        q_type = "Attributes"
        if q_type == "Attributes":
            random.seed()
            attribute_trigger = random.randint(0,1)
            if attribute_trigger == 0:
                if shape_trigger == 0:
                    circle = make_shape(shape_trigger)
                    area = [circle.area, "area"]
                    perimeter = [circle.peri, "perimeter"]
                    random.seed()
                    rand_pick = random.choice([area,perimeter])
                    random.seed()
                    if rand_pick[1] == "area":
                        solution = "The area of a circle is equal to \(\pi\).\(\r^2\)"
                    else:
                        solution = "The perimeter of a circle is equal to 2\(\pi\).r"
                    question = "The {} of a {} is {}. What is its radius ?".format(rand_pick[1],random.choice(shape_subs["circle"]),round(rand_pick[0],2))
                    answer = circle.r
                    options = make_wrong_options(answer)
                elif shape_trigger == 1:
                   rectangle = make_shape(shape_trigger)
                   random.seed()
                   question = "The surface area of a {} is {}, and its perimeter is {}. What are its dimensions?".format(random.choice(shape_subs["rectangle"]),rectangle.area,rectangle.peri)
                   answer = "{},{}".format(rectangle.l,rectangle.b)
                   solution = "The perimeter of a rectangle is 2(l+b), and the area is lxb.\n Thus the two equations we get are: \n {} = 2(l+b) ---- 1 \n {} = l.b ---- 2 \n On solving these, we get l = {}, b = {}".format(rectangle.peri,rectangle.area,rectangle.l,rectangle.b)
                   options = []
                   while len(options)<3:
                       random.seed()
                       offset = random.randint(2,8)
                       random.seed()
                       wr_len = random.randint(rectangle.l - offset, rectangle.l + offset)
                       random.seed()
                       offset = random.randint(2,8)
                       random.seed()
                       wr_bre = random.randint(rectangle.b - offset, rectangle.b + offset)
                       wr_ans = "{},{}".format(wr_len,wr_bre)
                       if wr_bre != rectangle.b or wr_len != rectangle.l:
                           if wr_ans not in options:
                               options.append(wr_ans)
                elif shape_trigger == 2:
                    square = make_shape(shape_trigger)
                    area = [square.area, "area"]
                    perimeter = [square.peri, "perimeter"]
                    random.seed()
                    rand_pick = random.choice([area,perimeter])
                    if rand_pick[1] == "area":
                        solution = "The area of a square is \(\a^2\), where a is the side length of the square. \n Thus a = \(\sqrt{area}\)."
                    else:
                        solution = "The perimeter of a square is 4.a , where a is the side length of the square. \n Thus a = \(\frac{perimeter}{4})"
                    question = "The {} of a square is {}. What is the length of its side?".format(rand_pick[1],rand_pick[0])
                    answer = square.l
                    options = make_wrong_options(answer)
            elif attribute_trigger == 1:
                if shape_trigger == 0:
                    circle = make_shape(shape_trigger)
                    random.seed()
                    rand_att = random.choice(["area", "perimeter"])
                    random.seed()
                    if rand_att == "area":
                        solution = "The area of a circle is equal to \(\pi\).\(\r^2\)"
                    else:
                        solution = "The perimeter of a circle is equal to 2\(\pi\).r"
                    question = "The radius of a {} is {}. What is its {}?".format(random.choice(shape_subs["circle"]),circle.r,rand_att)
                    if rand_att == "area":
                        answer = round(circle.area,2)
                    else:
                        answer = round(circle.peri,2)
                    options = make_wrong_options(answer)
                elif shape_trigger == 1:
                    rectangle = make_shape(shape_trigger)
                    random.seed()
                    rand_att = random.choice(["area", "perimeter"])
                    random.seed()
                    if rand_att == "perimeter":
                        solution = "The perimeter of a rectangle is given by P =  2.(l+b)."
                    else:
                        solution = "The area of a rectangle is given by A =  l.b."
                    question = "The dimensions of a {} are {} and {}. What is its {}?".format(random.choice(shape_subs["rectangle"]),rectangle.l,rectangle.b, rand_att)
                    if rand_att == "area":
                        answer = rectangle.area
                    else:
                        answer = rectangle.peri
                    options = make_wrong_options(answer)
                elif shape_trigger == 2:
                    square = make_shape(shape_trigger)
                    random.seed()
                    rand_att = random.choice(["area", "perimeter"])
                    if rand_att == "perimeter":
                        solution = "The perimeter of a square is given by P =  4.a ."
                    else:
                        solution = "The area of a square is given by A = \(\a^2\)"
                    question = "The side length of a square is {}. What is its {}?".format(square.l, rand_att)
                    if rand_att == "area":
                        answer = square.area
                    else:
                        answer = square.peri
                    options = make_wrong_options(answer)
        self.add_question(question,answer,options,solution)
        
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
        q.make_questions()
        print("Made {} questions".format(i + 1))
    q.save_questions()

if __name__ == "__main__":
    main()



