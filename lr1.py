rom random import choice, shuffle, randint
from time import time

def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
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

def generate_seq_facts(M):
	facts = list(range(0,M))
	shuffle(facts)
	return facts

def generate_rand_facts(code_max, M):
	facts = []
	for i in range(0,M):
		facts.append( randint(0, code_max) )
	return facts


def results(facts, rules):
    """
        This function returns new rules!
        Args:
             List of facts and statements
        Returns:
             New rules
        """
    fact = set(facts)
    interim_results = []
    for i in rules:
        for j in i['if']:
            if j == 'or':
                for atr in i['if'][j]:
                    # if a in facts:
                    if atr in fact:
                        # interim_results.append([facts,i['then']])
                        if len(interim_results) == 0:
                            fac = facts.copy()
                            interim_results.append({'if': fac, 'or': i['if'][j],
                                                    'then': i['then']})
                            facts.append(i['then'])
                            fact.add(i['then'])
                            break
                        else:
                            put = True
                            for mer in interim_results:
                                if 'or' in mer:
                                    if (mer['or'] == i['if'][j] and mer['then'] != i['then']) or (
                                            mer['or'] != i['if'][j] and mer['then'] == i['then']):
                                        put = False
                                        break
                                if 'and' in mer:
                                    if (mer['and'] == i['if'][j]) and (mer['then'] != i['then']):
                                        put = False
                                        break
                            if put is True:
                                fac = facts.copy()
                                interim_results.append({'if': fac, 'or': i['if'][j],
                                                        'then': i['then']})
                                facts.append(i['then'])
                                fact.add(i['then'])
            if j == 'and':
                count = len(i['if'][j])
                counter = 0
                for atr in i['if'][j]:
                    # if a in facts:
                    if atr in fact:
                        counter = counter + 1
                    else:
                        break
                if counter == count:
                    # interim_results.append([facts,i['then']])
                    if len(interim_results) == 0:
                        fac = facts.copy()
                        interim_results.append({'if': fac, 'and': i['if'][j], 'then': i['then']})
                        facts.append(i['then'])
                        fact.add(i['then'])
                    else:
                        put = True
                        for mer in interim_results:
                            if 'and' in mer:
                                if (mer['and'] == i['if'][j] and mer['then'] != i['then']) or (
                                        mer['and'] != i['if'][j] and mer['then'] == i['then']):
                                    put = False
                                    break
                        if put is True:
                            fac = facts.copy()
                            interim_results.append({'if': fac, 'and': i['if'][j],
                                                    'then': i['then']})
                            facts.append(i['then'])
                            fact.add(i['then'])

            if j == 'not':
                count = len(i['if'][j])
                counter = 0
                for atr in i['if'][j]:
                    # if a not in facts:
                    if atr not in fact:
                        counter = counter + 1
                    else:
                        break
                if counter == count:
                    # interim_results.append([facts,i['then']])
                    if len(interim_results) == 0:
                        fac = facts.copy()
                        interim_results.append({'if': fac, 'not': i['if'][j], 'then': i['then']})
                        facts.append(i['then'])
                        fact.add(i['then'])
                    else:
                        put = True
                        for mer in interim_results:
                            if 'not' in mer:
                                if (mer['not'] == i['if'][j] and mer['then'] != i['then']) or (
                                        mer['not'] != i['if'][j] and mer['then'] == i['then']):
                                    put = False
                                    break
                        if put is True:
                            fac = facts.copy()
                            interim_results.append({'if': fac, 'not': i['if'][j], 'then': i['then']})
                            facts.append(i['then'])
                            fact.add(i['then'])

    return interim_results


time_start = time()
#N = 100000
#M = 1000
rules = generate_simple_rules(100, 4, 10000)
#print(rules,'\n')
facts = generate_rand_facts(100, 1000)
print("%d rules generated in %f seconds" % (1000,time()-time_start))
#print(facts,'\n')
time_start = time()
in_res = results(facts, rules)
rez = time()-time_start
#print(rez)
#print(in_res,'\n')
print("%d facts validated vs %d rules in %f seconds" % (1000,10000,rez))
