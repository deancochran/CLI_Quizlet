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
        assert self.deck_loaded == True
        return len(os.listdir(self.flashcards_path))

    def deck_loaded(self):
        if self.flashcards_path == None:
            return False
        else:
            return True

    def load_flashcards(self):
        assert os.path.exists(self.flashcard_folders_dir) == True
        assert len(os.listdir(self.flashcard_folders_dir)) > 0
        os.system("clear")
        yn = str(input(f'Do you want to load a deck (Y/N): '))
        if yn.lower()=="y":
            available_decks=[filename for filename in os.listdir(self.flashcard_folders_dir) if 'flashcards' in filename and '.' not in filename]
            flag=False
            while flag==False:
                print('Available Decks: ',list(available_decks))
                name = str(input('Enter a Deck Name: '))
                if name in list(available_decks):
                    self.name=name
                    flag=True
            self.flashcards_path = f'{self.flashcard_folders_dir}/{name}'
            return True
        elif yn.lower()=="n":
            return False
        else:
            self.load_flashcards()


    def deck_editor(self):
        '''
        deck_editor is a self looping cli that allows the use to...
            - load a existing deck of flashcards from the provided directory
            - make a new deck of flashcards in the provided directory
        '''
        os.system('clear')
        print('Deck Editor View','\n')
        if self.deck_loaded==False:
            print(f'Deck Editor located at path: {self.flashcard_folders_dir}')
            print(f'No Deck Loaded')
        else:
            print(f'Deck Editor located at path: {self.flashcard_folders_dir}')
            print(f'Deck {self.name} Loaded with path: {self.flashcards_path}')
        print(f"""Action Keys: quit == " enter ", load deck == " L ", edit deck == " E ", take a quiz == " Q ", new deck == " N " """)
        
        key = str(input('Action Key: '))
        if key == "":
            pass
        elif key.lower() == "l":
            self.load_flashcards()
            self.deck_editor()
        elif key.lower() == "e":
            if self.deck_loaded():
                self.flashcard_editor()
            self.deck_editor()
        elif key.lower() == "q":
            if self.deck_loaded():
                self.quiz_me()
        elif key.lower() == "n":
            raise Exception('not implemented')
        else:
            self.get_editor_input()

    # def get_card(self,card_name: str):
    #     card_path = os.path.join(self.flashcards_path, card_name)
    #     obj=json.loads(open(card_path,"rb").read())
    #     return Flashcard(obj)

    # def question_prompt(self):
    #     flag=False
    #     while flag==False:
    #         q = str(input('Enter a Question: '))
    #         done=False
    #         while done==False:
    #             yn = str(input(f'Is your Question "{q}" correct (Y/N): '))
    #             if yn.lower()=="y":
    #                 flag=True
    #                 done=True
    #             elif yn.lower()=="n":
    #                 flag=False
    #                 done=True
    #             else:
    #                 print('\r\r', end='')
    #     return q

    # def answer_prompt(self):
    #     flag=False
    #     while flag==False:
    #         a = str(input('Enter a Answer: '))
    #         done=False
    #         while done==False:
    #             yn = str(input(f'Is your Answer "{a}" correct (Y/N): '))
    #             if yn.lower()=="y":
    #                 flag=True
    #                 done=True
    #             elif yn.lower()=="n":
    #                 flag=False
    #                 done=True
    #             else:
    #                 print('\r\r', end='')
    #     return a

    # def add_card_(self):
    #     q=self.question_prompt()
    #     a=self.answer_prompt()
    #     self.add_card({'q':q,"a":a})

    # def add_card(self, obj: dict):
    #     card = Flashcard(obj)
    #     if self.size == 0:
    #         os.mkdir(self.flashcards_path)
    #     card.save(self.flashcards_path, self.size)

    # def remove_card(self, card_name):
    #     card_path = os.path.join(self.flashcards_path, card_name)
    #     os.remove(card_path)


    # def quiz_me(self, results_dir='results'):
    #     Quiz(self, results_dir)

    # def show_card_maker(self):
    #     os.system ('clear')
    #     print(f'Making Deck "{self.name}, Current Size: {self.size} cards"')
    #     print(f"""Action Keys: quit == " enter ", add card == " A " """)
    #     print(' ')
    #     key = str(input('Action Key: '))
    #     if key == "":
    #         if self.size==0:
    #             print(f'Did not save Deck "{self.name}"')
    #         else:
    #             print(f'Finished Deck "{self.name} with {self.size} cards!"')
    #     elif key.lower() == "a":
    #         self.add_card_()
    #         self.show_card_maker() 
    #     else:
    #         self.get_card_maker_input()

        


    # def make_new_deck(self):
    #     os.system("clear")
    #     flag=False
    #     while flag==False:
    #         self.name = str(input('What do you want to call your deck: '))
    #         os.system("clear")
    #         if os.path.exists(f'{self.flashcard_folders_dir}/{self.name}'):
    #             print(f'A Deck with {self.name} already exists. Please enter a different name')
    #         else:
    #             yn = str(input(f'Is {self.name} correct (Y/N): '))
    #             if yn.lower()=="y":
    #                 flag=True
    #             elif yn.lower()=="n":
    #                 flag=True
    #                 return True
    #             else:
    #                 pass
    #     self.flashcards_path = f'{self.flashcard_folders_dir}/{self.name}'
    #     self.show_card_maker()


    


    # def flashcard_editor(self):
    #     os.system('clear')
    #     card_filenames = {i: card_filename }
    #     cards = []
    #     for card_filename in os.listdir(self.flashcards_path):
    #         card_path = os.path.join(self.flashcards_path, card_filenames[self.current_card_index])
    #         cards.append((card_filename,Flashcard(json.loads(open(card_path,"rb").read()))))
    #     print(f'Deck {self.name} has {self.size} cards')
    #     print(f"""Action Keys: next card == " enter ", edit card == " E ", remove card == " R ", exit == " Q " """)
    #     print('\n')
        
    #     print('Current Card:',cards[self.current_card_index].to_json())

    #     key = str(input('Action Key: '))
    #     if key == "":
    #         raise Exception('next card')
    #     elif key.lower() == "e":
    #         current_card.edit()
    #         current_card.save(self.)
    #     elif key.lower() == "r":
    #         raise Exception('remove card')
    #     elif key.lower() == "q":
    #         pass
    #     else:
    #         self.flashcard_editor()



        
