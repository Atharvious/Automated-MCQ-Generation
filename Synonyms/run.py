from Synonym import Generator
from sys import argv, exit
gen = Generator("Questions")

def main():
    if len(argv) < 2:
        print("Please enter number of questions for file %s" % argv[0])
        exit(1)
    num_questions = argv[1]
    gen.run(int(num_questions))
    
    
if __name__ == "__main__":
    main()