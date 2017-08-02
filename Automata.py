class State:
    '''
    Class for states that comprise the DFA
    
    Attributes:
        id_set: set, Each state in a DFA is a compound of few tree leaves, id_set keeps all of these leaves
        id: integer, the id a the state
        transitions: dictionary of sets, with alphabets of regex as key and a set of tree leaves ids which 
        in the end creates a single state
    '''

    def __init__(self, alphabet, id_list, id, terminal_id):
        '''
        Constructor for class State
        
        Args:
            alphabet: list containing alphabets used in regex (used in transitions of state) 
            id_list: list, Each state in a DFA is a compound of few leaves, List contains these leaves
            id: integer, id of the state
            terminal_id: integer, the id of '#' leaf/ the end char of regex
        '''
        self.id_set = set(id_list)
        self.id = id
        self.transitions = dict()  # Dictionary to keep all the transitions to other states
        self.final = terminal_id in self.id_set  # True if this is a final state
        for a in alphabet:
            self.transitions[a] = {}  # Each transitions from this state by a char is stored in a set


class DFA:
    def __init__(self, alphabet, tree):
        '''
        Constructor for class DFA.
        
        Args:
            alphabet: list containing alphabets used in regex
            tree: Tree, syntax tree of the regex with meta-data (nullable,firstpos,lastpo,followpos)
        '''
        self.states = []  # All the states in DFA containing State instances
        self.alphabet = alphabet
        self.id_counter = 1
        self.terminal = tree.id_counter - 1  # '#' leaf is the end of regex and the id of it is assigned to terminal
        self.compute_states(tree)  # constructs the DFA based on syntax tree

    def compute_states(self, t):
        '''
        Constructs the DFA based on t, the syntax tree.
        
        Args:
            t: Tree, the annotated syntax tree

        Returns:
            None

        '''
        D1 = State(self.alphabet, t.root.firstpos, self.give_next_id(), self.terminal)
        self.states.append(D1)
        queue = [D1]
        while len(queue) > 0:  # Finds the transitions to all states
            st = queue.pop(0)
            new_states = self.Dtran(st, t)
            for s in new_states:
                state = State(self.alphabet, s, self.give_next_id(), self.terminal)
                self.states.append(state)
                queue.append(state)
        return

    def Dtran(self, state, tree):
        '''
        This function finds all the transitions by the alphabet from state (for details refer to documentation.md)
        
        Args:
            state: State 
            tree: Tree, the annotated syntax tree

        Returns:
            list of all the leaves that state goes to that together form a state
        '''
        new_states = []
        for i in state.id_set:
            if i == self.terminal:
                continue
            label = tree.leaves[i]
            if state.transitions[label] == {}:
                state.transitions[label] = tree.followpos[i]
            else:
                state.transitions[label] = state.transitions[label].union(tree.followpos[i])
        for a in self.alphabet:
            if state.transitions[a] != {}:
                new = True
                for s in self.states:
                    if s.id_set == state.transitions[a] or state.transitions[a] in new_states:
                        new = False
                if new:
                    new_states.append(state.transitions[a])
        print(new_states)
        return new_states

    def post_processing(self):
        '''
        The post processing step to make the printing of the DFA more appealing.
        This function is not necessary to use.
        
        Returns:
            None
        '''
        has_none_state = False
        for state in self.states:
            for a in self.alphabet:
                if state.transitions[a] == {}:
                    has_none_state = True
                    state.transitions[a] = self.id_counter
                SET = state.transitions[a]
                for state2 in self.states:
                    if state2.id_set == SET:
                        state.transitions[a] = state2.id
        if has_none_state:
            self.states.append(State(self.alphabet, [], self.id_counter, self.terminal))
            for a in self.alphabet:
                self.states[-1].transitions[a] = self.states[-1].id

    def give_next_id(self):
        '''
        This function simply increments self.id_counter and return its previous value

        Returns: 
            self.id_counter

        '''
        id = self.id_counter
        self.id_counter += 1
        return id

    def print_DFA(self):
        '''
        This function prints out the DFA
        
        Returns:
            None
        Examples:
            >>> D.print_DFA()
            ->	1	a : 2	b : 3	Final State
                2	a : 2	b : 4	Final State
                3	a : 4	b : 3	Final State
                4	a : 4	b : 4	
        '''
        self.post_processing()
        for state in self.states:
            if state.id == 1:
                print('->', end='\t')
            else:
                print('', end='\t')
            print(state.id, end='\t')
            for a in self.alphabet:
                print(a, ':', state.transitions[a], end='\t')
            if state.final:
                print("Final State", end='')
            print()
