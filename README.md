# CLI_Quizlet
A simple cli flashcard quiz, with saved JSON format flashcards, decks, and results for analysis

## Plans for later updates
- functions to edit current decks
- functions to analyze results
    - find the questions that with the most skips and flips
- functions to provide analysis on results after a quiz


## Requirements
format for json flashcards files
{'q':q, 'a':a}
all json flash cards must be stored in a single folder with nothing else in it
file name must be 'card_{int}.json' where int is a unique integer number identifying the card

Folders containing the json flashcard files must have the word 'flashcards' in the folder name
