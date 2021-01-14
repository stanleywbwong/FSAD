from collections import Counter

def unscramble(text):
    """ 
    Determines if a string is some permutation of a word in the given word 
    list and returns a list of possible unscrambled words. 

    Approach: the given text is a permutation of a word iff the count of each
    letter matches the counts of letters in a valid word. Maintain a dict
    (Counter object) of the given string's letter counts and attempt to match 
    with letter counts of each line in the word list.
    """

    unscrambled_words = []
    text_count = Counter(text)

    with open("word_list.txt", 'r') as f:
        for line in f.readlines():
            # count letter instances in each line
            line_count = Counter(line.strip())

            # subtract letter instances of the given text
            line_count.subtract(text_count)

            # check if all counts are 0 - if so, then we have a match
            if not any(line_count.values()):
                unscrambled_words.append(line.strip())
    
    # note these are sorted by nature of the sorted word_list
    print(unscrambled_words)
    return unscrambled_words

    # Note: we can probably achieve better runtime by processing each line 
    # character by character (and ending the processing prematurely once we 
    # realize the line won't match the given text), rather than creating a new 
    # Counter object for each line.



if __name__ == "__main__":
    assert unscramble("hello") == ["hello"]
    assert unscramble("gibberishh") == []
    assert unscramble("eilnst") == ["enlist","listen","silent","tinsel"]
    assert unscramble("ivle") == ["evil, live, veil, vile, vlei"]
    assert unscramble("i")