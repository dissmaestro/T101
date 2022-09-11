from copy import deepcopy
from random import choice, shuffle, randint
from time import time
from typing import List

def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and","or","not"]):
	rules = []
	for j in range(0, n_generate):

	    log_oper = choice(log_oper_choice)  #not means and-not (neither)
	    if n_max < 2:
		    n_max = 2
	    n_items = randint(2,n_max)
	    items = []
	    for i in range(0,n_items):
		    items.append( randint(1,code_max) )
	    rule = {
	          'if':{
	              log_oper:	 items
	           },
	           'then':code_max+j
	        }
	    rules.append(rule)
	shuffle(rules)
	return(rules)

def generate_stairway_rules(code_max, n_max, n_generate, log_oper_choice=["and","or","not"]):
	rules = []
	for j in range(0, n_generate):

	    log_oper = choice(log_oper_choice)  #not means and-not (neither)
	    if n_max < 2:
		    n_max = 2
	    n_items = randint(2,n_max)
	    items = []
	    for i in range(0,n_items):
		    items.append( i+j )
	    rule = {
	          'if':{
	              log_oper:	 items
	           },
	           'then':i+j+1
	        }
	    rules.append(rule)
	shuffle(rules)
	return(rules)

def generate_ring_rules(code_max, n_max, n_generate, log_oper_choice=["and","or","not"]):
	rules = generate_stairway_rules(code_max, n_max, n_generate -1, log_oper_choice)
	log_oper = choice(log_oper_choice)  #not means and-not (neither)
	if n_max < 2:
	    n_max = 2
	n_items = randint(2,n_max)
	items = []
	for i in range(0,n_items):
	    items.append( code_max-i )
	rule = {
	       'if':{
	          log_oper:	 items
	       },
	       'then':0
	       }
	rules.append(rule)
	shuffle(rules)
	return(rules)

def generate_random_rules(code_max, n_max, n_generate, log_oper_choice=["and","or","not"]):
	rules = []
	for j in range(0, n_generate):

	    log_oper = choice(log_oper_choice)  #not means and-not (neither)
	    if n_max < 2:
		    n_max = 2
	    n_items = randint(2,n_max)
	    items = []
	    for i in range(0,n_items):
		    items.append( randint(1,code_max) )
	    rule = {
	          'if':{
	              log_oper:	 items
	           },
	           'then':randint(1,code_max)
	        }
	    rules.append(rule)
	shuffle(rules)
	return(rules)

def generate_seq_facts(M):
	facts = list(range(0,M))
	shuffle(facts)
	return facts

def generate_rand_facts(code_max, M):
	facts = []
	for i in range(0,M):
		facts.append( randint(0, code_max) )
	return facts


#samples:
#print(generate_simple_rules(100, 4, 10))
random_rules = generate_random_rules(100, 4, 10)
#print(generate_stairway_rules(100, 4, 10, ["or"]))
#print(generate_ring_rules(100, 4, 10, ["or"]))

#generate rules and facts and check time
time_start = time()
N = 100000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print("%d rules generated in %f seconds" % (N,time()-time_start))

#load and validate rules
# YOUR CODE HERE
print(facts)
#check facts vs rules
time_start = time()

def check_items_with_not_operation(fact:int ,items:List[int]):
    if fact in items:
        return False
    return True

def check_items_with_and_operation(fact:int,items:List[int]):
    if fact in items and items.count(fact) == 3:
        return True
    return False

def check_items_with_or_operation(fact:int , items:List[int]):
    if fact in items and items.count(fact) != 3:
        return True
    return False


def validate_facts_and_rules(rules:List, facts:List[int]):
    rules_facts = list()
    for rule in rules:
        for key , value in rule.items():
            if isinstance(value,dict):
                for operation , numbers in value.items():
                    oper = operation
                    items = numbers
                break
        for fact in facts:
            if oper == 'not':
                result = check_items_with_not_operation(fact=fact,items=items)
            elif oper == 'and':
                result = check_items_with_and_operation(fact=fact,items=items)
            else:
                result = check_items_with_or_operation(fact=fact , items=items)
            rules_facts.append((rule,fact,result))
    return rules_facts

def check_mutual_exclusion(rules_facts:List , results:List):
    copy_rules_facts = deepcopy(rules_facts)
    for rule_fact in copy_rules_facts:
        index = copy_rules_facts.index(rule_fact)
        value_result = results[index]
        rules_facts.remove(rule_fact)
        del results[index]
        while rule_fact in rules_facts:
            equal_index_rule_fact = rules_facts.index(rule_fact)
            equal_rule_fact = rules_facts[equal_index_rule_fact]
            if value_result != results[equal_index_rule_fact]:
                rules_facts.remove(equal_rule_fact)
                del results[equal_index_rule_fact]
    return rules_facts





# YOUR CODE HERE

print("%d facts validated vs %d rules in %f seconds" % (M,N,time()-time_start))
result_facts = validate_facts_and_rules(rules=random_rules,facts=facts)
print(*result_facts,sep='\n')