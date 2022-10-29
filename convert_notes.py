import os
import json
import uuid

def qa_json(lines):
    count=0
    data={}
    while count < len(lines):
        line = lines[count]
        if 'q:' in line:
            id=str(uuid.uuid4())
            q_index=count
        elif 'a:' in line:
            q=lines[q_index].replace('q:','').replace('\n','').strip(' ')
            a=lines[count].replace('a:','').replace('\n','').strip(' ')
            data[id]={
                'q':q,
                'a':a
            }
        count+=1
    return data
        

def get_qa_index(lines):
    flag = False
    line_len = len(lines)
    count=0
    while flag == False:
        if 'QA' in lines[count]:
            flag = True
        elif count +1 == line_len:
            flag = True
        else:
            count+=1
            
    if count +1 == line_len:
        return -1
    else:
        return count
    

def get_QA_section(path):
    with open(path, 'r') as f:
        lines = [x.strip('/n') for x in f.readlines()]
    qa_index = get_qa_index(lines)
    if get_qa_index(lines) != -1:
        return qa_json(lines[qa_index:])
    else:
        print(f'{path} has no QA section')
        return {}
                
    

def main(root_dir, deck_name):
    valid_notes = sorted([x for x in os.listdir('./notes/') if x.split('.')[-1]=='md'])
    data = {}
    for filename in valid_notes:
        for k,v in get_QA_section(path='./notes/'+filename).items():
            data[k] = v
    
    os.chdir(os.path.join(root_dir,'flashcards'))
    with open(deck_name, 'w') as f:
        json.dump(data, f, indent=4, )
        
if __name__ == "__main__":
    root_dir=os.getcwd()
    if 'flashcards' not in os.listdir():
        raise Exception('file must be ran in a root directory with "flashcards folder"')
    flag=False
    verbose = False
    while flag == False:
        dir_list = [x for x in os.listdir() if os.path.isfile(x) == False]
        dir_dict = {i:x for i, x in enumerate(dir_list)}
        os.system('clear')
        print(dir_dict)
        print('')
        print('- Use a # to select the dir with your notes folder')
        print('- Use ".." to move up one level')
        print('- Use a dir name to move into a dir')
        if verbose == True:
            print(f'No folder labeled "notes" in the "{name}" directory')
        else:
            print(' ')
        ans = input('Enter Here: ')
        if ans.isdigit():
            ans=int(ans)
            if ans in dir_dict.keys():
                name = dir_dict[ans]
                flag = True
            else:
                pass
        if ans == '..':
            os.chdir('..')
        if ans in list(dir_dict.values()):
            os.chdir(f'./{ans}')
        
        if flag == True:
            os.chdir(f'./{name}')
            if 'notes' not in os.listdir():
                flag = False
                verbose = True
                os.chdir('..')
    
    deck_name=name.lower()+'_flashcards.json'
    main(root_dir,deck_name)
