import argparse
import os
from cli_quizlet import *


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--flashcards_parent_dir',  default='.', type=str, help='directory containing the "flashcards" folder')
    parser.add_argument('--decks_parent_dir',  default='.', type=str, help='directory containing the "decks" folder')
    return parser.parse_args()

def find_current_card_counter(flashcards_dir):
    if os.listdir(flashcards_dir) != []:
        print(f"Adding to cards found in {flashcards_dir}", os.listdir(flashcards_dir))
        cards=[card.split('.')[0] for card in os.listdir(flashcards_dir)]
        card_counters=[int(card.split('_')[-1]) for card in cards]
        return max(card_counters)+1
    else:
        return 0

def new_deck(flashcards_dir):
    cards={}
    card_counter=find_current_card_counter(flashcards_dir)
    making_cards=True
    while making_cards:
        print('\n','Enter a question and answer')
        qa = str(input('QA: '))
        if qa != "exit" and '; ' in qa:
            qa_list = qa.split('; ')
            q=qa_list[0]
            a=qa_list[1]
            cards[card_counter]={'q':q, 'a':a}
        elif qa=='exit':
            making_cards=False
        elif '; ' not in qa:
            print('format must be of  "Q"; "A"  or type "exit"')
        else:
            pass
        
    
    for k,v in cards.items():
        filename=flashcards_dir+f"/card_{k}.json"
        with open(filename, "w") as f:
            f.write(json.dumps(v))
    print(f'Saved Flashcards in {flashcards_dir}')

def main(args):
    try:
        assert 'flashcards' in os.listdir(args.flashcards_parent_dir)
        assert 'decks' in os.listdir(args.decks_parent_dir)

    except:
        print('flashcards or decks directory was not found!')
        print('making folder for you')
        os.chdir(args.flashcards_parent_dir)
        os.mkdir('flashcards')
        os.chdir(args.decks_parent_dir)
        os.mkdir('decks')

    decks_dir=args.decks_parent_dir+f'/decks'
    flashcards_dir=args.flashcards_parent_dir+f'/flashcards'
    name = str(input('Enter a new Deck Name: '))
    deck=Deck(decks_dir=decks_dir,name=name)
    new_deck(flashcards_dir)
    deck.load_flashcards(flashcards_dir)
    deck.save_deck()

        


    

    

if __name__ == "__main__":
    os.system('clear')
    args=parse_args()
    main(args)