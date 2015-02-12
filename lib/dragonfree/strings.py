def get_similar_symbol_name(spoken_phrase, list_of_symbols):

    best = (0, "")
    without_homonyms = abbreviated_string(spoken_phrase)
    with_homonyms = abbreviated_string(homonym_replaced_string(spoken_phrase))
    
    for w in list_of_symbols:
        score = phrase_to_symbol_similarity_score(without_homonyms.lower(), w.lower())
        if score > best[0]:
            best = (score, w)
        score = phrase_to_symbol_similarity_score(with_homonyms.lower(), w.lower())
        if score > best[0]:
            best = (score, w)
     
    return best[1]

def homonym_replaced_string(s):
    # if there are numbers or things which sound like numbers in the symbol, replace those things in the spoken phrase before breaking it
    homonym_replacements = {"one":1, "won":1, "two":2, "to":2, "too":2, "three":3, "for":4, "four":4, "five":5, "six":6, "sex":6,
                          "seven":7, "eight":8, "ate":8, "nine":9, "zero":0
                          }
    for homonym in homonym_replacements:
        if homonym in s:
            s = s.replace(homonym, " " + str(homonym_replacements[homonym]) + " ")
    return s.replace("  ", " ").rstrip()

def abbreviated_string(s):
    # get power characters from spoken phrase
    words_in_phrase = s.split(" ")
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

def phrase_to_symbol_similarity_score(abbrev, symbol):
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
                if index_abbrev+1<len_abbrev:
                    abbrev = abbrev[index_abbrev+1:]
                    index_abbrev = 0
                len_abbrev = len(abbrev)
                score += 1
                break
            
            # else bump up the abbreviation index
            else:
                index_abbrev += 1
    return score
