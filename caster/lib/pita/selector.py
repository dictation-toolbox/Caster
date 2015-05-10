'''
Created on Feb 26, 2015

@author: dave
'''
from caster.lib import settings


def get_similar_symbol_name(spoken_phrase, list_of_symbols):
    if settings.SETTINGS["pita"]["automatic_lowercase"]:
        spoken_phrase = spoken_phrase.lower()
    best = (0, "")
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
        if score > best[0]:
            best = (score, w)
        score = _phrase_to_symbol_similarity_score(with_homonyms_lower, w_lower) - penalty + bonus
        if score > best[0]:
            best = (score, w)
     
    return best[1]

def _homonym_replaced_string(s):
    # if there are numbers or things which sound like numbers in the symbol, replace those things in the spoken phrase before breaking it
    homonym_replacements = {"one":1, "won":1, "two":2, "to":2, "too":2, "three":3, "for":4, "four":4, "five":5, "six":6, "sex":6,
                          "seven":7, "eight":8, "ate":8, "nine":9, "zero":0
                          }
    for homonym in homonym_replacements:
        if homonym in s:
            s = s.replace(homonym, " " + str(homonym_replacements[homonym]) + " ")
    return s.replace("  ", " ").strip()

def _abbreviated_string(spoken_phrase):
    # get power characters from spoken phrase
    words_in_phrase = spoken_phrase.split(" ")
    abbrev = ""
    for w in words_in_phrase:
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
            # if the symbol character is found in the abbreviation,
            # reduce the abbreviation, remeasure the abbreviation
            # and reset the index on the abbreviation, break the while
            if abbrev[index_abbrev] == symbol[i]:
                if index_abbrev + 1 < len_abbrev:
                    abbrev = abbrev[index_abbrev + 1:]
                    index_abbrev = 0
                len_abbrev = len(abbrev)
                score += 1
                break
            
            # else bump up the abbreviation index
            else:
                index_abbrev += 1
    return score

def _length_penalty(spoken_phrase, symbol):
    # penalize when symbol is much longer than spoken phrase
    penalty = len(symbol) - len(spoken_phrase)
    if penalty < 0:
        penalty = 0
    return penalty

def _whole_word_bonus(spoken_phrase, symbol):
    bonus = 0
    words = spoken_phrase.split(" ")
    for w in words:
        if w in symbol:
            bonus += 1
    return bonus

####################################################################################
####################################################################################
####################################################################################

def _search(all_symbols, word):
    '''old search code from element'''
    # get index
    high_score = [0, 0]
    # high_score = index, score
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
