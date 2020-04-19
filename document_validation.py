    import re
    import spacy
    import string
    import neuralcoref
    #nltk.download() # use this line if you are executing the code for the first time in your device
    from nltk import tokenize
    from nltk.corpus import wordnet 
    import pandas as pd
    
    
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
        
        global feedback_sentokenization
        
        sentence_tokenized_text = tokenize.sent_tokenize(text) 
        
        feedback_sentokenization = sentence_tokenized_text
        
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
                        try:
                            if j == ac:
                                al = re.sub(r'\b%s\b'% ac,key,i)
                                synonyms_replaced_text[synonyms_replaced_text.index(i)] = al
                        except ValueError:
                            continue
    
    
        print("\nAfter replacing synonmys in the given text: ",synonyms_replaced_text) 
    
        find_dependency(synonyms_replaced_text,flag)     
            
    ###############################################################################################        
    
    def find_dependency(text,flag):
        
        '''This function is used to find the dependency among words in a sentence'''
        
        global dependency_text, original_list2, given_list2, checklist
        
        mini = 0
        
        for l in text:
            
            leng = 0
            leng = len(re.findall(r'\w+', l))
            
            if leng>mini:
                mini = leng
    
        dependency = [[[] for x in range(mini)]for x in range(len(text))] 
        original_list2 = [[[] for x in range(mini)]for x in range(len(text))] 
        checklist = [[[] for x in range(mini)]for x in range(len(text))]
        given_list2 = [[[] for x in range(mini)]for x in range(len(text))] 
    
    
        d = 0
    
        for l in text:
            
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(l)
            
            x=0
            
            for token in doc:    
                for j in (token.text, token.tag_, token.head.text, token.dep_):
                    try:
                        dependency[d][x].append(j)
                    except IndexError:
                        continue
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
    
    text_original = """Photosynthesis is faster than respiration. Photosynthesis is the process by which plants prepare their own food with the help of sunlight, carbondioxide, chlorophyll and water. Photosynthesis takes place at night."""
    #text_original = "Ram is a boy. He is good"
    #text_original = """The company requires staff to watch a safety video every year"""
    print("\nOriginal Text: ",text_original)
    
    global dependency_text
    global meanings
    global original_list2
    global feedback_sentokenization
    global checklist
    
    find_pronoun(text_original,1)
    
    dependency_text_original = dependency_text
    meanings_original = meanings
    
    original_list3 = original_list2
    checklist2 = checklist

    #--------------------------------------------------------------------------------------------#
    
    text_given = """At night, photosythesis takes place. Photosynthesis is faster than  respiration. The process by which plants prepare their own food with the help of carbondioxide, water and sunlight is called photosynthesis."""
    #text_given = "Prepare food sunlight chlorophyll water. night"
    #text_given = "Ram is a boy. He is good"
    #text_given = "The staff are required by the company to watch a safety video every year"

    print("\nGiven Text: ",text_given)
    
    global synonyms_replaced_text, given_list2
    
    find_pronoun(text_given,0)
    
    dependency_text_given = dependency_text
    
    given_list3 = given_list2
    
    
    #---------------------------------------------------------------------------------------------#
    
    ''''count = 0
    for i in dependency_text_original:
        for j in i:
            tag = j[3]
            print(tag)
            for k in dependency_text_given:
                for l in k:
                    if l[3] == tag:
                        if j[0] == l[0]:
                            count = count+1
                            print(j[0],l[0])
                 
            
            
    
            
    print(count)'''     
    k=0  
    for i in dependency_text_original:
        l=1
        repeat = []
        for j in i:
            if j[3]=="ROOT":
                root1 = j[0]
                original_list3[k][0].append(j)
                repeat.append(j[0])
                break
        for j in i:
            if j[2] == root1 and j[3]!='ROOT' and j[0] not in repeat:
                original_list3[k][l].append(j)
                l=l+1
                repeat.append(j[0])
        for j in i:
            if j[3]!= "ROOT":
                root1 = j[0]
                for j in i:
                    try:
                        if j[2] == root1 and j[0]!= root1 and j[0] not in repeat:
                            original_list3[k][l].append(j)
                            l=l+1
                            repeat.append(j[0])
                    except IndexError:
                        continue
        k=k+1
    
        
    original_list4 = [[x for x in c if x] for c in original_list3]
    
    print(original_list4)    
    print("\n")            
                
    k=0
    for i in dependency_text_given:
        l=1
        repeat = []
        for j in i:
            if j[3]=="ROOT":
                root1 = j[0]
                given_list3[k][0].append(j)
                repeat.append(j[0])
                break
        for j in i:
            if j[2] == root1 and j[3]!='ROOT' and j[0] not in repeat :
                given_list3[k][l].append(j)
                l=l+1
                repeat.append(j[0])
        for j in i:
            if j[3]!= "ROOT":
                root1 = j[0]
                for j in i:
                    try:
                        if j[2] == root1 and j[0]!= root1 and j[0] not in repeat:
                            given_list3[k][l].append(j)
                            l=l+1
                            repeat.append(j[0])
                    except IndexError:
                        continue
                    
        k=k+1
        
    given_list4 = [[x for x in c if x] for c in given_list3]
    
    print(given_list4, "\n\n")    
    

                    
    nsubj = ['obj', 'oprd', 'nsubjpass', 'attr', 'pobj', 'dobj','nsubj']
    pobj  = ['compound', 'conj', 'pobj']
    #unwanted = ['cc','preconj','prep','auxpass','aux','punct']
    unwanted = []
    key_answer = [{('NAN','plants', 'prepare', 'food') : 1, ('NAN','carbondioxide'):0.25, ('NAN','water') : 0.25 , ('NAN','chlorophyll') : 0.25, ('NAN','sunlight') : 0.25},{('NAN','takes','place','night') : 0.5},{('NAN','faster','than','respiration') : 0.5}]

 
    
    match_rate = [[]for x in range(len(key_answer))]

    for i in range(len(key_answer)):
        for j in original_list4:
            match_count = 0
            for k in key_answer[i]:
                for o in k[1:]:
                    for r in j:
                        if(o==r[0][0]):
                            match_count = match_count+1
            match_rate[i].append(match_count)
        
    
    match_rate1 = [[]for x in range(len(key_answer))]

    

    for i in range(len(match_rate)):
        match_rate1[i].append(pd.Series(match_rate[i]).idxmax())


    m=0    
    for u,i in zip(match_rate1,range(len(key_answer))):
        n=0
        for j in range(len(original_list4)):
            match_count = 0
            for k in key_answer[i]:
                for o in k[1:]:
                    for r in original_list4[j]:
                        if(o==r[0][0]):
                            checklist2[i][n].append(r[0])
                n = n+1

        

    checklist3 = [[x for x in c if x] for c in checklist2]

    print(checklist3)


    match_rate = [[]for x in range(len(checklist3))]

    for i in range(len(checklist3)):
        for j in given_list4:
            match_count = 0
            for k in checklist3[i]:
                for o in k:
                    for r in j:
                        if(o[0]==r[0][0]):
                            match_count = match_count+1
            match_rate[i].append(match_count)
    
    
    
    match_rate1 = [[]for x in range(len(checklist3))]

    for i in range(len(match_rate)):
        match_rate1[i].append(pd.Series(match_rate[i]).idxmax())


    match = 0
    score = 0
    feedback = []

    for i,f in zip(range(len(checklist3)),key_answer):
        for m in match_rate1[i]:
            for j,(h,s) in zip(checklist3[i],f.items()):
                match_list = []
                for k in j:
                    for n in given_list4[m]:
                        if(k[0]==n[0][0] and k[3] not in unwanted and n[0][3] not in unwanted):
                            if(k[3] == n[0][3] or (k[3] in nsubj and n[0][3] in nsubj) or (k[3] in pobj and n[0][3] in pobj)):
                                print(n[0][0])
                                match = 1
                                break
                            else:
                                match = 0
                        else:
                            match = 0
                    if match == 1:
                        match_list.append(n[0][0])
                        continue
                    else:
                        feedback.append((h[1:],s))
                        break
                if(match==1):
                    for q in key_answer:
                        for j in q:
                            for r in match_list:
                                if r in j[1:]:
                                    absent = 0
                                else:
                                    absent = 1
                                    break
                            if absent == 0:
                                score = score + q[j]
                else:
                    continue
            
    print(score)

    if not feedback:
        print("Feedback: Your answer is correct")
    else:
        print("You missed your marks here: ",feedback)
