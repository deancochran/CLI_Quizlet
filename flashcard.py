import json
import os

class Flashcard():
    def __init__(self,obj: dict, flashcards_path:str, card_index:int):
        self.flashcards_path=flashcards_path
        self.card_index=card_index
        self.q = obj['q']
        self.a = obj['a']
        self.skips=0
        self.flips=0
        self.side=0

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

    def to_json(self):
        return {'q':self.q, 'a':self.a}

    def save(self, flashcards_path: str):
        file_path = os.path.join(flashcards_path, f"card_{self.card_index}"+'.json')
        with open(file_path, "w") as f:
            f.write(json.dumps(self.to_json()))

    def remove(self):
        card_path = os.path.join(self.flashcards_path, f"card_{self.card_index}"+'.json')
        os.remove(card_path)

    def prompt_user(self, key='q'):
        if key == 'q':
            keyword='Question'
        else:
            keyword='Answer'
        flag=False
        while flag==False:
            qa = str(input(f'Enter a {keyword}: '))
            done=False
            while done==False:
                yn = str(input(f'Is your {keyword}: "{qa}" correct (Y/N): '))
                if yn.lower()=="y":
                    flag=True
                    done=True
                elif yn.lower()=="n":
                    flag=False
                    done=True
                else:
                    print('\r\r', end='')
        return qa

    def show_editor(self):
        os.system('clear')
        print('Card Editor View')
        print(' ')
        print('Question: ', self.q)
        print('Answer: ', self.a)
        print('')
        print(f"""Action Keys: quit == " enter ", edit Answer == " A ",edit Question == " Q " """)

    def edit(self):
        flag=False
        while flag==False:
            self.show_editor()
            done=False
            while done==False:
                key = str(input(f'Enter a Action Key: '))
                if key == "":
                    pass
                elif key.lower() == "a":
                    self.set_a(self.prompt_user(key='a'))
                    self.show_editor() 
                elif key.lower() == "q":
                    self.set_a(self.prompt_user(key='q'))
                    self.show_editor() 
                else:
                    self.show_editor()
