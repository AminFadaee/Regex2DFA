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
Examples:
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
### 3. Constructing the DFA