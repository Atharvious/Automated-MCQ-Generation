import pandas as pd
import random
class AP:
    def __init__(self, first_term,common_difference):
        self.a = first_term
        self.d = common_difference

    def nth_term(self,n):
        return self.a + (n-1)*self.d
    
    def sum_n(self,n):
        return (n/2)*(self.a + self.nth_term(n))
    
    def print_ap(self,n):
        terms = []
        for x in range(n):
            terms.append(str(self.a + x*self.d))
        ap = ",".join(terms)
        #print(ap)
        return terms
        
    def is_member(self,x):
        if self.d == 0:
            return self.a == x
        else:
            return ((x - self.a) % self.d == 0 and int(x- self.a)/self.d >= 0)

def random_ap():
    random.seed()
    a = random.randint(12,16)
    random.seed()
    d = random.randint(3,14)
    return AP(a,d)

rand_ap = random_ap()

rand_ap.print_ap(10)


def rand_question(trigger):
    random.seed()
    ap = random_ap()
    if trigger == 0:
        question = "The first term of the series is {} and the common difference is {}. Which of the following can be of this sequence?".format(ap.a,ap.d)
        random.seed()
        seq_len = random.randint(1,3)
        rand_elem = random.randint(5,13)
        answer = [str(ap.nth_term(rand_elem))]
        for i in range(seq_len-1):
            answer.append(str(ap.nth_term(rand_elem+i+1)))
        answer_string = ",".join(answer)
        solution = "Out of the given options, only {} is a term sequence for the ap with a = {} and d = {}".format(answer_string,ap.a,ap.d)
        options  = []
        while len(options) < 3:
            random.seed()
            offset = random.randint(5,20)
            random.seed()
            rand_no = random.randint(ap.nth_term(rand_elem) - offset , ap.nth_term(rand_elem) + offset)
            if rand_no != ap.nth_term(rand_elem):
                option = [str(rand_no)]
                for i in range(seq_len-1):
                    random.seed()
                    next_no = rand_no +  random.randint(ap.d - random.randint(3,5), ap.d + random.randint(3,5))
                    option.append(str(next_no))
                options.append(option)
        options_list = []
        for option in options:
            options_list.append(",".join(option))
            
    elif trigger == 1:
        question = "Select the series having common difference {}.".format(ap.d)
        answer = ap.print_ap(3)
        answer_string = ",".join(answer)
        options_list = []
        while len(options_list) < 3:
            wrong_ap = random_ap()
            if wrong_ap.d != ap.d:
                option = ",".join(wrong_ap.print_ap(3))
                if option not in options_list:
                    options_list.append(option)
        solution = "In an AP, d = differnece between consecutive terms. The only AP with d = {} is {}...".format(ap.d,",".join(ap.print_ap(3)))
    
    elif trigger == 2:
        random.seed()
        what_to_find = random.randint(0,1)
        random.seed()
        which_term = random.randint(8,14) 
        if what_to_find == 0:
            answer = ap.nth_term(which_term)
            wtf_str = "{}th term.".format(which_term)
            solution = "The nth term of an AP is calculated by Tn = a + (n-1)d."
        else:
            answer = ap.sum_n(which_term)
            wtf_str = "sum of first {} terms.".format(which_term)
            solution = "The sum of first n terms in an AP is calculated using the formula Sn = \frac{n}{2}*(2a + (n-1)d)"
            
        answer_string = str(answer)
        options_list = []
        while len(options_list) < 3:
            random.seed()
            wrong_answer = str(random.randint(answer - random.randint(4,12), answer + random.randint(4,12)))
            if int(wrong_answer) != answer and wrong_answer not in options_list:
                options_list.append(wrong_answer)
        question = "If the first term of a series is {} and the common difference is {}, find the {}".format(ap.a,ap.d,wtf_str)
        
    elif trigger == 3:
        random.seed()
        series_num = random.randint(3,5)
        question = "What is the common difference of the series - {}".format(",".join(ap.print_ap(series_num)))
        answer = ap.d
        solution = "The difference between consecutive terms is the common difference of an AP."
        answer_string = str(answer)
        options_list = []
        while len(options_list) < 3:
            random.seed()
            wrong_answer = str(random.randint(answer - random.randint(4,12), answer + random.randint(4,12)))
            if int(wrong_answer) != answer and wrong_answer not in options_list and int(wrong_answer)>0:
                options_list.append(wrong_answer)
                
    elif trigger == 4:
        random.seed()
        which_term = random.randint(4,15)
        random.seed()
        offset = random.randint(1,4)
        answer = ap.a
        answer_string = str(answer)
        solution = "The nth term of an AP is given as : Tn = a + (n-1)d. \n Thus the two equations we get are: \n {} = a + ({}-1)d ---- 1 \n {} = a + ({}-1)d ---- 2 \n Solving both the equations, we get a = {}.".format(ap.nth_term(which_term),which_term,ap.nth_term(which_term+ offset), which_term+offset, ap.a)
        question = "If the {}th term of a series is {} and the {}th term of the series is {}, what is the first term?".format(which_term,ap.nth_term(which_term),which_term + offset,ap.nth_term(which_term + offset ))
        options_list = []
        while len(options_list) < 3:
            random.seed()
            wrong_answer = str(random.randint(answer - random.randint(4,12), answer + random.randint(4,12)))
            if int(wrong_answer) != answer and wrong_answer not in options_list and int(wrong_answer)>0:
                options_list.append(wrong_answer)
    
    elif trigger == 5:
        random.seed()
        correct_flag = random.randint(0,1)
        if correct_flag == 1:
            offset = 0
            answer_string = "Yes"
        else:
            random.seed()
            offset = random.randint(1, ap.d - 1)
            answer_string = "No"
        n = random.randint(20,30)
        question = "Is {} a term in the ap {}... ?".format(ap.nth_term(n + offset),",".join(ap.print_ap(4)))
        if answer_string == "Yes":
            options_list = ["No", "Maybe", "Can't say"]
        elif answer_string == "No":
            options_list = ["Yes", "Maybe", "Can't say"]
        solution = ("To find if a number is in a given AP, we check if the difference between the number and first term(a) is a multiple of the common difference (d) or not.")
    return question, answer_string, options_list, solution
    
    
        
def generate_questions(num_questions = 1):
    quest_dict = {
            "Question":[],
            "Option1": [],
            "Option2": [],
            "Option3": [],
            "Option4": [],
            "Answer":  [],
            "Solution": []
            }
    for number in range(num_questions):
        random.seed()
        trigger = random.randint(0,5)
        quest, answer, options, solution = rand_question(trigger)
        quest_dict["Question"].append(quest)
        quest_dict["Solution"].append(solution)
        opts = ["Option1","Option2", "Option3", "Option4"]
        random.seed()
        right_op = random.choice(opts)
        quest_dict[right_op].append(answer)
        quest_dict["Answer"].append(right_op)
        rem_opts = opts[:]
        rem_opts.remove(right_op)
        for opt,option in zip(rem_opts,options):
            quest_dict[opt].append(option)
    df = pd.DataFrame(quest_dict)
    df.to_csv("Questions.csv")

         
generate_questions(20)            
            
            
            
            
            
            
            
            
                 
            
            
        
        
        
        
        