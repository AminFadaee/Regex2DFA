# Documentation
## Algorithm
### 1. Pre-procsessings
#### General Pseudocode:
```
```
The steps done for preprocessing the input are as follows (these steps are done in `Regex2DFA.py`):

##### 1.1. Tokenization of the input regex into a list of tokens.

This steps is done by the function `create_token_queue`

##### 1.2. Computing the post-order of the tokens

This steps is needed to construct the Syntax Tree and is done by the function `create_postfix_token_queue`

### 2. Constructing the Annotated Syntax Tree
#### General Pseudocode:
```
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
- id: Each non empty-char tree leaf should have an integer id
- type: one of 'identifier','cat','or','star' representing the type of node in syntax tree
- left_child
- right_child
- label: label of a node ('.' for 'cat','*' for 'star','+' for 'or', and the actual label in the regex for 'identifier'
- nullable: True if we can derive empty-char from this node
- firstpos: firstpos of node (refer to documentation.md for detail).
- lastpos: followpos of node (refer to documentation.md for detail).

###### Methods:
- print_subtree: Function for printing the subtree with root self. This function has been written for debugging purposes
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
##### 2.1. Class Tree
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
- root: Root of the tree (root is always concatenation of the regex with '#' mark.)
- leaves: Keeping track of the labels of the leaves for convenience
- id_counter: This variable is used to assign id to leaves.
- followpos: list of sets for storing the followpos
###### Methods
- create_tree(): Creates tree structure (without metadata) by the tokens in post-order form.
- give_next_id(): This function simply increments self.id_counter and return its previous value
- postorder_nullable_firstpos_lastpos_followpos(): Recursive function for annotating the tree with the meta-data
        (Nullable, Firstpos, Lastpos) and deriving the Followpos in a
         post-order manner.
- compute_follows(): This function compute the Followpos of n and updates self.followpos

### 3. Constructing the DFA
#### General Pseudocode:
```
```
The steps done in this part is in the `Automata.py` and the classes `State` and `DFA` are designed for the purpose of constructing the dfa.
##### 3.1. Class State
Class for states that comprise the DFA
###### Attributes
- id_set: Each state in a DFA is a compound of few leaves, id_set contains these leaves
- id: id of the state
- transitions: Dictionary to keep all the transitions to other states
- final: True if this is a final state
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
- states: All the states in DFA; containing `State` instances
- alphabet: alphabets used in regex
- id_counter = 1
- terminal: '#' leaf is the end of regex and the id of it is assigned to terminal
###### Methods
- compute_states(): Constructs the DFA based on the syntax tree.
- Dtran(): This function finds all the transitions by the alphabet from state.
- post_processing(): The post processing step to make the printing of the DFA more appealing.
        This function is not necessary to use.
- give_next_id(): This function simply increments self.id_counter and return its previous value
