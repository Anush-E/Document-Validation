import re
import spacy
import string
import neuralcoref
#nltk.download() # use this line if you are executing the code for the first time in your device
from nltk import tokenize
from nltk.corpus import wordnet 


#############################################################################################

def find_pronoun(text,flag):
    
    '''This function is used to find to which nouns are the pronouns pointing to'''
    
    nlp = spacy.load('en_core_web_sm')
    
    neuralcoref.add_to_pipe(nlp)
    
    doc = nlp(text)
    
    a = doc._.coref_clusters
    
    leng = len(a)
    
    pronoun_pairs=[[] for x in range(leng)]

    for j in range (0,leng):
        for i in a[j]:
            pronoun_pairs[j].append(i.text)

    print("\nNoun-Pronoun Pair(s) : ",pronoun_pairs)
    
    replace_pronoun(pronoun_pairs,text,flag)
    
###############################################################################################

def replace_pronoun(pronoun_pairs,text,flag):
    
    '''This function is used to replace the pronouns with their respective nouns. This function
       takes (noun, pronoun) pair from 'find_pronoun' function'''

    for i in pronoun_pairs:
        for j in i:
            text = re.sub(r'\b%s\b'% j,i[0],text)
            
    pronoun_free_text = text

    
    print("\nAfter replacing PRONOUNS with NOUNS: ",pronoun_free_text)
    
    word_tokenization(pronoun_free_text,flag)

###############################################################################################

def word_tokenization(text,flag):
    
    '''This function is used to tokenize the text into individual words. The output is a list
       of individual words'''
    
    word_tokenized_text = text.split() #splitting words from sentences

    print("\nAfter TOKENIZING into WORDS: ",word_tokenized_text)
    
    articles_removal(word_tokenized_text,flag)

###############################################################################################

def articles_removal(text,flag):
    
    '''This function is used to remove the articles (a, an, the) from a text'''
    
    
    articles = ["a", "an", "the"]

    article_free_text  = [word for word in text if word.lower() not in articles] #removing articles
    
    print("\nAfter removing ARTICLES: ",article_free_text)
    
    de_tokenization(article_free_text,flag)

###############################################################################################

def de_tokenization(text,flag):
    
    '''This function is used to join the individual words together to form a sentence'''
    
    de_tokenized_text = ' '.join(text) #forming sentence again from words

    print("\nAfter de-tokenizing back to sentence: ",de_tokenized_text)

    sentence_tokenization(de_tokenized_text,flag)

###############################################################################################

def sentence_tokenization(text,flag):
    
    '''This function is used to tokenize the text into individual sentences'''
    
    sentence_tokenized_text = tokenize.sent_tokenize(text) 
    
    print("\nAfter TOKENIZING into SENTENCES: ",sentence_tokenized_text)
    
    punctuation_removal(sentence_tokenized_text,flag)

###############################################################################################

def punctuation_removal(text,flag):
    
    '''This function is used to remove the punctuations'''
    
    punctuation_free_text = [''.join(c for c in s if c not in string.punctuation) for s in text]

    print("\nAfter removing PUNCTUATIONS: ",punctuation_free_text)
    
    if flag == 1:
        find_dependency(punctuation_free_text,flag)
        
    else:
        replace_synonyms(punctuation_free_text,flag)

###############################################################################################
        
def replace_synonyms(synonyms_replaced_text,flag):
    
    '''This function is used to replace the words with their respective synonym'''
    
    global synonmys_replaced_text

    for i in synonyms_replaced_text:
        for ac in i.split():
            for key,value in meanings.items():
                for j in value:
                    if j == ac:
                        al = re.sub(r'\b%s\b'% ac,key,i)
                        synonyms_replaced_text[synonyms_replaced_text.index(i)] = al


    print("\nAfter replacing synonmys in the given text: ",synonyms_replaced_text) 

    find_dependency(synonyms_replaced_text,flag)     
        
###############################################################################################        

def find_dependency(text,flag):
    
    '''This function is used to find the dependency among words in a sentence'''
    
    global dependency_text
    
    mini = 0
    
    for l in text:
        
        leng = 0
        leng = len(re.findall(r'\w+', l))
        
        if leng>mini:
            mini = leng

    dependency = [[[] for x in range(mini)]for x in range(len(text))] 

    d = 0

    for l in text:
        
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(l)
        
        x=0
        
        for token in doc:    
            for j in (token.text, token.tag_, token.head.text, token.dep_):
                
                dependency[d][x].append(j)
                
            x = x+1
        d = d+1
        
    
    dependency_text = [[x for x in c if x] for c in dependency]

    print("\nAfter finding DEPENDENCY: ")
    
    for i in dependency_text:
        for j in i:
            print("\n",j)
        print("----------------------------------------------------------------")
        
    if flag == 1:   
        finding_synonyms(dependency_text)

###############################################################################################
        
def finding_synonyms(text):
    
    '''This function is used to find the synonyms of the words in a sentence'''
    
    global meanings
    
    meanings = {}


    for j in text:
        for m in j:
            synonyms=[]
            for syn in wordnet.synsets(m[0]): 
                for l in syn.lemmas(): 
                    synonyms.append(l.name()) 
                    meanings[m[0]] = list(set(synonyms))
    
    print("\nSYNONYMS of words: \n")

    for i,j in meanings.items():
        print("\n",i," : ",j,"\n","----------------------------------------------------------------")
    
###############################################################################################

'''Below is the main function. Execution starts from here'''

text_original = "Ram is a boy. He is good"
print("\nOriginal Text: ",text_original)

global dependency_text
global meanings

find_pronoun(text_original,1)

dependency_text_original = dependency_text
meanings_original = meanings

#--------------------------------------------------------------------------------------------#

text_given = "Ram is a boy. He is skilful"
print("\nGiven Text: ",text_given)

global synonyms_replaced_text

find_pronoun(text_given,0)

dependency_text_given = dependency_text














