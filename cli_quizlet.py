from fileinput import filename
import random
import json
import os
import time
import datetime

class Flashcard():
    def __init__(self,obj: dict):
        self.q = obj['q']
        self.a = obj['a']
        self.skips=0
        self.flips=0
        self.side=0

    def flip(self):
        if self.side == 0:
            self.side = 1
        else:
            self.side = 0

    def set_q(self, question):
        self.q=question

    def set_a(self, answer):
        self.a = answer

    def show(self):
        if self.side == 0:
            print(f'Question: {self.q}')
        else:
            print(f'Answer: {self.a}')

    def to_json(self):
        return {'q':self.q, 'a':self.a}

    def save(self, flashcards_path, card_filename):
        file_path = os.path.join(flashcards_path, card_filename)
        with open(file_path, "w") as f:
            f.write(json.dumps(self.to_json()))
    
class Deck(): 
    def __init__(self,flashcard_folders_dir):
        self.flashcard_folders_dir=flashcard_folders_dir
        self.load_flashcard_path()

    @property
    def size(self):
        return len(self.deck.keys())

    def get_card(self,card_name: str):
        card_path = os.path.join(self.flashcards_path, card_name)
        obj=json.loads(open(card_path,"rb").read())
        return Flashcard(obj)
    
    def add_card(self, obj):
        assert obj is dict
        card = Flashcard(obj)
        card.save(self.flashcards_path, f'card_{self.size}')

    def remove_card(self, card_name):
        card_path = os.path.join(self.flashcards_path, card_name)
        os.remove(card_path)

    def load_flashcard_path(self):
        assert os.path.exists(self.flashcard_folders_dir) == True
        assert len(os.listdir(self.flashcard_folders_dir)) > 0
        available_decks={filename.split('.')[0]: filename for filename in os.listdir(self.flashcards_dir)}
        flag=False
        while flag==False:
            print('Available Decks: ',list(available_decks.keys()))
            name = str(input('Enter a Deck Name: '))
            if name in list(available_decks.keys()):
                self.name=name
                flag=True
        self.flashcards_path = f'{self.flashcards_dir}/{available_decks[name]}'
        print(f'Loaded Deck: {self.name} from {self.flashcards_dir}, Size: {self.size}')

class Quiz():
    def __init__(self, deck: Deck, results_dir):
        self.deck=deck
        self.results_dir=results_dir
        self.start_size=self.deck.size       
        self.answered=0
        self.first_card_shown=False
        self.cards=[]
        self.answered_cards=[]
        self.load_deck()
        self.start()
        self.show_quiz()
        
    def get_rand_card(self):
        return random.sample(self.cards, 1)[0]
        
    def show_action_keys(self):
        print(f"""Action Keys: skip == " enter ", flip== " ' ", remove == " ; " """)

    def show_quiz_status(self):
        complete=self.answered/self.start_size
        print(f'Finished {complete:.2f}% of Deck: "{self.deck.name}"')

    def load_deck(self):
        for card_name in os.listdir(self.deck.flashcards_path):
            self.cards.append(self.deck.get_card(card_name))

    def start(self):
        for i in reversed(range(5)):
            os.system ('clear')
            if i == 0:
                print(f'Deck: {self.deck.name} Size: {self.start_size} cards')
                print(f'Starting Flashcard quiz in.. {i}')
            else:
                print(f'GO!')
            time.sleep(1)
        self.start_time=datetime.datetime.now()
    
    def skip(self):
        self.key_press=True
        self.current_card.skips+=1
        self.current_card = self.get_rand_card()
        self.show_quiz()
        
    def flip_card(self):
        self.key_press=True
        self.current_card.flips+=1
        self.current_card.flip()
        self.show_quiz()

    def remove_card(self):
        self.key_press=True
        self.answered+=1
        self.answered_cards.append(self.cards.pop(self.cards.index(self.current_card)))
        if len(self.answered) != self.start_size:
            self.current_card = self.get_rand_card()
            self.show_quiz()
        else:
            self.end_time=datetime.datetime.now()   
            self.show_quiz_results()

    def get_input(self):
        key = str(input('Input Key: '))
        if key == "":
            self.skip()
        elif key == "'":
            self.flip_card()
        elif key == ";":
            self.remove_card()    
        else:
            print('\r',end='')
            self.get_input()

    def show_quiz(self):
        os.system ('clear')
        self.show_quiz_status()
        self.show_action_keys()
        print(' ')
        self.current_card.show()
        self.get_input()

    def show_quiz_results(self):
        os.system ('clear')
        self.show_quiz_status()
        self.total_time = self.end_time-self.start_time
        print(f"Time: {self.total_time}")
        self.save_quiz_results()

    def to_json(self):
        data={}
        for card in self.answered_cards:
            data[card.q]={
                    'answer':card.a,
                    'flips':card.flips,
                    'skips':card.skips,
                }
        data['time']=str(self.total_time)
        return data

    def save_quiz_results(self):
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        quiz_name = self.deck.name+'_'+str(datetime.datetime.now().today())
        quiz_results_file_path=self.results_dir+f'/{quiz_name}.json'
        with open(quiz_results_file_path, "w") as f:
            f.write(json.dumps(self.to_json()))
        print(f'Saved Quiz to {quiz_results_file_path}')

if __name__ == "__main__":
    os.system('clear')
    deck=Deck(decks_dir='decks')
    decks={filename.split('.')[0]: filename for filename in os.listdir('decks')}
    flag=False
    while flag==False:
        print('Available Decks: ',list(decks.keys()))
        name = str(input('Enter a Deck Name: '))
        if name in list(decks.keys()):
            flag=True
    deck.load_deck(f'decks/{decks[name]}')
    time.sleep(5)
    Quiz(deck, 'results')