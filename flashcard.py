import os
class Flashcard():
    """
        Flashcard is a class that represents a single question and answer set which can be identified by
        its unique uuid identifier
    """
    def __init__(self, id, obj:dict):
        self.id = str(id)
        self.q = str(obj['q'])
        self.a = str(obj['a'])
        self.flips=0
        self.skips=0
        self.side = 0
    
    def get_q(self) -> str:
        return self.q

    def get_a(self) -> str:
        return self.a

    def get_id(self) -> str:
        return self.id

    def set_q(self, question):
        self.q = question

    def set_a(self, answer):
        self.a = answer

    def flip(self):
        if self.side == 0:
            self.side = 1
        else:
            self.side = 0

    def to_json(self):
        return {'id':self.id, 'qa':{'q':self.q, 'a':self.a}}

    def show(self):
        if self.side == 0:
            print(f'Question: {self.q}')
        else:
            print(f'Answer: {self.a}')
       
    def edit(self):
        self.show_editor() 
        done=False
        while done==False:
            key = str(input(f'Enter a Action Key: '))
            if key == "":
                done=True
            elif key.lower() == "a":
                self.set_a(self.prompt_user(key='a'))
                self.show_editor() 
            elif key.lower() == "q":
                self.set_q(self.prompt_user(key='q'))
                self.show_editor() 
            else:
                self.show_editor()

    def show_editor(self):
        os.system('clear')
        print('Card Editor View')
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        print('Question: ', self.q)
        print('Answer: ', self.a)
        print('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')
        print(f"""Action Keys: quit == " enter ", edit Answer == " A ", edit Question == " Q " """)

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
