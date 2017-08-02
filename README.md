Regular Expression to DFA
=========================
## Introduction:
This project converts and arbitrary regular expression (Regex) to a DFA using a Syntax Tree and conducting the following steps:

1. Converting the Regex to post-order format
2. Creating the Annotated Syntax Tree of the Regex
3. Creating the DFA based on the tree.

## Documentation

The code is documented using Google Style Docstring but for a detailed documentation on the algorithm and code, read the  [documentation.md](https://github.com/AminFadaee/Regex2DFA/blob/master/Documentation.md)

## Requirements

* Python Version 3+
* General Knowledge of Regular Expressions and Finite State Automatas

## Running:

Run the project by running [Regex2DFA.py](https://github.com/AminFadaee/Regex2DFA/blob/master/Regex2DFA.py)

Here is the results for [Input1.txt](https://github.com/AminFadaee/Regex2DFA/blob/master/Inputs/Input1.txt) located in the inputs directory:
```
a*+b*
.
|
|___+
|   |
|   |___*___b
|   |
|   |___*___a
|
|___#

->  1   a : 2   b : 3   Final State
    2   a : 2   b : 4   Final State
    3   a : 4   b : 3   Final State
    4   a : 4   b : 4
```

and [Input4.txt](https://github.com/AminFadaee/Regex2DFA/blob/master/Inputs/Input4.txt):
```
(a+b)*.a.(a+b)
.
|
|___.
|   |
|   |___.
|   |   |
|   |   |___+
|   |   |   |
|   |   |   |___b
|   |   |   |
|   |   |   |___a
|   |   |
|   |   |___a
|   |
|   |___*___+
|           |
|           |___b
|           |
|           |___a
|
|___#

->  1   a : 2   b : 2
    2   a : 3   b : 4
    3   a : 3   b : 3   Final State
    4   a : 4   b : 4
```

For more detail on the format of input and output please refer to [InOut_Formatting.md](https://github.com/AminFadaee/Regex2DFA/blob/master/InOut_Formatting.md)

## License

The MIT License. Copyright (c) 2017 Amin Fadaee

## About Author

[Amin Fadaee](https://www.linkedin.com/in/aminfadaee/)
