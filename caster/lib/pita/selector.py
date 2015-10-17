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

def _search(all_symbols, word):
    '''old search code from element'''
    # get index
    high_score = [0, 0]
    for i in range(0, len(all_symbols)):
        score = _word_similarity_score(all_symbols[i], word)
        if score > high_score[1]:
            high_score = [i, score]
            if score == len(word):
                break
    return high_score

def _word_similarity_score(w1, w2):
    smaller_len = len(w1)
    w2_len = len(w2)
    if w2_len < smaller_len:
        smaller_len = w2_len
    score = 0
    for i in range(0, smaller_len):
        if w1[i] == w2[i]:
            score += 1
        else:
            return score
    return score
