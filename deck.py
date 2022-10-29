import json
import os
from tabnanny import verbose
import time
from numpy import max
import uuid
from flashcard import Flashcard
from quiz import Quiz
class Deck():
    """
        Deck is a class object that represents a collection of Flashcard objects that can be sorted, 
        shuffled, and collected via their index position
    """
    def __init__(self, flashcards_root_dir):
        assert os.path.exists(flashcards_root_dir) == True
        self.root_path = flashcards_root_dir
        self.flashcards_path = None
        self.current_card_index=0
        self.deck_editor()

    def deck_loaded(self):
        return self.root_path != None

    def read_cards(self):
        with open(self.flashcards_path, 'r') as f:
            card_set = json.load(f)
        return [Flashcard(uuid, obj) for uuid, obj in card_set.items()]

    def quiz_me(self):
        Quiz(name=self.name, cards=self.read_cards(), results_dir=os.path.join(self.root_path, 'results'))

    def set_flashcards_path(self):
        print(os.listdir(self.root_path))
        available_decks={i: filename for i, filename in enumerate([deck for deck in os.listdir(self.root_path) if 'flashcards.json' in deck])}
        assert len(available_decks) > 0
        flag=False
        while flag==False:
            os.system("clear")
            print('Available Decks: ')
            for i, name in available_decks.items():
                print(f'{i}: {name}')
            print(' ')
            str_id = input('Enter a Deck id: ')
            if str_id.isdigit():
                id=int(str_id)
                if id in available_decks.keys():
                    self.name=available_decks[id].split('.')[0]
                    flag=True
            
        self.flashcards_path = f'{self.root_path}/{self.name}.json'

    def deck_editor(self,verbose=False):
        os.system('clear')
        print('Deck Editor View','\n')
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        if self.flashcards_path == None:
            print(f'Deck Editor located at path: {self.root_path}')
            print(f'No Deck Loaded')
        else:
            print(f'Deck Editor located at path: "{self.root_path}"')
            print(f'Deck {self.name} has path: "{self.flashcards_path}"')
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        if verbose:
            print('Loading a deck with at least one card is required to edit and quiz ')
        else:
            print(' ')
        print(f"""Action Keys: quit == " enter ", load deck == " L ", edit deck == " E ", take a quiz == " Q ", new deck == " N " """)
                
        key = str(input('Action Key: '))
        if key == "":
            print('Closing Editor')
        elif key.lower() == "l":
            self.set_flashcards_path()
            self.deck_editor()
            
        elif key.lower() == "q":
            if self.deck_loaded() == True and len(self.read_cards())>0:
                self.quiz_me()
            else:
                self.deck_editor(verbose=True)
                
        elif key.lower() == "e":
            if self.deck_loaded():
                self.flashcard_editor()
                self.deck_editor()
            else:
                self.deck_editor(verbose=True)
                
        elif key.lower() == "n":
            self.make_new_deck()
            self.deck_editor()
        else:
            self.deck_editor(verbose=True)

    def make_new_deck(self):
        os.system("clear")
        flag=False
        while flag==False:
            self.name = str(input('What do you want to call your ~new~ deck: '))
            self.flashcards_path = f'{self.root_path}/{self.name}.json'
            os.system("clear")
            if os.path.exists(f'{self.flashcards_path}'):
                print(f'A Deck with {self.name} already exists. Please enter a different name')
            elif "flashcards" != self.name.split('_')[-1]:
                print(f'A Deck must end with "_flashcards" or be called "flashcards". Please adjust your name')
            else:
                yn = str(input(f'Is {self.name} correct (Y/N): '))
                if yn.lower()=="y":
                    flag=True
                elif yn.lower()=="n":
                    flag=True
                    return True
                else:
                    pass
        with open(f'{self.flashcards_path}', 'w') as f:
            json.dump(dict(),f)
            
    def save_cards(self, cards):
        with open(f'{self.flashcards_path}', 'w') as f:
            data={}
            for card in cards.values():
                obj=card.to_json()
                data[obj['id']]=obj['qa']
            json.dump(data,f, indent=4)

    def flashcard_editor(self, card_set = None):
        if card_set != None:
            cards = {i: flashcard for i, flashcard in enumerate(card_set.values())} 
        else:
            cards = {i: flashcard for i, flashcard in enumerate(self.read_cards())} 
        os.system('clear')
        self.size = len(cards)
        print(f'Deck {self.name} has {self.size} cards')
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        if self.size>0:
            current_card=cards[self.current_card_index]
            print(f'Current Card Index: {self.current_card_index}')
            print('Question: ',current_card.get_q())
            print('Answer: ',current_card.get_a())
            print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        print(' ')
        print(f"""Action Keys: next card == " enter ", edit card == " E ", add card == " A ", remove card == " R ", exit == " Q " """)
        key = str(input('Action Key: '))
        if key == "" and self.size>0:
            self.current_card_index = (self.current_card_index+1)%len(cards)
            self.flashcard_editor(cards)
        elif key.lower() == "e" and self.size>0:
            cards[self.current_card_index].edit()
            self.flashcard_editor(cards)
        elif key.lower() == "a":
            id=str(uuid.uuid4())
            obj={'q':'new question...','a':'new answer...'}
            card=Flashcard(id, obj)
            card.edit()
            if self.size == 0:
                card_index = 0
            else:
                card_index = max(list(cards.keys())) + 1
            cards[card_index] = card
            self.flashcard_editor(cards)
        elif key.lower() == "r" and self.size>0:
            del cards[self.current_card_index]
            if len(cards) != 0:
                self.flashcard_editor(cards)
            else:
                os.remove(self.flashcards_path)
        elif key.lower() == "q":
            self.save_cards(cards)
        else:
            self.flashcard_editor()
            
if __name__ == "__main__":
    Deck('./flashcards')    
