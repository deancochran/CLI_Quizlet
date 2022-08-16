import json
import os

from flashcard import Flashcard
from quiz import Quiz
class Deck(): 
    def __init__(self,flashcard_folders_dir):
        self.flashcard_folders_dir=flashcard_folders_dir
        self.flashcards_path=None
        self.deck_editor()

    @property
    def size(self):
        return len(os.listdir(self.flashcards_path))

    def deck_loaded(self):
        return self.flashcards_path != None

    def set_flashcards_path(self):
        assert os.path.exists(self.flashcard_folders_dir) == True
        assert len(os.listdir(self.flashcard_folders_dir)) > 0
        available_decks=[filename for filename in os.listdir(self.flashcard_folders_dir) if 'flashcards' in filename and '.' not in filename]
        flag=False
        while flag==False:
            os.system("clear")
            print('Available Decks: ',list(available_decks))
            name = str(input('Enter a Deck Name: '))
            if name in list(available_decks):
                self.name=name
                flag=True
        self.flashcards_path = f'{self.flashcard_folders_dir}/{name}'

    def read_cards(self):
        return [Flashcard(json.loads(open(os.path.join(self.flashcards_path, card_filename),"rb").read()), self.flashcards_path, i) for i, card_filename in enumerate(os.listdir(self.flashcards_path))]

    def flashcard_editor(self):
        os.system('clear')
        cards=self.read_cards()
        assert self.size == len(cards)
        print(f'Deck {self.name} has {self.size} cards')
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        print('len(cards)',len(cards))
        print('self.current_card_index',self.current_card_index)
        current_card_obj=cards[self.current_card_index].to_json()
        print('Current Card:')
        print('Question: ',current_card_obj['q'])
        print('Answer: ',current_card_obj['a'])
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        print(' ')
        print(f"""Action Keys: next card == " enter ", edit card == " E ", add card == " A ", remove card == " R ", exit == " Q " """)
        key = str(input('Action Key: '))
        if key == "":
            self.current_card_index = (self.current_card_index+1)%len(cards)
            self.flashcard_editor()
        elif key.lower() == "e":
            cards[self.current_card_index].edit()
            cards[self.current_card_index].save()
            self.flashcard_editor()
        elif key.lower() == "a":
            card=Flashcard({'q':'New Card','a':'New Card Answer'}, self.flashcards_path, len(cards))
            card.edit()
            card.save()
            self.flashcard_editor()
        elif key.lower() == "r":
            card=cards.pop(self.current_card_index)
            card.remove()
            if len(cards)>0:
                for i, card in enumerate(cards):
                    card.remove()
                    card.set_card_index(i)
                    card.save()
                self.current_card_index = (self.current_card_index+1)%len(cards)
                self.flashcard_editor()
            else:
                os.rmdir(self.flashcards_path)
        elif key.lower() == "q":
            pass
        else:
            self.flashcard_editor()

    def quiz_me(self, results_dir='results'):
        Quiz(name=self.name, cards=self.read_cards(), results_dir=results_dir)

    def make_new_deck(self):
        os.system("clear")
        flag=False
        while flag==False:
            self.name = str(input('What do you want to call your ~new~ deck: '))
            os.system("clear")
            if os.path.exists(f'{self.flashcard_folders_dir}/{self.name}'):
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
        self.flashcards_path = f'{self.flashcard_folders_dir}/{self.name}'
        if os.path.exists(self.flashcards_path) == False:
            os.mkdir(self.flashcards_path)
        card=Flashcard({'q':'This is your first card','a':'You can add more once this is made'}, self.flashcards_path, len(self.read_cards()))
        card.edit()
        card.save()

    def deck_editor(self,verbose=False):
        os.system('clear')
        print('Deck Editor View','\n')
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        if self.flashcards_path == None:
            print(f'Deck Editor located at path: {self.flashcard_folders_dir}')
            print(f'No Deck Loaded')
        else:
            print(f'Deck Editor located at path: "{self.flashcard_folders_dir}"')
            print(f'Deck {self.name} has path: "{self.flashcards_path}"')
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        if verbose:
            print('Loading a deck is required to edit and quiz ')
        else:
            print(' ')
        print(f"""Action Keys: quit == " enter ", load deck == " L ", edit deck == " E ", take a quiz == " Q ", new deck == " N " """)
                
        key = str(input('Action Key: '))
        if key == "":
            print('Closing Editor')
        elif key.lower() == "l":
            self.set_flashcards_path()
            self.deck_editor()
        elif key.lower() == "e":
            if self.deck_loaded():
                self.current_card_index = 0
                self.flashcard_editor()
                self.deck_editor()
            else:
                self.deck_editor(verbose=True)
        elif key.lower() == "q":
            if self.deck_loaded() == True:
                self.quiz_me()
                self.deck_editor()
            else:
                self.deck_editor(verbose=True)
        elif key.lower() == "n":
            self.make_new_deck()
            self.current_card_index = 0
            self.flashcard_editor()
            self.deck_editor()
        else:
            self.deck_editor(verbose=True)

        
