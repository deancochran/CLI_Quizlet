import random
import json
import os
import time
import datetime
import uuid

class Flashcard():
    def __init__(self, obj:dict):
        if self.load(obj) == False:
            raise Exception('Obj is empty or not valid')
        
    def set_id(self, identifier:str):
        self.id=identifier
        
    def set_a(self, answer:str):
        self.a = answer
        
    def set_q(self, question:str):
        self.q = question
        
    def get_id(self):
        return self.id
        
    def get_a(self):
        return self.a 
        
    def get_q(self):
        return self.q 
    
    def load(self, obj:dict):
        if self.id_isValid(obj.id) and self.qa_isValid(obj.q) and self.qa_isValid(obj.a):
            self.set_id(obj.id) 
            self.set_q(obj.q) 
            self.set_a(obj.a)    
            return True
        else:
            return False

    def id_isValid(id:str):
        # check for uuid format
        try:
            uuid_obj = uuid.UUID(id, version=4)
        except ValueError:
            return False
        return str(uuid_obj) == id

    def qa_isValid(qa:str):
        # Check for valid answer -- unrestricted
        if qa == None:
            return False
        elif qa.strip(' ') == "":
            return False
        else:
            return True

class Deck():
    def __init__(self, file_path:str):
        if self.load(file_path) == False:
            raise Exception('Path to File does not exist')
    def load(self):
        if os.path.exists(self.file_path) is True:
            self.cards=[Flashcard(obj) for obj in json.load(self.file_path)]
            return True
        else:
            return False
            
    

# class Quiz():
#     def __init__(self, deck: Deck, results_dir):
#         self.deck=deck
#         self.results_dir=results_dir
#         self.start_size=self.deck.size       
#         self.answered=0
#         self.first_card_shown=False
#         self.cards=[]
#         self.answered_cards=[]
#         self.load_deck()
#         self.start_quiz()
#         self.show_quiz()
        
#     def get_rand_card(self):
#         return random.sample(self.cards, 1)[0]
        
#     def show_action_keys(self):
#         print(f"""Action Keys: skip == " enter ", flip== " ' ", remove == " ; " """)

#     def show_quiz_status(self):
#         complete=self.answered/self.start_size
#         print(f'Finished {complete:.2f}% of Deck: "{self.deck.name}"')

#     def load_deck(self):
#         for card_name in os.listdir(self.deck.flashcards_path):
#             self.cards.append(self.deck.get_card(card_name))

#     def start_quiz(self):
#         for i in reversed(range(5)):
#             os.system ('clear')
#             if i != 0:
#                 print(f'Deck: {self.deck.name} Size: {self.start_size} cards')
#                 print(f'Starting Flashcard quiz in.. {i}')
#                 time.sleep(1)
#             else:
#                 print(f'GO!')
#                 time.sleep(1)
#         self.start_time=datetime.datetime.now()
#         self.current_card=self.get_rand_card()
    
#     def skip(self):
#         self.key_press=True
#         self.current_card.skips+=1
#         self.current_card = self.get_rand_card()
#         self.show_quiz()
        
#     def flip_card(self):
#         self.key_press=True
#         self.current_card.flips+=1
#         self.current_card.flip()
#         self.show_quiz()

#     def remove_card(self):
#         self.key_press=True
#         self.answered+=1
#         self.answered_cards.append(self.cards.pop(self.cards.index(self.current_card)))
#         if self.answered != self.start_size:
#             self.current_card = self.get_rand_card()
#             self.show_quiz()
#         else:
#             self.end_time=datetime.datetime.now()   
#             self.show_quiz_results()

#     def get_input(self):
#         key = str(input('Action Key: '))
#         if key == "":
#             self.skip()
#         elif key == "'":
#             self.flip_card()
#         elif key == ";":
#             self.remove_card()    
#         else:
#             print('\r',end='')
#             self.get_input()

#     def show_quiz(self):
#         os.system ('clear')
#         self.show_quiz_status()
#         self.show_action_keys()
#         print(' ')
#         self.current_card.show()
#         self.get_input()

#     def show_quiz_results(self):
#         os.system ('clear')
#         self.show_quiz_status()
#         self.total_time = self.end_time-self.start_time
#         print(f"Time: {self.total_time}")
#         self.save_quiz_results()

#     def to_json(self):
#         data={}
#         for card in self.answered_cards:
#             data[card.q]={
#                     'answer':card.a,
#                     'flips':card.flips,
#                     'skips':card.skips,
#                 }
#         data['time']=str(self.total_time)
#         return data

#     def save_quiz_results(self):
#         if not os.path.exists(self.results_dir):
#             os.makedirs(self.results_dir)
#         quiz_name = self.deck.name+'_'+str(datetime.datetime.now().today())
#         quiz_results_file_path=self.results_dir+f'/{quiz_name}.json'
#         with open(quiz_results_file_path, "w") as f:
#             f.write(json.dumps(self.to_json()))
#         print(f'Saved Quiz to {quiz_results_file_path}')

# if __name__ == "__main__":
#     os.system('clear')
#     deck=Deck('.')
#     while deck.flashcards_path == None:
#         deck=Deck('.')

    
        
        