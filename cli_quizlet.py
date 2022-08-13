import random
import json
import os
import time
import datetime

class Flashcard():
    def __init__(self, q=None, a=None, obj=None):
        if obj is None:
            assert type(q) is str
            assert type(a) is str
            self.q = q
            self.a = a
            self.side = 0
        else:
            assert type(obj) is dict
            self.q = obj['q']
            self.a = obj['a']
            self.side = 0
        self.skips=0
        self.flips=0

    def set_q(self, question):
        self.q=question

    def set_a(self, answer):
        self.a = answer

    def flip(self):
        if self.side == 0:
            self.side = 1
        else:
            self.side = 0

    def show(self):
        if self.side == 0:
            print(f'Question: {self.q}')
        else:
            print(f'Answer: {self.a}')

    def read_json(self, obj):
        self.question = obj['q']
        self.answer = obj['a']

    def to_json(self):
        return {
            'q':self.q,
            'a':self.a
            }




class Deck():
    def __init__(self, decks_dir, name='deck'):
        self.decks_dir=decks_dir
        self.name = name
        self.deck = {}

    @property
    def size(self):
        return len(self.deck)

    def items(self):
        return self.deck.items()

    def add_card(self, card: Flashcard):
        self.deck[self.size] = card

    def get_card(self, bad_keys=None):
        if bad_keys is None:
            keys = list(self.deck.keys())
            card_key = random.sample(keys, 1)[0]
            return card_key, self.deck[card_key]
        else:
            keys = [key for key in list(self.deck.keys()) if key not in bad_keys]
            card_key = random.sample(keys, 1)[0]
            return card_key, self.deck[card_key]

    def remove_card(self, card_key):
        self.deck.pop(card_key)

    def is_empty(self):
        if self.deck == {}:
            return True
        else:
            return False

    def load_flashcards(self, flashcards_path):
        flashcard_filenames = os.listdir(flashcards_path)
        for filename in flashcard_filenames:
            card_path=flashcards_path+f'/{filename}'
            obj=json.loads(open(card_path,"rb").read())
            card=Flashcard(obj=obj)
            self.add_card(card)
        print(f'Loaded Flashcards from {flashcards_path}')

    def load_deck(self, deck_path):
        self.name=deck_path.split("/")[-1].split(".")[0]
        obj=json.loads(open(deck_path,"rb").read())
        for _, v in obj.items():
            self.add_card(Flashcard(obj=v))
        print(f'Loaded Deck: {self.name}')
        
    def save_deck(self):
        if not os.path.exists(self.decks_dir):
            os.makedirs(self.decks_dir)
        filename=self.decks_dir+f"/{self.name}.json"
        with open(filename, "w") as f:
            f.write(json.dumps(self.to_json()))
        print(f'Saved Deck to {self.decks_dir}')

    def to_json(self):
        return {k:v.to_json() for k,v in self.items()}
            
class Quiz():
    def __init__(self, deck: Deck, results_dir):
        self.deck=deck
        self.results_dir=results_dir
        self.start_size=self.deck.size       
        self.answered=0
        self.current_card_key,self.current_card = deck.get_card()
        self.removed_card_keys=[]
        self.show_cli()
        self.show_quiz()

    def show_cli(self):
        os.system ('clear')
        print('Starting Flashcard quiz...')
        print(f'Deck: {self.deck.name} Size: {self.start_size} cards')
        time.sleep(2)
        self.start_time=datetime.datetime.now()
        
    def action_keys_info(self):
        print(f"""Action Keys: skip == " enter ", flip== " ' ", remove == " ; " """)

    def quiz_status(self):
        complete=self.answered/self.start_size
        print(f'Finished {complete:.2f}% of Deck: "{self.deck.name}"')

    def show_current_card(self):
        self.current_card.show()

    def skip(self):
        self.key_press=True
        self.current_card.skips+=1
        self.current_card_key,self.current_card = self.deck.get_card(bad_keys=self.removed_card_keys)
        self.show_quiz()
        
    def flip_card(self):
        self.key_press=True
        self.current_card.flips+=1
        self.current_card.flip()
        self.show_quiz()

    def remove_card(self):
        self.key_press=True
        self.answered+=1
        self.removed_card_keys.append(self.current_card_key)
        if len(self.removed_card_keys) != self.start_size:
            self.current_card_key,self.current_card = self.deck.get_card(bad_keys=self.removed_card_keys)
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

    def show_quiz_results(self):
        os.system ('clear')
        self.quiz_status()
        self.total_time = self.end_time-self.start_time
        print(f"Time: {self.total_time}")
        self.save_quiz_results()
        
    def show_quiz(self):
        os.system ('clear')
        self.quiz_status()
        self.action_keys_info()
        print(' ')
        self.show_current_card()
        self.get_input()

    def save_quiz_results(self):
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        quiz_name = self.deck.name+'_'+str(datetime.datetime.now().today())
        quiz_results_file_path=self.results_dir+f'/{quiz_name}.json'
        with open(quiz_results_file_path, "w") as f:
            f.write(json.dumps(self.to_json()))
        print(f'Saved Quiz to {quiz_results_file_path}')

    def to_json(self):
        data={}
        for card_id, card in self.deck.items():
            data[card_id]={
                    'question':card.q,
                    'answer':card.a,
                    'flips':card.flips,
                    'skips':card.skips,
                }
        data['time']=str(self.total_time)
        return data

if __name__ == "__main__":
    deck=Deck(decks_dir='decks', name="Demov2" )
    deck.load_deck('decks/dean.json')
    deck.save_deck()

    print('\n')
    Quiz(deck, 'results')