from fractions import Fraction
from sympy import *
import sympy as sp
from sympy.abc import x,y,k
import random
import pandas as pd
from sys import argv, exit

from sympy import init_printing
init_printing()

class Equation_Parser:
    def __init__(self,a,b,c):
        self.ex = Eq(a*x+b*y,c)
        self.lat = sp.latex(self.ex)
        self.kay = random.choice([a,b,c])
        if self.kay == a:
            self.dummy = sp.latex(Eq(k*x + b*y,c))
        elif self.kay == b:
            self.dummy = sp.latex(Eq(a*x + k*y,c))
        else:
            self.dummy = sp.latex(Eq(a*x + b*y,k))
            
def check_sols(cofs1,cofs2):
    a1,b1,c1 = cofs1
    a2,b2,c2 = cofs2
    if a1/a2 == b1/b2 and b1/b2 == c1/c2:
        return 2
    elif a1/a2 == b1/b2 and b1/b2 != c1/c2:
        return 1
    elif a1/a2 != b1/b2:
        return 0

def solve_eq(cofs1,cofs2):
    
    a1,b1,c1 = cofs1
    a2,b2,c2 = cofs2
    
    def det(a1,b1,a2,b2):
        return b2*a1 - a2*b1
    
    D = det(a1,b1,a2,b2)
    Dx = det(c1,b1,c2,b2)
    Dy = det(a1,c1,a2,c2)
    
    return (Fraction(round(Dx/D,2)).limit_denominator(100),Fraction(round(Dy/D,2)).limit_denominator(100))

def make_eq(sol_type):
    if sol_type == 0:
        i = 0 
        #Distinct solution
        while i == 0:
            random.seed()
            a1 = random.randint(-17,17)
            random.seed()
            a2 = random.randint(-17,17)
            if a2 == 0:
                a1 += 1
            random.seed()
            b1 = random.randint(-17,17)
            random.seed()
            b2 = random.randint(-17,17)
            if b2 == 0:
                b2 += 1
            random.seed()
            c1 = random.randint(-17,17)
            random.seed()
            c2 = random.randint(-17,17)
            if c2 == 0:
                c2 += 1
            if check_sols([a1,b1,c1],[a2,b2,c2]) == sol_type:
                i = 1
                return ([a1,b1,c1],[a2,b2,c2])
    elif sol_type == 1:
        i = 0
        #No solution
        while i == 0:
            random.seed()
            a1 = random.randint(-17,17)
            if a1 == 0:
                a1   += 1
            random.seed()
            b1 = random.randint(-17,17)
            if b1 == 0:
                b1 += 1
            random.seed()
            scale = random.randint(-5,5)
            if scale == 0 or scale == 1:
                scale +=2
            a2 = a1*scale
            b2 = b1*scale
            random.seed()
            c1 = random.randint(-17,17)
            random.seed()
            c2 = random.randint(-17,17)
            if c2 == 0:
                c2 += 1
            if check_sols([a1,b1,c1],[a2,b2,c2]) == sol_type:
                i = 1
                return ([a1,b1,c1],[a2,b2,c2])
    elif sol_type == 2:
        i = 0
        while i == 0:
            random.seed()
            a1 = random.randint(-17,17)
            if a1 == 0:
                a1 += 1
            random.seed()
            b1 = random.randint(-17,17)
            if b1 == 0:
                b1 += 1
            random.seed()
            c1 = random.randint(-17,17)
            if c1 == 0:
                c1 += 1
            random.seed()
            scale = random.randint(-5,5)
            if scale == 1 or scale == 0:
                scale+=2
            a2 = a1*scale
            b2 = b1*scale
            c2 = c1*scale
            if check_sols([a1,b1,c1],[a2,b2,c2]) == sol_type:
                i = 1
                return ([a1,b1,c1],[a2,b2,c2])
            
          
coffs = make_eq(0)

""" Types of questions:
    1 - solve the given system of equations.
    2 - solution type of given system of equation. (whether the lines forms by the given equations intersect
                                                       or parallel or coincident)
    3 - select value of k for which the given system has 'this' type of solution.
"""   
class Question:
    def __init__(self):
        self.quest_dict = {
                "Question":[],
                "Option1":[],
                "Option2":[],
                "Option3":[],
                "Option4":[],
                "Answer":[],}
        self.quest_types = ["Solve", "Sol_type", "Select value"]
        
    def get_options(self,solution_tup):
        x = solution_tup[0]
        y = solution_tup[1]
        options = []
        random.seed()
        while len(options)<3:
            random.seed()
            offset = random.randint(5,11)
            random.seed()
            wr_x = Fraction(random.uniform(int(x) - offset, int(x) + offset)).limit_denominator(100)
            random.seed()
            offset = random.randint(5,11)
            random.seed()
            wr_y = Fraction(random.uniform(int(y) - offset, int(y) + offset)).limit_denominator(100)
            if wr_x != x or wr_y != y:
                wrong_ans = "x = {}, y = {}".format(wr_x,wr_y)
                if wrong_ans not in options:
                    options.append(wrong_ans)
        return options
        
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
        random.seed()
        quest_type = random.choice(self.quest_types)
        if quest_type == "Solve":
            eqn = make_eq(0)
            l1,l2 = eqn
            eq1 = Equation_Parser(l1[0],l1[1],l1[2])
            eq2 = Equation_Parser(l2[0],l2[1],l2[2])
            question = "For the given pair of equations {} and {} ,the values of x and y that satisfy both of them are:".format(eq1.lat,eq2.lat)
            solution = solve_eq(l1,l2)
            answer = "x = {}, y = {}".format(solution[0],solution[1])
            options = self.get_options(solution)
        elif quest_type == "Sol_type":
            sol_type_dict = {
                    "0":["One Solution","Intersect"],
                    "1": ["No Solution", "are Parallel"],
                    "2": ["Infinitely many Solutions","are Co-incident"]}
            random.seed()
            sol_graph_flag = random.randint(0,1)
            random.seed()
            solution_type = random.randint(0,2)
            l1,l2 = make_eq(solution_type)
            eq1 = Equation_Parser(l1[0],l1[1],l1[2])
            eq2 = Equation_Parser(l2[0],l2[1],l2[2])            
            if sol_graph_flag == 0:
                question = "The given pair of equations {} and {} have:".format(eq1.lat, eq2.lat)
                options = ["Two Solutions"]
                        
            elif sol_graph_flag ==1:
                question = "If we plot the given pair of equations {} and {} on a graph, the lines:".format(eq1.lat,eq2.lat)
                options = ["None of the above"]
        
            answer = sol_type_dict[str(solution_type)][sol_graph_flag]
            i = 0
            while len(options)<3:
                option = sol_type_dict[str(i)][sol_graph_flag]
                if option != answer:
                    options.append(option)
                i += 1
                    
        elif quest_type == "Select value":
            sol_type_dict = {
                    "0":["One Solution","Intersect"],
                    "1": ["No Solution", "are Parallel"],
                    "2": ["Infinitely many Solutions","are Co-incident"]}
            random.seed()
            eq_line = random.randint(0,1)
            random.seed()
            solution_type = random.randint(1,2)
            l1,l2 = make_eq(solution_type)
            eq1 = Equation_Parser(l1[0],l1[1],l1[2])
            eq2 = Equation_Parser(l2[0],l2[1],l2[2])
            random.seed()
            if eq_line == 0:
                question = "Find the value of k for which the given equations {} and {} have {}".format(eq1.lat,eq2.dummy,sol_type_dict[str(solution_type)][eq_line])
            else:
                question = "Find the value of k for which the lines given by the equations {} and {} {}.".format(eq1.lat,eq2.dummy,sol_type_dict[str(solution_type)][eq_line])
            answer = eq2.kay
            options = []
            while len(options)<3:
                random.seed()
                offset = random.randint(3,9)
                random.seed()
                wrong_ans = random.randint(answer - offset,answer+offset)
                if wrong_ans != answer and wrong_ans not in options:
                    options.append(wrong_ans)
                    
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
        print("Made {} questions.".format(i+1))
    q.save_questions()



if __name__ == "__main__":
    main()

