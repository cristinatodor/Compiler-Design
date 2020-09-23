import sys
import os 
import nltk
from nltk.tree import Tree
from nltk.draw.tree import TreeView

path = os.getcwd()

# log file 
g = open("parser.log", "a")

variables = []
constants = []
predicates = {}
equality = []
connectives = []
quantifiers = []

input_formula_list = []
input_formula = ""

# If input file is not specified, example1.txt is set as default 
file_name = "example1.txt"
if len(sys.argv) > 1:
    file_name = sys.argv[1]

g.write("\nInput file is: ")
g.write(file_name)

# Read from file
f = open(file_name, "r")
Lines = f.readlines()

i = 0
while i < len(Lines):
    line = Lines[i]
    
    if line.startswith("variables"):  
        '''
        if i != len(Lines)-1 and (not Lines[i+1].startswith("constants")) and (not Lines[i+1].startswith("predicates")) and (not Lines[i+1].startswith("equality")) and (not Lines[i+1].startswith("connectives")) and (not Lines[i+1].startswith("quantifiers")) and (not Lines[i+1].startswith("formula")):
            line += Lines[i+1]
            print(line)
            i += 1 
        '''
        line = line[len("variables")+2:]   
        aux = ""
        for char in line:
            if char != ' ' and char != '\n':
                aux += char
            else:
                variables.append(aux)
                aux = "" 

    if line.startswith("constants"):  
        '''
        if i != len(Lines)-1 and (not Lines[i+1].startswith("variables")) and (not Lines[i+1].startswith("predicates")) and (not Lines[i+1].startswith("equality")) and (not Lines[i+1].startswith("connectives")) and (not Lines[i+1].startswith("quantifiers")) and (not Lines[i+1].startswith("formula")):
            line += Lines[i+1]
            print(line)
            i += 1 
        '''
        line = line[len("constants")+2:]   
        aux = ""
        for char in line:
            if char != ' ' and char != '\n':
                aux += char
            else:
                constants.append(aux)
                aux = "" 

    if line.startswith("predicates"): 
        '''
        if i != len(Lines)-1 and (not Lines[i+1].startswith("variables")) and (not Lines[i+1].startswith("constants")) and (not Lines[i+1].startswith("equality")) and (not Lines[i+1].startswith("connectives")) and (not Lines[i+1].startswith("quantifiers")) and (not Lines[i+1].startswith("formula")):
            line += Lines[i+1]
            print(line)
            i += 1 
        '''
        line = line[len("predicates")+2:]   
        aux = ""
        for char in line:
            if char != ' ' and char != '\n':
                if not char.isdigit() and char != '[' and char != ']':
                    aux += char 
                elif char == '[':
                    num = ""
                elif char.isdigit():
                    num += char 
                elif char == ']':
                    predicates[aux] = int(num)  
                    num = ""
                    aux = ""

    if line.startswith("equality"): 
        line = line[len("equality")+2:] 
        aux = ""
        for char in line:
            if char != ' ' and char != '\n':
                 aux += char
            else:
                equality.append(aux)
                aux = "" 

    if line.startswith("connectives"):  
        '''
        if i != len(Lines)-1 and (not Lines[i+1].startswith("variables")) and (not Lines[i+1].startswith("predicates")) and (not Lines[i+1].startswith("constants")) and (not Lines[i+1].startswith("equality")) and (not Lines[i+1].startswith("quantifiers")) and (not Lines[i+1].startswith("formula")):
            line += Lines[i+1]
            print(line)
            i += 1 
        '''
        line = line[len("connectives")+2:]   
        aux = ""
        for char in line:
            if char != ' ' and char != '\n':
                aux += char
            else:
                connectives.append(aux)
                aux = "" 

    if line.startswith("quantifiers"):  
        '''
        if i != len(Lines)-1 and (not Lines[i+1].startswith("variables")) and (not Lines[i+1].startswith("predicates")) and (not Lines[i+1].startswith("constants")) and (not Lines[i+1].startswith("equality")) and (not Lines[i+1].startswith("connectives")) and (not Lines[i+1].startswith("formula")):
            line += Lines[i+1]
            print(line)
            i += 1 
        '''
        line = line[len("quantifiers")+2:]   
        aux = ""
        for char in line:
            if char != ' ' and char != '\n':
                aux += char
            else:
                quantifiers.append(aux)
                aux = "" 

    if line.startswith("formula"):  
        if i != len(Lines)-1 and (not Lines[i+1].startswith("variables")) and (not Lines[i+1].startswith("constants")) and (not Lines[i+1].startswith("predicates")) and (not Lines[i+1].startswith("equality")) and (not Lines[i+1].startswith("connectives")) and (not Lines[i+1].startswith("quantifiers")):
            line += Lines[i+1]
            i += 1 
        line = line[len("formula")+2:]   
        input_formula = line
        aux = ""
        for char in line:
            if char != ' ' and char != '\n':
                aux += char
            else:
                input_formula_list.append(aux)
                aux = "" 
    i += 1


# Check the number of elements in equality, connectives, quantifiers 
if len(equality) != 1:
    g.write("Invalid number of equality symbols \n")
    print("Error occured; check log \n")
    sys.exit(1)
if len(connectives) != 5:
     g.write("Invalid number of connectives \n")
     print("Error occured; check log \n")
     sys.exit(1)
if len(quantifiers) != 2:
    g.write("Invalid number of quantifiers \n")
    print("Error occured; check log \n")
    sys.exit(1)

# Check constants, predicates, variables have different names
for x in constants:
    if x in predicates or x in variables:
        g.write("Invalid constant name \n")
        print("Error occured; check log \n")
        sys.exit(1)
for x in predicates:
    if x in constants or x in variables:
        g.write("Invalid predicate name \n")
        print("Error occured; check log \n")
        sys.exit(1)
for x in variables:
    if x in predicates or x in constants:
        g.write("Invalid variable name \n")
        print("Error occured; check log \n")
        sys.exit(1)

    
g.write("\nValid file")   

print('\n')
print("Variables: ", variables)
print("Constants: ", constants)
print("Predicates: ", predicates)
print("Equality: ", equality)
print("Connectives: ", connectives)
print("Quantifiers: ", quantifiers)
print("\nInput formula : ", input_formula)


def startswith_symbol(symbol, element):
    for x in symbol:
        if element.startswith(x):
            return x
    return 0

aux = ""

# function for transforming the formula into a list
def formula_to_list(formula_copy, formula_copy_list):
    while(len(formula_copy)):
        if formula_copy.startswith(' '):
            formula_copy = formula_copy[1:]
        
        elif formula_copy.startswith('('):
            formula_copy_list.append('(')
            formula_copy = formula_copy[1:]
        
        elif formula_copy.startswith(')'):
            formula_copy_list.append(')')
            formula_copy = formula_copy[1:]
        
        elif formula_copy.startswith(','):
            formula_copy_list.append(',') 
            formula_copy = formula_copy[1:]
        else:
            conn = startswith_symbol(connectives, formula_copy)
            if conn != 0:  
                formula_copy_list.append(conn)
                formula_copy = formula_copy[len(conn):]
            else:
                var = startswith_symbol(variables, formula_copy)
                if var != 0:  
                    formula_copy_list.append(var)
                    formula_copy = formula_copy[len(var):]
                else:
                    const = startswith_symbol(constants, formula_copy)
                    if const != 0:  
                        formula_copy_list.append(const)
                        formula_copy = formula_copy[len(const):]
                    else:
                        quant = startswith_symbol(quantifiers, formula_copy)
                        if quant != 0:  
                            formula_copy_list.append(quant)
                            formula_copy = formula_copy[len(quant):]
                        else:
                            pred = startswith_symbol(predicates, formula_copy)
                            if pred != 0:
                                formula_copy_list.append(pred)
                                formula_copy = formula_copy[len(pred):]
                            else:
                                if formula_copy.startswith(equality[0]):
                                    formula_copy_list.append(equality[0])
                                    formula_copy = formula_copy[len(equality[0]):]
                                else:
                                   formula_copy = formula_copy[1:]

    return formula_copy, formula_copy_list

# function for checking a predicate formula is correct
def check_predicate(pred, formula_el):
    arity = predicates[pred]
    sep = arity - 1

    if formula_el[1] != "(":
        return 0
    if formula_el[arity+sep+2] != ")":
        return 0
    for i in range(2, len(formula_el), 2):
        if formula_el[i] not in variables:
            return 0

    return 1

# function for checking an equality formula is correct
def check_equality(formula_el):
    aux = equality[0]
    aux = formula_el.split(aux)

    if aux[0] in constants and aux[1] in constants:
        return 1
    if aux[0] in constants and aux[1] in variables:
        return 1
    if aux[0] in variables and aux[1] in constants:
        return 1
    if aux[0] in variables and aux[1] in variables:
        return 1 
    
    return 0
    
# function for checking if a formula is valid    
def is_valid(formula, error_message):
    # check brackets match 
    stack = []
    for element in formula:
        if element == "(":
            stack.append(element)
        elif element == ")":
            if len(stack) != 0:
                stack.pop()
            else:
                error_message.append("unmatching brackets found")
                return 0

    if len(stack) != 0: 
        error_message.append("unmatching brackets found")
        return 0 

    # check predicates and equalities
    for i in range(len(formula)):
        # check equalities 
        if formula[i] == equality[0]:
            if i == 0 or i == len(formula)-1:
                return 0
            else :
                check = formula[i-1] + formula[i] + formula[i+1] 
                if check_equality(check) == 0:
                    error_message.append("invalid equality found")
                    return 0
        else:
            x = startswith_symbol(predicates, formula[i])
            # check predicates 
            if x != 0 :
                if i+1+2*predicates[x] > len(formula)-1:
                    return 0
                else:
                    if check_predicate(x, formula[i:(i+2+2*predicates[x])]) == 0:
                        error_message.append("invalid predicate found")
                        return 0
            
            # check forall, exists are followed by variable 
            elif formula[i] in quantifiers:
                    if formula[i+1] not in variables:
                        error_message.append("invalid symbol found after quantifier")
                        return 0
    
    # check brackets aren't redundant
    conn_count = 0
    open_brack_count = 0
    i = 0
    while i < len(formula):
        if formula[i] in predicates:
            x = startswith_symbol(predicates, formula[i])
            i += predicates[x] + 2
        elif formula[i] == '(':
            open_brack_count += 1
        elif formula[i] in connectives:
            conn_count += 1
        i += 1

    if (open_brack_count != conn_count):
        error_message.append("redundand brackets found")
        return 0

    return 1
                  
formula_copy = input_formula
formula_copy_list = []
formula_copy, formula_copy_list = formula_to_list(formula_copy, formula_copy_list)

# check if formula is valid and write corresponding message to log 
error_message = []
valid = is_valid(formula_copy_list, error_message)
if valid == 1:
    print("\nThe formula is valid")
    g.write("\nValid formula")
else:
    print("\nThe formula is invalid")
    g.write("\nInvalid formula: ")
    message = ""
    for x in error_message:
        message += x + " "
    g.write(message)
g.write("\n")

# Build the grammar for the set of valid formulae 
# the sets of terminal and non-terminal symbols
terminals = ""
for x in connectives:
    terminals += x + "  "
for x in quantifiers:
    terminals += x + "  "
for x in equality:
    terminals += x + "  "
for x in constants:
    terminals += x + "  "
for x in variables:
    terminals += x + "  "
for x in predicates:
    terminals += x + "  "

terminals += "(    )   ,"

non_terminals = "Start  Formula  PredicateFormula  EqualityFormula  T  connective  negation  quantifier  equality  constant  variable  predicate  o_bracket c_bracket  separator"

# production rules 
start_prod_rules = "Start -> Formula" 
formula_prod_rules = "Formula -> PredicateFormula  |  EqualityFormula  |  o_bracket Formula connective Formula c_bracket  |  negation Formula  |  quantifier variable Formula" 
pred_formula_prod_rules = "PredicateFormula -> predicate o_bracket variable separator variable separator ... separator variable c_bracket "
equality_formula_prod_rules = "EqualityFormula ->  bracket variable equality variable bracket |  bracket constant equality constant bracket  |  bracket constant equality variable bracket  |  bracket variable equality constant bracket"

term_prod_rules = "T -> constant  |  variable"

connective_prod_rules = "connective -> "
for x in connectives:
    connective_prod_rules += x + "  |  "
connective_prod_rules = connective_prod_rules[:len(connective_prod_rules)-5]
l = len(connectives[len(connectives)-1])
connective_prod_rules = connective_prod_rules[:len(connective_prod_rules)-l-4]

negation_prod_rules = "negation -> "
negation_prod_rules += connectives[len(connectives)-1]

quantifier_prod_rules = "quantifier -> "
for x in quantifiers:
    quantifier_prod_rules += x + "  |  "
quantifier_prod_rules = quantifier_prod_rules[:len(quantifier_prod_rules)-4]

equality_prod_rules = "equality -> "
equality_prod_rules += equality[0]

constant_prod_rules = "constant -> " #any string not used as a variable or predicate"
for x in constants:
    constant_prod_rules += x + "  |  "
constant_prod_rules = constant_prod_rules[:len(constant_prod_rules)-4]

variable_prod_rules = "variable -> " #any string not used as a constant or predicate"
for x in variables:
    variable_prod_rules += x + "  |  "
variable_prod_rules = variable_prod_rules[:len(variable_prod_rules)-4]

predicate_prod_rules = "predicate -> " #any string not used as a constant or variable" 
for x in predicates:
    predicate_prod_rules += x + "  |  "
predicate_prod_rules = predicate_prod_rules[:len(predicate_prod_rules)-4]

o_brack_prod_rules = "o_bracket -> ( "  
c_brack_prod_rules = "c_bracket -> ) "
sep_prod_rules = "separator -> ,"

print("\nThe corresponding grammar for the language of valid formulae: ")
print("\nTerminal symbols: ", terminals)
print("\nNon-terminal symbols: ", non_terminals)
print("\nProduction rules:")
print(start_prod_rules)
print("\n")
print(formula_prod_rules)
print("\n")
print(pred_formula_prod_rules)
print("\n")
print(equality_formula_prod_rules)
print("\n")
print(term_prod_rules) 
print("\n")
print(connective_prod_rules)
print("\n")
print(negation_prod_rules)
print("\n")
print(quantifier_prod_rules)
print("\n")
print(equality_prod_rules)
print("\n")
print(constant_prod_rules)
print("\n")
print(variable_prod_rules)
print("\n")
print(predicate_prod_rules)
print("\n")
print(o_brack_prod_rules)
print("\n")
print(c_brack_prod_rules)
print("\n")
print(sep_prod_rules)
print("\n")

f.close()
g.close()

# Exit the program if the formula is invalid
# otherwise, build the parse tree
if valid == 0:
     sys.exit(1)
else:
    print("Check generated parse tree")


connectives_copy = connectives[:len(connectives)-1]
negation = connectives[len(connectives)-1:]

work_list = formula_copy_list
tree_list = []

# Build the parse tree bottom-up

# start with the leaves
for element in work_list:
    if element == '(':
        tree = Tree('o_bracket', [element])
        tree_list.append(tree)
    if element == ')':
        tree = Tree('c_bracket', [element])
        tree_list.append(tree)
    if element == ',':
        tree = Tree('separator', [element])
        tree_list.append(tree)
    if element in variables:
        tree = Tree('variable', [element])
        tree_list.append(tree)
    if element in constants:
        tree = Tree('constant', [element])
        tree_list.append(tree)
    if element in connectives_copy:
        tree = Tree('connective', [element])
        tree_list.append(tree)
    if element in negation:
        tree = Tree('negation', [element])
        tree_list.append(tree)
    if element in quantifiers:
        tree = Tree('quantifier', [element])
        tree_list.append(tree)
    if element in equality:
        tree = Tree('equality', [element])
        tree_list.append(tree)
    if element in predicates:
        tree = Tree('predicate', [element])
        tree_list.append(tree)


tree_list_copy = tree_list
work_list_copy = work_list

# look for equality formulas
i = 0
while i < len(work_list):
    if work_list[i] in equality:
        #print(i)
        aux_tree = Tree('EqualityFormula', tree_list[(i-2):(i+3)])
        #print(len(tree_list_copy))
        tree_list_copy[i-2] = aux_tree
        work_list_copy[i-2] = 'EqualityFormula'
        del tree_list_copy[i-1:i+3]
        del work_list_copy[i-1:i+3]
        work_list = work_list_copy
        tree_list = tree_list_copy
        i = i-2
    else: 
        i += 1

# look for predicate formulas
i = 0 
while i < len(work_list):
    if work_list[i] in predicates:
        #print(i)
        arity = predicates[work_list[i]]
        aux_tree = Tree('PredicateFormula', tree_list[(i):(i+2*arity+2)])
        
        tree_list_copy[i] = aux_tree
        work_list_copy[i] = 'PredicateFormula'

        del tree_list_copy[i+1:(i+2*arity+2)]
        del work_list_copy[i+1:(i+2*arity+2)]

        work_list = work_list_copy
        tree_list = tree_list_copy
    else: 
        i += 1

# look for brackets, connectives, negation, quantifiers+variables
i = 0 
while i < len(work_list):
    if work_list[i] == '(':
        work_list[i] = 'o_bracket'
    if work_list[i] == ')':
        work_list[i] = 'c_bracket'
    if work_list[i] in connectives_copy:
        work_list[i] = 'connective'
    if work_list[i] in negation:
        work_list[i] = 'negation'
    if work_list[i] in quantifiers:
        work_list[i] = 'quantifier'
    if work_list[i] in variables:
        work_list[i] = 'variable'
    i += 1

# look for equality formulas and predicate formulas, replace them with formula - change comment 
i = 0 
while i < len(work_list):
    if work_list[i] == 'EqualityFormula':
        work_list[i] = 'Formula'
        aux_tree = Tree('Formula', [tree_list[i]])
        tree_list[i] = aux_tree
    if work_list[i] == 'PredicateFormula':
        work_list[i] = 'Formula'
        aux_tree = Tree('Formula', [tree_list[i]])
        tree_list[i] = aux_tree
    i += 1

while len(work_list) > 1:
    # look for negation Formula
    i = 0
    while i < len(work_list):
        if work_list[i] == 'negation' and work_list[i+1] == 'Formula':
            aux_tree = Tree('Formula', tree_list[i:i+2])

            tree_list_copy[i] = aux_tree
            work_list_copy[i] = 'Formula'

            del tree_list_copy[i+1]
            del work_list_copy[i+1]

            work_list = work_list_copy
            tree_list = tree_list_copy
        else:
            i += 1
    
    # look for quantifier variable Formula 
    i = 0
    while i < len(work_list):
        if work_list[i] == 'quantifier' and work_list[i+1] == 'variable' and work_list[i+2] == 'Formula':
            aux_tree = Tree('Formula', tree_list[i:i+3])

            tree_list_copy[i] = aux_tree
            work_list_copy[i] = 'Formula'

            del tree_list_copy[i+1:i+3]
            del work_list_copy[i+1:i+3]

            work_list = work_list_copy
            tree_list = tree_list_copy
        else:
            i += 1
    
    # look for o_bracket Formula connective Formula connective c_bracket 
    i = 0
    while i < len(work_list):
        if work_list[i] == 'o_bracket' and work_list[i+1] == 'Formula' and work_list[i+2] == 'connective' and work_list[i+3] == 'Formula' and work_list[i+4] == 'c_bracket':
            aux_tree = Tree('Formula', tree_list[i:i+5])

            tree_list_copy[i] = aux_tree
            work_list_copy[i] = 'Formula'

            del tree_list_copy[i+1:i+5]
            del work_list_copy[i+1:i+5]

            work_list = work_list_copy
            tree_list = tree_list_copy
        else:
            i += 1
    

parseTree = Tree('Start', tree_list)
TreeView(parseTree)._cframe.print_to_file('ParseTree.ps') 
