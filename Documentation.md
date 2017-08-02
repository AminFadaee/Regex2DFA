# Documentation
Table of Contents
=================
- [Introduction](#introduction)
- [Algorithm](#algorithm)
    - [General Pseudocode #1](#general-pseudocode-1)
    1. [Pre-procsessings](#1-pre-procsessings)
        1. [Tokenization of the input regex into a list of tokens](#11-tokenization-of-the-input-regex-into-a-list-of-tokens)
        2. [Computing the post-order of the tokens](#12-computing-the-post-order-of-the-tokens)
    2. [Constructing the Annotated Syntax Tree](#2-constructing-the-annotated-syntax-tree)
        - [General Pseudocode #2](#general-pseudocode-2)
        1. [Class Node](#21-class-node)
            - [Example](#example)
            - [Attributes](#attributes)
            - [Methods](#methods)
        2. [Class Tree](#22-class-tree)
            - [Example](#example-1)
            - [Attributes](#attributes-1)
            - [Methods](#methods-1)
    3. [Constructing the DFA](#3-constructing-the-dfa)
        - [General Pseudocode #3](#)
        1. [Class State](#general-pseudocode-3)
            - [Attributes](#attributes-2)
            - [Methods](#methods-2)
        2. [Class DFA](#32-class-dfa)
            - [Example](#example-2)
            - [Attributes](#attributes-3)
            - [Methods](#methods-2)
- [About Author](#about-author)
- [License](#license)

## Introduction:
This project converts and arbitrary regular expression (Regex) to a DFA that recognizes the language of this regex using a Syntax Tree and conducting the following steps:

1. Converting the Regex to post-order format
2. Creating the Annotated Syntax Tree of the Regex
3. Creating the DFA based on the tree.
## Algorithm
Note: All pseudocodes in this documentation is roughly cited from the book *Compilers - Principles, Techniques and Tools 2nd Edition*
#### General Pseudocode #1:
```
INPUT : A regular expression r.
OUTPUT: A DFA D that recognizes L(r)
Method:
1. Construct a syntax tree T from augmented regular expression (r).#
2. Compute nullable, firstpos, lastpos and followpos for T, using methods of General Pseudocode #2.
3. Construct the DFA based on General Psuedocode #3.
```
### 1. Pre-procsessings
The steps done for preprocessing the input are as follows (these steps are done in `Regex2DFA.py`):

##### 1.1. Tokenization of the input regex into a list of tokens.

This steps is done by the function `create_token_queue`

##### 1.2. Computing the post-order of the tokens

This steps is needed to construct the Syntax Tree and is done by the function `create_postfix_token_queue`

### 2. Constructing the Annotated Syntax Tree
#### General Pseudocode #2:
```
1. Construct the basic tree based on the tokens.

2. Anotate it with firstpos, lastpos and nullable using these rules:

    1. If N is a leaf with labeled @ (empty char):
        * nullable(N)=True
        * firstpos(N)={}
        * lastpos(N)={}
    2. If N is a leaf with id i:
        * nullable(N)=False
        * firstpos(N)= {i}
        * lastpos(N) = {i}
    3. If N = c1 + c2:
        * nullable(N) = nullable(c1) or nullable(c2)
        * firstpos(N) = firstpos(c1) U firstpos(c2)
        * lastpos(N) = lastpos(c1) U lastpos(c2)
    4. If N = c*
        * nullable(N)=True
        * firstpos(N) = firstpos(c)
        * lastpos(N) = lastpos(c)
    5. If N=c1.c2:
        * nullable(N)=nullable(c1) and nullable(c2)
        * if(nullable(c1): firstpos(N)=firstpos(c1) U firstpos(c2)
          else: firstpos(N)=firstpos(c1)
        * if(nullable(c2)): lastpos(N)=lastpos(c1) U lastpos(c2)
          else: lastpos(c2)

3. Compute the followpos:

    1. if N=c1.c2:
            for each i in lastpos(c1):
                followpos(i)=followpos(i) U firstpos(c2)
    2. if N=c*:
            for each i in lastpos(c):
                followpos(i)=followpos(i) U firtspos(c)
```
The steps done in this parts are in `SyntaxTree.py`.
For the purpose of creating the tree we have two classes :`Node` and `Tree`
##### 2.1. Class Node
This class is responsible for book-keepings of each node in the tree.
###### Example:
```python
>>> Node('cat','.')
<'cat' Node with label '.' and 0 children>
>>> print(Node('star','*'))
Type        :   star
Label       :   *
Children    :   0
Nullable    :   False
Firstpos    :   set()
Lastpos     :   set()
```
###### Attributes:
- **id**: Each non empty-char tree leaf should have an integer id
- **type**: one of 'identifier','cat','or','star' representing the type of node in syntax tree
- **left_child**
- **right_child**
- **label**: label of a node ('.' for 'cat','*' for 'star','+' for 'or', and the actual label in the regex for 'identifier'
- **nullable**: True if we can derive empty-char from this node
- **firstpos**: firstpos of node (refer to documentation.md for detail).
- **lastpos**: followpos of node (refer to documentation.md for detail).

###### Methods:
- **print_subtree**(): Function for printing the subtree with root self. This function has been written for debugging purposes
        but can also be used for printing the whole tree in the output of the program.

    Example:
    ```python
    >>> N.print_subtree()
    +
    |
    |___*___b
    |
    |___*___a
    ```
##### 2.2. Class Tree
This class constructs the syntax tree which is a crucial part in
    obtaining the DFA
###### Example
```python
>>> POtokens=['a', '*', 'b', '*', '+']
>>> Tree(POtokens)
.
|
|___+
|   |
|   |___*___b
|   |
|   |___*___a
|
|___#
```
###### Attributes
- **root**: Root of the tree (root is always concatenation of the regex with '#' mark.)
- **leaves**: Keeping track of the labels of the leaves for convenience
- **id_counter**: This variable is used to assign id to leaves.
- **followpos**: list of sets for storing the followpos
###### Methods
- **create_tree**(): Creates tree structure (without metadata) by the tokens in post-order form.
- **give_next_id**(): This function simply increments self.id_counter and return its previous value
- **postorder_nullable_firstpos_lastpos_followpos**(): Recursive function for annotating the tree with the meta-data
        (Nullable, Firstpos, Lastpos) and deriving the Followpos in a
         post-order manner.
- **compute_follows**(): This function compute the Followpos of n and updates self.followpos

### 3. Constructing the DFA
#### General Pseudocode #3:
```
Construct Dstates, the set of states of DFA D, and Dtran,
the transition function for D, by the procedure below.
The states of D are sets of positions in T. Initially,
each state is unmarked and a state becomes marked just
before we consider its out-transitions. The start state
of D is firstpos(N0), where node N0 is the root of T.
The accepting states are those containing the position
for the endmarker symbol #.

initialize Dstates to contain only the unmarked state firstpos(N0),
where N0 is the root of syntax tree T for (r).#

while(there is an unmarked state S in Dstates){
    mark S
    for each input sympol a
        let u be the union of followpos(p) for all p
            in S that correspond to a
        if u is not in Dstates
            add u as an unmarked state to Dstates
        Dtran[S,a] = u
```
The steps done in this part is in the `Automata.py` and the classes `State` and `DFA` are designed for the purpose of constructing the dfa.
##### 3.1. Class State
Class for states that comprise the DFA
###### Attributes
- **id_set**: Each state in a DFA is a compound of few leaves, id_set contains these leaves
- **id**: id of the state
- **transitions**: Dictionary to keep all the transitions to other states
- **final**: True if this is a final state
###### Methods: None
##### 3.2. Class DFA
Class representing the DFA that creates and store the DFA corresponding to the regex.
###### Example
```python
>>> t = Tree(['a', '*', 'b', '*', '+'])
>>> d = DFA(alphabet=['a','b'],tree=t)
>>> d
->  1   a : 2   b : 3   Final State
    2   a : 2   b : 4   Final State
    3   a : 4   b : 3   Final State
    4   a : 4   b : 4
```
###### Attributes
- **states**: All the states in DFA; containing `State` instances
- **alphabet**: alphabets used in regex
- **id_counter**
- **terminal**: '#' leaf is the end of regex and the id of it is assigned to terminal
###### Methods
- **compute_states**(): Constructs the DFA based on the syntax tree.
- **Dtran**(): This function finds all the transitions by the alphabet from state.
- **post_processing**(): The post processing step to make the printing of the DFA more appealing.
        This function is not necessary to use.
- **give_next_id**(): This function simply increments self.id_counter and return its previous value

## About Author

[Amin Fadaee](https://www.linkedin.com/in/aminfadaee/)

## License

The MIT License. Copyright (c) 2017 Amin Fadaee