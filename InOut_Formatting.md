Input and Output Formatting
===========================
## Input
### Genera Format:
The input for this project should follow a specific formatting.
- The first line is an integer `N` representing the number of alphabets in the regular expression language.
- The next N lines are the alphabet used in the language.
- The last line is the regex.

### Notes:
1. The alphabets can be single characters (any thing except `*,.,+,$ or @`) or complete words.
2. The concatenation is *not* done implicitly! Where ever you are concatenating two alphabets you **have to** use the `.` character:
    - Wrong: `ab*`
    - Right: `a.b*`
### Example:
```
2
a
b
(a+b)*.a.(a+b).(a+b)
```
## Output
### General Format:
- The first line is the regular expression read from the input.
- After that the syntax tree based on this regex is shown.
- Lastly the DFA would be depicted:
    - The `->` denotes the starting state.
    - The final states would have a `Final State` besides them.
    - The first column is the `id` of the state,
    - Followed by the transition for each alphabet.
### Example:
```
(a+b)*.a.(a+b).(a+b)
.
|
|___.
|   |
|   |___.
|   |   |
|   |   |___.
|   |   |   |
|   |   |   |___+
|   |   |   |   |
|   |   |   |   |___b
|   |   |   |   |
|   |   |   |   |___a
|   |   |   |
|   |   |   |___+
|   |   |       |
|   |   |       |___b
|   |   |       |
|   |   |       |___a
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
    2   a : 3   b : 3
    3   a : 4   b : 5
    4   a : 4   b : 4   Final State
    5   a : 5   b : 5
```