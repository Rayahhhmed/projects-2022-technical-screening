"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: This challenge is EXTREMELY hard and we are not expecting anyone to pass all
our tests. In fact, we are not expecting many people to even attempt this.
For complete transparency, this is worth more than the easy challenge. 
A good solution is favourable but does not guarantee a spot in Projects because
we will also consider many other criteria.
"""
import json
import re 

MONOSPACE = ' '
COURSE_CODE_RANGE = 4
LOGIC_OPERATIONS = ["AND", "OR"]
LB = '('
RB = ')'
# NOTE: DO NOT EDIT conditions.json
with open("screening_for_subcom\projects-2022-technical-screening\conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit"""

    """The design for checking if a person has done a particular source would be done with
    lists. Think of it like a decision tree."""

    unparsed_string = CONDITIONS
    # need to check if there were no courses inputted 
    # not sure if there would be a case where target course not given
    handle_trivial_cases(courses_list, target_course)
    print(CONDITIONS[target_course].split())
     
    # delimit string to list 
    monospaced_prerequisites = MONOSPACE.join(CONDITIONS[target_course].split())
    if len(monospaced_prerequisites) == 1:
        return monospaced_prerequisites in courses_list
    
    construct_course_progressions(0, monospaced_prerequisites)
    



def handle_trivial_cases(courses_list, target_course):    
    """need to amortise for trivial cases"""
    if len(courses_list) == 0:
        return False

def check_if_valid_course_name(course_name):
    """ This will check for the last 4 digits of a course name"""
    course_is_valid = True
    name_len = len(course_name)
    for x in range(1, COURSE_CODE_RANGE):
        if course_name[name_len - x].isnumeric() is False: 
            course_is_valid = False 
    return course_is_valid


def check_subsequent_course_key_with_bracket(lo, monospaced_prerequisites):
    count_brackets = 0
    temp_list = []
    for x in range(lo, len(monospaced_prerequisites) - 1):
        count_brackets += monospaced_prerequisites[x].count(LB)
        count_brackets -= monospaced_prerequisites[x].count(RB)
        monospaced_prerequisites[x].split()
        monospaced_prerequisites[x].remove(LB)
        monospaced_prerequisites[x].remove(RB)
        temp_list.append(monospaced_prerequisites[x])
        if count_brackets is 0:
            return temp_list
        

def construct_course_progressions(lo, monospaced_prerequisites):

    for index in range(lo, len(monospaced_prerequisites) - 1):
        course_name = monospaced_prerequisites[index]
        if LB or RB in course_name:
            check_subsequent_course_key_with_bracket(index, monospaced_prerequisites)
        # Check if the thing has The operators or course codes
        if course_name in LOGIC_OPERATIONS: 
            if course_name is "AND":
                "check if previous course name is a list or string"
               # if type(monospaced_prerequisites[index - 1]) is str: 
                pass
            else: 
                "the code here is an \"OR\" "
                monospaced_prerequisites.remove(course_name)

                if type(monospaced_prerequisites[index - 1]) is str:
                    temp_list = []
                    temp_list.append(monospaced_prerequisites[index - 1])
                    temp_list.append(monospaced_prerequisites[index])
                    monospaced_prerequisites[index - 1] = temp_list
                else: 
                     monospaced_prerequisites[index - 1].append(course_name) 
        elif check_if_valid_course_name(course_name) == False:
            print("Course name bad!")
            




if __name__ == '__main__':  
    print(is_unlocked(["COMP1531 AND (COMP2521 OR COMP1927)"], "COMP2511"))

