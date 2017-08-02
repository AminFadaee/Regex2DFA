class Node:
    '''
    This class is responsible for book-keepings of each node in the tree.
    
    Examples:
        >>> Node('cat','.')
        <'cat' Node with label '.' and 0 children>
        >>> print(Node('star','*'))
        Type		:	star
        Label		:	*
        Children	:	0
        Nullable	:	False
        Firstpos	:	set()
        Lastpos		:	set()

    '''

    def __init__(self, type, label, id=None, left_child=None, right_child=None):
        '''
        Constructor for the class Node.
        
        Args:
            type: one of 'identifier','cat','or','star' representing the type of node in syntax tree.
            label: label of a node ('.' for 'cat','*' for 'star','+' for 'or', and the actual label in the regex for 'identifier'
            id: integer, id of the node
            left_child: Node, representing the left child
            right_child: Node, representing the right child
        '''
        self.id = id  # Each non empty-char tree leaf should have an integer id
        self.type = type
        self.left_child = left_child
        self.right_child = right_child
        self.label = label
        self.nullable = False  # True if we can derive empty-char from this node
        self.firstpos = set()  # firstpos of node (refer to documentation.md for detail).
        self.lastpos = set()  # followpos of node (refer to documentation.md for detail).

    def __str__(self):
        '''Printing string'''
        childrenCount = int(self.right_child != None) + int(self.left_child != None)
        return '''Type\t\t:\t{0}
Label\t\t:\t{1}
Children\t:\t{2}
Nullable\t:\t{3}
Firstpos\t:\t{4}
Lastpos\t\t:\t{5}'''.format(self.type, self.label, childrenCount, self.nullable, self.firstpos, self.lastpos)

    def __repr__(self):
        '''In console string'''
        childrenCount = int(self.right_child != None) + int(self.left_child != None)
        s = "<" + "'{0}'".format(self.type) + ' Node with label ' + "'{0}'".format(self.label) + ' and ' + str(
            childrenCount) + [' child', ' children'][childrenCount != 1] + '>'
        return s

    def print_subtree(self, level=0, linelist=[], rightchild=False, instar=False):
        '''
        Function for printing the subtree with root self. This function has been written for debugging purposes
        but can also be used for printing the whole tree in the output of the program.
        
        Args:
            level: integer, the level of tree we are currently in 
            linelist: list of the lines that follows to the ancestors
            rightchild: Boolean, True if self is the right child of its father
            instar: Boolean, True if the father of self is a star node

        Returns:
            None
        Examples:
            >>> N.print_subtree()
            .
            |
            |___+
            |	|
            |	|___*___b
            |	|
            |	|___*___a
            |
            |___#
        '''
        star = self.type == 'star'
        N = '\n'
        T = '\t'
        L = '|'
        if level == 0:
            ret = self.label + '\n'
        else:
            s = ''
            if not instar:
                for k in range(2):
                    for i in range(level):
                        if i in linelist:
                            s += T*(i!=0) + L
                        else:
                            s += T
                    if k == 0:
                        s += N

            ret = s + '___' + self.label + N * (not star)
        if rightchild:
            linelist.pop(-1)
        if self.left_child:
            ret += self.left_child.print_subtree(level + 1, linelist + [level] * (not star),
                                                 instar=star)
        if self.right_child:
            ret += self.right_child.print_subtree(level + 1, linelist + [level], rightchild=True)
        return ret


class Tree:
    '''
    This class constructs the syntax tree which is a crucial part in
    obtaining the DFA (refer to documentation.md for details).
    
    Examples:
        >>> POtokens=['a', '*', 'b', '*', '+']
        >>> Tree(POtokens)
        .
        |
        |___+
        |	|
        |	|___*___b
        |	|
        |	|___*___a
        |
        |___#
    '''
    def __init__(self, post):
        '''
        This class inputs the tokens in post-order form and create the appropriate
        syntax tree for computing the DFA
        
        Args:
            post: list of tokens in a post-order fashion 
        '''
        self.root = Node('cat', '.')  # Root is always concatenation of the regex with '#' mark.
        self.leaves = dict()  # Keeping track of the labels of the leaves for convenience
        self.id_counter = 1  # This variable is used to assign id to leaves.
        # 1. Creating tree:
        self.create_tree(post)
        # 2. Finding the followpos of the tree and Nullable,Firstpos and Lastpos for each node:
        self.followpos = [set() for i in range(self.id_counter)]
        self.postorder_nullable_firstpos_lastpos_followpos(self.root)

    def create_tree(self, post):
        '''
        Creates tree structure (without metadata) by the tokens in post-order form.
        
        Args:
            post: list of tokens in a post-order fashion 

        Returns:
            None

        '''
        stack = []
        for token in post:
            if token == '.':
                left = stack.pop()
                right = stack.pop()
                temp = Node('cat', token, left_child=left, right_child=right)
                stack.append(temp)
            elif token == '+':
                left = stack.pop()
                right = stack.pop()
                temp = Node('or', token, left_child=left, right_child=right)
                stack.append(temp)
            elif token == '*':
                left = stack.pop()  # Star node has only one child.
                temp = Node('star', token, left_child=left)
                stack.append(temp)
            else:  # identifier
                temp = Node('identifier', token, id=self.give_next_id())
                self.leaves[temp.id] = temp.label
                stack.append(temp)

        temp = Node('identifier', '#', id=self.give_next_id())
        self.leaves[temp.id] = temp.label
        self.root.left_child = stack.pop()
        self.root.right_child = temp
        return

    def give_next_id(self):
        '''
        This function simply increments self.id_counter and return its previous value
        
        Returns: 
            self.id_counter

        '''
        id = self.id_counter
        self.id_counter += 1
        return id

    def postorder_nullable_firstpos_lastpos_followpos(self, node):
        '''
        Recursive function for annotating the tree with the meta-data
        (Nullable, Firstpos, Lastpos) and deriving the Followpos in a
         post-order manner.
        
        Args:
            node: Node, Current node

        Returns:
            None

        '''
        if not node:  # Recursion terminator
            return
        # 1. Left
        self.postorder_nullable_firstpos_lastpos_followpos(node.left_child)
        # 2. Right
        self.postorder_nullable_firstpos_lastpos_followpos(node.right_child)
        # 3. Root
        if node.type == 'identifier':
            if node.label == '@':  # empty char
                node.nullable = True
            else:
                node.firstpos.add(node.id)
                node.lastpos.add(node.id)
        elif node.type == 'or':
            node.nullable = node.left_child.nullable or node.right_child.nullable
            node.firstpos = node.left_child.firstpos.union(node.right_child.firstpos)
            node.lastpos = node.left_child.lastpos.union(node.right_child.lastpos)
        elif node.type == 'star':
            node.nullable = True
            node.firstpos = node.left_child.firstpos
            node.lastpos = node.left_child.lastpos
            self.compute_follows(node)  # Follows is only computed for star and cat nodes
        elif node.type == 'cat':
            node.nullable = node.left_child.nullable and node.right_child.nullable
            if node.left_child.nullable:
                node.firstpos = node.left_child.firstpos.union(node.right_child.firstpos)
            else:
                node.firstpos = node.left_child.firstpos
            if node.right_child.nullable:
                node.lastpos = node.left_child.lastpos.union(node.right_child.lastpos)
            else:
                node.lastpos = node.right_child.lastpos
            self.compute_follows(node)  # Follows is only computed for star and cat nodes
        return

    def compute_follows(self, n):
        '''
        This function compute the Followpos of n and updates self.followpos
        
        Args:
            n: Node

        Returns:
            None
        '''
        if n.type == 'cat':
            for i in n.left_child.lastpos:
                self.followpos[i] = self.followpos[i].union(n.right_child.firstpos)
        elif n.type == 'star':
            for i in n.left_child.lastpos:
                self.followpos[i] = self.followpos[i].union(n.left_child.firstpos)

    def __str__(self):
        '''Printing string'''
        return self.root.print_subtree()
    def __repr__(self):
        '''In console string'''
        return self.root.print_subtree()
