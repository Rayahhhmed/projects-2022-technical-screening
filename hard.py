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
from os import name
import re 

"Constants and definitions"
MONOSPACE = ' '
COURSE_CODE_RANGE = 4
LOGIC_OPERATIONS = ["AND", "OR"]
LB = '('
RB = ')'
UNITS_OF_CREDIT = 6
NO_CASE_FLAG = 0x0F

# NOTE: DO NOT EDIT conditions.json
with open("screening_for_subcom\projects-2022-technical-screening\conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()


class DegreeTree: 
    def __init__(self, course_name):
        self.name = course_name
        self.uoc = UNITS_OF_CREDIT
        index_of_course_code = len(course_name) - COURSE_CODE_RANGE
        self.level_of_course = course_name[index_of_course_code]
        self.children = []
        self.parent = self
        
    def add_child(self, child):
        child.parent = self 
        self.children.append(child) 

    def remove_child(self, child):
        self.children.remove(child)

    def get_children_courses(self):
        return self.children

    def print_tree_bfs(self):
        queue = [self]
        while queue: 
            course_inspected = queue.pop(0)
            print(course_inspected.name + " ")
            for child_course in course_inspected.children:
                if child_course:
                    queue.append(child_course)

def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit"""

    """The design for checking if a person has done a particular source would be done with
    lists. Think of it like a decision tree."""
    # need to check if there were no courses inputted 
    # not sure if there would be a case where target course not given
    

    # delimit string to list 
    CONDITIONS[target_course] = CONDITIONS[target_course].replace('.', '').replace(',', " OR").replace('.', '').upper()
    #monospaced_prerequisites = MONOSPACE.join(CONDITIONS[target_course].split())
    monospaced_prerequisites = CONDITIONS[target_course].split()
    """ Amortising for trivial cases: 
        NOTE: Handles cases where: 
                - No course codes are provided
                - Only one prerequisite
                - no course prereqs"""

    flag_value = handle_trivial_cases(courses_list, target_course, monospaced_prerequisites)
    if flag_value is not NO_CASE_FLAG: 
        return flag_value
    
    #todo remove: 
    print(monospaced_prerequisites)

    
    parent_course_node = DegreeTree(target_course)
   
    # Telling it basically to start the degree progression list from the start
    # with the string which is spliced to be neater. 

    construct_course_progressions(parent_course_node, monospaced_prerequisites)

    parent_course_node.print_tree_bfs()

    return check_if_course_can_be_done(parent_course_node, courses_list, target_course, False)


def handle_trivial_cases(courses_list, target_course, monospaced_prerequisites):    
    """need to amortise for trivial cases"""
    if len(courses_list) == 0:
        return False
    if len(monospaced_prerequisites) == 1 and target_course == "COMP1511":
        return monospaced_prerequisites in courses_list
    if len(monospaced_prerequisites) == 0: 
        # Empty prereqs
        return True
    else: 
        return NO_CASE_FLAG


def check_if_valid_course_name(course_name):
    """ This will check for the last 4 digits of a course name"""
    course_is_valid = True
    name_len = len(course_name)
    for x in range(1, COURSE_CODE_RANGE):
        if course_name[name_len - x].isnumeric() is False: 
            course_is_valid = False  
    if name_len <= 4: return False

    return course_is_valid


def check_subsequent_course_key_with_bracket(lo, monospaced_prerequisites):
    count_brackets = 0
    temp_list = []
    for x in range(lo, len(monospaced_prerequisites) - 1):
        count_brackets += monospaced_prerequisites[x].count(LB)
        count_brackets -= monospaced_prerequisites[x].count(RB)
        monospaced_prerequisites[x].split()
        monospaced_prerequisites[x].replace(LB, '')
        monospaced_prerequisites[x].replace(RB, '')
        temp_list.append(monospaced_prerequisites[x])
        if count_brackets == 0:
            return temp_list
        
def check_if_course_can_be_done (degree_tree, courses_done, target_course, bool_course_dfs_found):
    print(courses_done, target_course)
    if bool_course_dfs_found is True or not degree_tree.get_children_courses(): 
        return True
    
    for course_child in degree_tree.get_children_courses(): 
        if course_child.name in courses_done:
            bool_course_dfs_found = check_if_course_can_be_done(course_child, 
                                                                courses_done, 
                                                                target_course, bool_course_dfs_found)

    return bool_course_dfs_found
def construct_course_progressions(parent_course_node, monospaced_prerequisites):
    
    for token in monospaced_prerequisites:
        if LB in token or RB in token:
           # new_sub_list = get_new_course_list_within_brackets(token, monospaced_prerequisites)
            pass
        # Check if the thing has The operators or course codes
        
        if token in LOGIC_OPERATIONS:
            if token == "AND":
                monospaced_prerequisites.remove(token)
                for courses_preceding in monospaced_prerequisites:
                    if courses_preceding in parent_course_node.get_children():
                        construct_course_progressions(courses_preceding, monospaced_prerequisites)
            elif token == "OR": 
                "the code here is an \"OR\" "
                monospaced_prerequisites.remove(token)
                construct_course_progressions(parent_course_node.parent, monospaced_prerequisites)
        course_name_validity = check_if_valid_course_name(token)
        if course_name_validity == True:
            parent_course_node.add_child(DegreeTree(token))
            monospaced_prerequisites.remove(token)
        elif len(token) == COURSE_CODE_RANGE and token.isnumeric():
            token = "COMP" + token
            parent_course_node.children.append(DegreeTree(token))
                

if __name__ == '__main__':  
    print(is_unlocked(["COMP7777", "COMP4951"], "COMP4952"))
