# CLI_Quizlet
A simple cli flashcard quiz, with JSON formatted flashcard files

# How to use 
Welcome.

To use this repository to its full extent, you will want to import the Deck() class into your desired directory...

    from deck import Deck

All that is left is to start the class looping function by providing the class object with a path to any directory that you want to make flashcards inside of, or where you have already made flashcards.

    Deck('./path/to/flashcard/files/')

This will start the Command Line Interface (CLI) interface, allowing you to quickly and precisely create/update/save/remove flashcards from your files (all flashcard files should be in the format **someFileName**_flashcards.json). 

# Quizing yourself
This is the real bread and butter of this project. While your CLI is running, you have the ability to test yourself on any of your pre-made flashcard sets.

After running the quiz within the CLI interface, your results will be saved in a 'results' folder inside the directory you passed to initialize the Deck object (all results should be in the format **someFileName**_flashcards_**theCurrenTimeOfDay**.json).

## Plans for later updates
- Better interface functions
- Better performance functions
- functions to analyze results
    - find the questions that with the most skips and flips
- functions to provide analysis on results after a quiz
