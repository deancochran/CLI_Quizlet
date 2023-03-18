import datetime
import random
import time
import json
import os
from flashcard import Flashcard

class Quiz():
    """
        Quiz is a class object to utilize deck objects to provide a CLI interface for the user to perform 
        a quiz on the preloaded flashcards
    """
    def __init__(self, name, cards, results_dir):
        self.results_dir=results_dir
        self.name=name
        self.cards=[card for card in cards]
        self.answered_cards=[]
        self.start_size=len(cards)      
        self.answered=0
        self.start_quiz()
        
    def get_rand_card(self) -> Flashcard:
        return random.choice(self.cards)
        
    def get_input(self):
        key = str(input('Action Key: '))
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
        complete=self.answered/self.start_size
        print(f'Finished {complete:.2f}% of Deck: "{self.name}"')
        print(f"""Action Keys: skip == " enter ", flip== " ' ", remove == " ; " """)
        print(' ')
        self.current_card.show()
        self.get_input()

    def remove_card(self):
        self.answered+=1
        self.current_card.end_timer()
        self.answered_cards.append(self.cards.pop(self.cards.index(self.current_card)))
        if self.answered != self.start_size:
            self.current_card = self.get_rand_card()
            self.current_card.start_timer()
            self.show_quiz()
        else:
            self.end_time=datetime.datetime.now()   
            self.show_quiz_results()

    def flip_card(self):
        self.current_card.flips+=1
        self.current_card.flip()
        self.show_quiz()

    def skip(self):
        self.current_card.skips+=1
        self.current_card.end_timer()
        self.current_card = self.get_rand_card()
        self.current_card.start_timer()
        self.show_quiz()   
        

    def to_json(self):
        columns = ['card_id','question','answer','flips', 'skips', 'card_time']
        data={col:list() for col in columns}
        for col in columns:
            for card in self.answered_cards:
                if col == 'card_id': 
                    data[col].append(card.id)
                elif col == 'question': 
                    data[col].append(card.q)
                elif col == 'answer': 
                    data[col].append(card.a)
                elif col == 'flips': 
                    data[col].append(card.flips)
                elif col == 'skips': 
                    data[col].append(card.skips)
                elif col == 'card_time': 
                    data[col].append(card.elapsed_time)
                else:
                    raise Exception('attribute of card result == "{col}" is not implemented')
        return data

    def save_quiz_results(self):
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        quiz_name = self.name+'_'+str(datetime.datetime.now().today())
        quiz_results_file_path=self.results_dir+f'/{quiz_name}.json'
        with open(quiz_results_file_path, "w") as f:
            f.write(json.dumps(self.to_json()))
        print(f'Saved Quiz to {quiz_results_file_path}')

    def show_quiz_results(self):
        os.system ('clear')
        complete=self.answered/self.start_size
        print(f'Finished {complete:.2f}% of Deck: "{self.name}"')
        self.total_time = self.end_time-self.start_time
        print(f"Time: {self.total_time}")
        self.save_quiz_results()
        time.sleep(3)

    def start_quiz(self):
        for i in reversed(range(5)):
            os.system ('clear')
            if i != 0:
                print(f'Deck: {self.name} Size: {self.start_size} cards')
                print(f'Starting Flashcard quiz in.. {i}')
                time.sleep(1)
            else:
                print(f'GO!')
                time.sleep(1)
        self.start_time=datetime.datetime.now()
        self.current_card = self.get_rand_card()
        self.current_card.start_timer()
        self.show_quiz()
 
