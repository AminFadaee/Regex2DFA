from SyntaxTree import *
from Automata import *

def create_token_queue(INPUT):
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


def read_input():
    alph = []
    file = open('Input.txt')
    lines = file.readlines()
    file.close()
    for i in range(int(lines[0])):
        alph.append(lines[1 + i].strip())
    return alph, lines[int(lines[0]) + 1].strip()


def __main__():
    ALPH, INPUT = read_input()
    tokens = create_token_queue(INPUT)
    post = create_postfix_token_queue(tokens)
    t = Tree(post)
    print(post)
    print(t)
    d = DFA(ALPH, t)
    d.print_DFA()


__main__()