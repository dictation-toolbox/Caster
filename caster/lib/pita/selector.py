'''
Created on Feb 26, 2015

@author: dave
'''
from operator import itemgetter

from caster.lib import settings


def get_similar_symbol_name(spoken_phrase, list_of_symbols):
    '''
    spoken_phrase: list of strings
    list_of_symbols: list of strings
    '''
    
    if settings.SETTINGS["pita"]["automatic_lowercase"]:
        spoken_phrase = [x.lower() for x in spoken_phrase] 
    results = []
    without_homonyms = _abbreviated_string(spoken_phrase)
    with_homonyms = _abbreviated_string(_homonym_replaced_string(spoken_phrase))
    
    for w in list_of_symbols:
        # make copies because _phrase_to_symbol_similarity_score is destructive (of spoken phrase)
        without_homonyms_lower = without_homonyms.lower()
        with_homonyms_lower = with_homonyms.lower()
        w_lower = w.lower()
        
        penalty = 0
        bonus = 0
        if settings.SETTINGS["pita"]["use_penalty"]:
            penalty = _length_penalty(spoken_phrase, w_lower)
        if settings.SETTINGS["pita"]["use_bonus"]:
            bonus = _whole_word_bonus(spoken_phrase, w_lower)
        
        score = _phrase_to_symbol_similarity_score(without_homonyms_lower, w_lower) - penalty + bonus
        score_homonyms = _phrase_to_symbol_similarity_score(with_homonyms_lower, w_lower) - penalty + bonus
        score = score if score>score_homonyms else score_homonyms
        results.append((score, w))
        
    length = 10 if len(results)>10 else len(results)
    results = sorted(results, key=itemgetter(0), reverse=True)[:length]
    return [x[1] for x in results]

_HOMONYM_REPLACEMENTS= {"one":1, "won":1, "two":2, "to":2, "too":2, "three":3, "for":4, "four":4, "five":5, "six":6, "sex":6,
                          "seven":7, "eight":8, "ate":8, "nine":9, "zero":0
                          }
def _clean_homonyms(word):
    global _HOMONYM_REPLACEMENTS
    for homonym in _HOMONYM_REPLACEMENTS:
        if homonym in word:
            word = word.replace(homonym, " " + str(_HOMONYM_REPLACEMENTS[homonym]) + " ")
    return word
        
def _homonym_replaced_string(spoken_list):
    # if there are numbers or things which sound like numbers in the symbol, replace those things in the spoken phrase before breaking it
    return [_clean_homonyms(x) for x in spoken_list]

def _abbreviated_string(spoken_phrase):
    '''
    get power characters from spoken phrase
    --
    spoken_phrase: an array of strings
    '''
    
    abbrev = ""
    for w in spoken_phrase:
        abbrev += w[0]
        
        wlen = len(w)
        if wlen > 1:
            abbrev += w[1]
            if wlen > 2:
                abbrev += w[2]
                if wlen > 3:
                    abbrev += w[-1]
    return abbrev

def _phrase_to_symbol_similarity_score(abbrev, symbol):
    score = 0
    index_abbrev = 0
    len_abbrev = len(abbrev)
    len_symbol = len(symbol)
    for i in range(0, len_symbol):
        index_abbrev = 0
        while index_abbrev < len_abbrev:
            '''
             if the symbol character is found in the abbreviation,
             reduce the abbreviation, remeasure the abbreviation
             and reset the index on the abbreviation, break the while
            '''
            if str(abbrev[index_abbrev]) == str(symbol[i]):
                if index_abbrev + 1 < len_abbrev:
                    abbrev = abbrev[index_abbrev + 1:]
                    index_abbrev = 0
                len_abbrev = len(abbrev)
                score += 1
                break
            else:
                '''else bump up the abbreviation index'''
                index_abbrev += 1
    return score

def _length_penalty(spoken_phrase, symbol):
    '''penalize when symbol is much longer than spoken phrase'''
    penalty = len(symbol) - len(" ".join(spoken_phrase))
    if penalty < 0:
        penalty = 0
    return penalty

def _whole_word_bonus(spoken_phrase, symbol):
    bonus = 0
    for word in spoken_phrase:
        if word in symbol:
            bonus += 1
    return bonus

####################################################################################
####################################################################################

def get_similar_process_names(spoken_phrase, list_of_processes):
    '''
    spoken_phrase: list of strings
    list_of_symbols: list of strings
    '''
    results = []
    process = _abbreviated_string(spoken_phrase)
    unwanted_processes=["wininit", "csrss", "System Idle Process", "winlogon",  \
                        "SearchFilterHost", "conhost"]
    wanted_processes=[x for x in list_of_processes if x not in unwanted_processes]
    for w in wanted_processes:
        # make copies because _phrase_to_symbol_similarity_score is destructive (of spoken phrase)
        process_lower = process.lower()
        w_lower = w.lower()
        
        score = _phrase_to_symbol_similarity_score(process_lower, w_lower)
        results.append((score, w))
    
    length = 10 if len(results)>10 else len(results)
    results = sorted(results, key=itemgetter(0), reverse=True)[:length]
    return [x[1] for x in results]

def get_similar_window_names(spoken_phrase, list_of_titles):
    '''
    spoken_phrase: list of strings
    list_of_symbols: list of strings
    '''
    results = []
    title = " ".join(spoken_phrase)
    unwanted_titles=[]
    wanted_processes=[x for x in list(set(list_of_titles)) if x not in unwanted_titles]
    for w in wanted_processes:
        # make copies because _phrase_to_symbol_similarity_score is destructive (of spoken phrase)
        title_lower = title.lower()
        w_lower = w.lower()
        
        score = _phrase_to_symbol_similarity_score(title_lower, w_lower)
        results.append((score, w))
    
    length = 10 if len(results)>10 else len(results)
    results = sorted(results, key=itemgetter(0), reverse=True)[:length]
    return [x[1] for x in results]
    
####################################################################################
####################################################################################

class OffsetArrayItem(object):
    def __init__(self, c1, c2, trans):
        self.c1=c1
        self.c2=c2
        self.trans=trans

def sift4(s1, s2, max_offset, max_distance):
    '''credit Siderite, and thanks'''
    if s1 is None or len(s1)==0:
        if s2 is None:
            return 0
        return len(s2)
    
    if s2 is None or len(s2)==0:
        return len(s1)
    
    l1=len(s1)
    l2=len(s2)
    
    c1=0 #cursor for string 1
    c2=0 #cursor for string 2
    lcss=0 #largest common subsequence
    local_cs=0 #local common substring
    trans=0 #number of transpositions ('ab' vs 'ba')
    offset_array=[] #offset pair array, for computing the transpositions
    
    while c1<l1 and c2<l2:
        if s1[c1]==s2[c2]:
            local_cs+=1
            is_trans=False
            #see if current match is a transposition
            i=0
            while i<len(offset_array):
                ofs=offset_array[i]
                if c1<=ofs.c1 or c2<=ofs.c2:
                    #when two matches cross, the one considered a transposition is the one with the largest difference in offsets
                    is_trans=abs(c2-c1)>=abs(ofs.c2-ofs.c1)
                    if is_trans:
                        trans+=1
                    elif not ofs.trans:
                        ofs.trans=True
                        trans+=1
                    break
                elif c1>ofs.c2 and c2>ofs.c1:
                    del offset_array[i]
                else:
                    i+=1
            offset_array.append(OffsetArrayItem(c1, c2, is_trans))
        else:
            lcss+=local_cs
            local_cs=0
            if c1!=c2:
                c1=c2=min(c1, c2)# using min allows the computation of transpositions
            
            #if matching characters are found, remove 1 from both cursors (they get incremented at the end of the loop)
            #so that we can have only one code block handling matches 
            i=0
            while i<max_offset and (c1+i<l1 or c2+i<l2):
                if c1+i<l1 and s1[c1+i]==s2[c2]:
                    c1+=i-1
                    c2-=1
                    break
                if c2+i<l2 and s1[c1]==s2[c2+i]:
                    c1-=1
                    c2+=i-1
                    break
                i+=1
        c1+=1
        c2+=1
        if max_distance:
            temporary_distance=max(c1, c2)-lcss+trans
            if temporary_distance>=max_distance:
                return round(temporary_distance)
        #this covers the case where the last match is on the last token in list, so that it can compute transpositions correctly
        if c1>=l1 or c2>=l2:
            lcss+=local_cs
            local_cs=0
            c1=c2=min(c1, c2)        
    lcss+=local_cs
    return round(max(l1, l2)-lcss+trans)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
