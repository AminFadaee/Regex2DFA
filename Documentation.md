# Documentation
## Algorithm
### 1. Pre-procsessings

The steps done for preprocessing the input are as follows (these steps are done in `Regex2DFA.py`):

##### 1.1. Tokenization of the input regex into a list of tokens.

This steps is done by the function `create_token_queue`

##### 1.2. Computing the post-order of the tokens

This steps is needed to construct the Syntax Tree and is done by the function `create_postfix_token_queue`

### 2. Constructing the Annotated Syntax Tree

The steps done in this parts are in `SyntaxTree.py`.
For the purpose of creating the tree we have two classes :`Node` and `Tree`
##### 2.1. Class Node
###### Examples:
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