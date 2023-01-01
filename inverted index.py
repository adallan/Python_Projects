In this project I create a series of functions that are all involved in creating an inverted index
The goal of an inverted index is to create an index in memory of a list of files that contain desirable information and that information's
index locations within the file.

Step 1: Creation of a document generator that can make a range of files to have regular expressions performed on them.
---------------------------------------------------------------------------------------------------------
def doc_gen(num):
    from faker import Faker
    fake = Faker()
    file_path = 'insert_path_here'
    for x in range(num):
        file_name = fake.text(20)
        with open(f'{file_path}/{file_name}','w') as f:
            indexnum = random.randint(1,15)
            if indexnum in (1,3,4,13):
            
                #index is a digit/integer
                
                f.write(fake.text(1000))
                f.write(imp_info.get(indexnum) + str(fake.random_int()))
                
                # imp_info is a dictionary for the purpose inserting text to be regexed later on
                
                f.write(fake.text(1000))
            elif indexnum in (2,8,9,14):
            
                #index is a date
                 
                f.write(fake.text(1000))
                f.write(imp_info.get(indexnum) + str(fake.day_of_month()))
                f.write(fake.text(1000))
            else: 
            
                #index is phone number
                
                f.write(fake.text(1000))
                f.write(imp_info.get(indexnum) + str(fake.phone_number()))
                f.write(fake.text(1000)) 

Step 2: Define function for searching for a word with regex
Step 3: Function for grabbing the searched words index location
Step 4: Function for creating a dictonary that will act as the inverted index and adding searched word to it
---------------------------------------------------------------------------------------------------------
def word_search(text_body,search_word):
    pattern = str(search_word)
    result = re.search(pattern,text_body)
    return result

def find_location(text_body,search_word):
    try:
        match = word_search(text_body,search_word)
        word = match[0]
        location = match.span()
        return word,location
    except:
        pass

def add_to_dict(inv_index,filename,word,location):
    
    key_word,key_index = word,location
    word_index = {filename:{key_word:key_index}}
    inv_index.update(word_index)
    return(inv_index)
    
    
Step 5: Combine the three functions into one.
---------------------------------------------------------------------------------------------------------
def update_invert_index(inv_index):
    import os
    file_path = '/Users/alex/Desktop/My python stuff/doc_storage'
    os.chdir(file_path)
    files = os.listdir()
    search_word = input('What are you searching for?: ')
    for file in files:
        full_path = file_path+'/'+file
        with open(full_path,'r',encoding='utf8') as f:
            text = f.read()
            try:
                word,location = find_location(text,search_word)
                add_to_dict(inv_index,file,word,location)
            except:
                pass
    return inv_index
    
Step 6: Function to extract word from the inverted index.
---------------------------------------------------------------------------------------------------------    
    new_dict = {}
def extract_word_loc(inv_index,new_dict):
    
    word = input('What would you like to pull from the index? ')
    for files in inv_index.items():
        file = files[0]
        try:
        
#find if word is in file
#grab locations, filename that has word
# new dict that is filename:location

            if word in inv_index[file].keys():
                location = inv_index[file][word]
                file_location = {file:location}
                new_dict.update(file_location)
            else:
                pass
        except:
            pass
    return word
    
Step 7: New function that open and read file and return text +10 and -10 of indexes
---------------------------------------------------------------------------------------------------------    
def find_text(file,word,loc_tup):
    file_path = '/Users/alex/Desktop/My python stuff/doc_storage'
    full_path = file_path+'/'+file
    with open(full_path,'r',encoding='utf8') as f:
        text = f.read()
        if word in text:
            print(text[loc_tup[0]-50:loc_tup[1]+50])
        else:
            pass
      
Step 8: Inverted index interface that utilizes all functions. Searches for a word and shows what files contain it,
then opens the file and reads ten words before and ten words after searched word to give context.
---------------------------------------------------------------------------------------------------------           
#needs to use find_text and extract word
#needs to use files,word,location variables
def inv_index_interface(inv_index):
    new_dict = {}
    word = extract_word_loc(inv_index,new_dict)
    print(new_dict)
    file = input('Which file would you like to open?: ')
    loc_tup = inv_index[file][word]
    find_text(file,word,loc_tup)
