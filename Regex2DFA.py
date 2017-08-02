from SyntaxTree import *
from Automata import *


def create_token_queue(INPUT):
    '''
    Process the input and converts it to a list containing the regex elements and alphabets.
    
    Args:
        INPUT: string, containing the input 

    Returns:
        list, containing the regex elements and alphabets.

    '''
    tokens = []
    id = ''
    for c in INPUT:
        if c in ['(', ')', '.', '*', '+']:
            if id != '':
                tokens.append(id)
                id = ''
            tokens.append(c)
        else:
            id = id + c
    if id != '':
        tokens.append(id)
    return tokens


def create_postfix_token_queue(tokens):
    '''
    Creates the postfix representation of the regex (stored in a list). This postfix representation is later used to create the Syntax Tree.
    
    Args:
        tokens: list, containing the regex elements and alphabets 

    Returns:
        list, containing the regex elements and alphabets in a postfix manner.

    '''
    output_queue = []
    stack = []
    for token in tokens:
        if token == '(':
            stack.append('(')
        elif token == ')':
            while (len(stack) > 0 and stack[-1] != '('):
                output_queue.append(stack.pop())
            stack.pop()
        elif token == '*':
            stack.append(token)
        elif token == '.':
            while len(stack) > 0 and stack[-1] == '*':
                output_queue.append(stack.pop())
            stack.append(token)
        elif token == '+':
            while len(stack) > 0 and (stack[-1] == '*' or stack[-1] == '.'):
                output_queue.append(stack.pop())
            stack.append(token)
        else:
            output_queue.append(token)
    while (len(stack) > 0):
        output_queue.append(stack.pop())
    return output_queue


def read_input(path):
    '''
    Reads in the input which should be in the following format:
    <N, number of alphabets>
    <alphabet 1>
    <alphabet 2>
    <alphabet ...>
    <alphabet N>
    <REGEX>
    for more detail on the input please refer to InOut_Formatting.md
    
    Args:
        path: string, the path to the input file

    Returns:
        list, containing the alphabets
        string, containing the Regex
    '''
    alph = []
    file = open(path)
    lines = file.readlines()
    file.close()
    for i in range(int(lines[0])):
        alph.append(lines[1 + i].strip())
    return alph, lines[int(lines[0]) + 1].strip()


def regex2DFA(path):
    '''
    Computes the DFA of a regular expression
    
    Args:
        path: string, the path to the input file

    Returns:
        None
    '''
    # 1. Reading the input
    ALPH, INPUT = read_input(path)
    # 2. Getting the tokens
    tokens = create_token_queue(INPUT)
    # 3. Converting the tokens to post-order format
    post = create_postfix_token_queue(tokens)
    # 4. Creating the tree
    t = Tree(post)
    # 5. Creating the DFA
    d = DFA(ALPH, t)
    # 6. Printing the results
    print(INPUT)
    print(t)
    print(d)


regex2DFA('Inputs\\Input2.txt')
