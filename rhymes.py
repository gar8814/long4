""" File: rhymes.py
    Author: Garrett Scott
    Purpose: Create a "pronunciation dictionary" from a text file and compare
    user input words to find words that rhyme with the user word. The program
    will then print all the words from the "dictionary" that rhyme.
    CSC 120, Fall 2020
"""
import sys

def file_input_cond():
    """Takes a user input string and strips front and back whitespace.
        Arguments: None
        Return Value: string
        Pre-condition: None
    """

    file_name = input().strip()
    return  file_name

def file_handler(file_name):
    """ Takes a file name as arg and opens the file and reads the lines of the
        file and places the contents of each line into a list of lists.
        Arguments: str
        Return Value: list of list -> [[word, phoneme, phoneme,...],[...],...]
        Pre-condition: file object is valid object
    """
    file = open(file_name)
    file_lst = file.readlines()

    # Striping comments and spliting each line into elements of their
    # own list
    cleaner_lst = []
    for line in file_lst:
        if "#" not in line.strip():
            cleaner_lst.append(line.strip().split())

    # Getting rid of any blank lines from the file
    even_cleaner_lst = []
    for item in cleaner_lst:
        if item:
            even_cleaner_lst.append(item)

    return even_cleaner_lst



def list_to_dicts(lst):
    """ Takes a list created from reading a file of words and its phonemes and
        creates a dict with key = word, value = phoneme list and a dict with
        key = phoneme and value =- word. the key-word dict's value is a list of
        lists to hold phonemes for more than one pronunciation for the given
        spelling.
        Arguments: List
        Return Value: dict, dict
        Pre-condition: list passed into the function is a list of lists
    """
    # takes list element from the list of lists and uses the first element of
    # the sublist and uses it as the key of the dict and the rest of the list
    # as the value for that key
    out_dict = {}
    for item in lst:
        if item[0] in out_dict.keys():
            out_dict[item[0]].append(item[1:])

        else:
            out_dict[item[0]] = []
            out_dict[item[0]].append(item[1:])
    # This takes the new dictionary and creates a copy but in the format-
    # Old_Value: Old_key
    reversed_out_dict = {}

    for k, v in out_dict.items():
        # if there is more than one pronucniation for a spelling make sure
        # there are two entries in the dict to handle both pronunciations
        if len(v) > 1:
            for i in v:
                nkey = " ".join(i)
                # Checks to make sure two or more words with the same pronunc
                # are accounted for in the new dict.
                if nkey in reversed_out_dict.keys():
                    reversed_out_dict[nkey].append(k)

                else:
                    reversed_out_dict[nkey] = []
                    reversed_out_dict[nkey].append(k)

        else:
            # ther is only one pronuciation for the word.
            nkey = " ".join(v[0])
            # Checks to make sure two or more words with the same pronunc
            # are accounted for in the new dict
            if nkey in reversed_out_dict.keys():
                reversed_out_dict[nkey].append(k)

            else:
                reversed_out_dict[nkey] = []
                reversed_out_dict[nkey].append(k)

    return out_dict, reversed_out_dict

def check_input(word):
    """ A word is passed into this function. if the word is empty it will
        print out an error, or if there is more than one word it will print out
        a different error message.
        Arguments: string
        Return value: Boolean True or Fase
        Pre-conditions: None
    """
    try:
        assert word != ""
    except AssertionError:
        print("No word given")
        print()
        return False

    try:
        assert " " not in word
    except AssertionError:
        print("Multiple words entered, please enter only one word at a time.")
        print()
        return False

    return True


def primary_stress(arg1):
    """ Takes an iterable data type containing phonemes and scans for a
        primary_stress and returnes the index.
        Arguments: Iterable data type
        Return value: int or none
        Pre-condition: the arg1 is an iterable with phonemes
    """
    assert type(arg1) == list
    assert len(arg1) > 0
    assert "" not in arg1

    for i in range(len(arg1)):
        if arg1[i][-1] == '1':
            return i
    return None

def find_rhyme(usr_wd, usr_pronunc, p_w_dict, words_lst):
    """ Compares a word with other words in a pronuciation dictionary looking
        for words that are perfect rhymes and stores matches in a lst of words.
        Perfect rhymes are defined by haveing the same primary stress and every
        subsquent sound after and having a different phoneme prior to the
        primary stress.
        Arguments: string, list of strings, dictionary and list of words
        Return Value: none
        Pre-condition: the usr_wd is valid and in the dictionary of phonemes.
    """
    p_str_i = primary_stress(usr_pronunc)
    # if there is a primary stress in the user word continu checking
    if p_str_i:
        # loop through the dictionary that has keys that are pronuciations
        for k in p_w_dict:
            # If the user primary stress is in the current pronuc key and
            # its not looking act the same word as the user word continue check
            if usr_pronunc[p_str_i] in k and p_w_dict[k] != usr_wd:
                # convert the key we are looking from str -> lst
                k_lst = k.split()
                # grab the index of the key's primary stress
                p_str_j = primary_stress(k_lst)
                # check if  primary stress is the first element
                if p_str_j == 0:
                    continue

                else:
                    if k_lst[p_str_j - 1] != usr_pronunc[p_str_i - 1]:
                        # check to see if the phonemes after the primary stress
                        # are the same
                        if k_lst[p_str_j:] == usr_pronunc[p_str_i:]:
                            # if there are more then one words for a
                            # pronunciation in the reversed_out_dict loop
                            # through it and add them all for output.
                            if len(p_w_dict[k]) > 1:
                                for wd in p_w_dict[k]:
                                    if wd not in words_lst:
                                        words_lst.append(wd)

                            else:
                                if p_w_dict[k][0] not in words_lst:
                                    words_lst.append(p_w_dict[k][0])

                        else:
                            continue

                    else:
                        continue

            else:
                continue

    else:
        return

def scan_dictionary(usr_wd, w_p_dict, p_w_dict):
    """ Scans for the user word in a dictionary of phonemes and if its found
        will look through the dictionary finding other words that rhyme. Will
        output a list of words that rhyme with the user word.
        Arguments: string, two dictionarys
        Return Value: list of strings
        Pre-conditions: there exists two dictionarys on with word to phoneme
        maping and one with phoneme to word maping and a valid user word.
    """
    # if the word is in the dictionary grab the list of phonemes
    words_out = []
    if usr_wd in w_p_dict.keys():
        # user_word_pronun list.
        usr_w_p= w_p_dict[usr_wd]
        # if there are more than one pronucniation for the word
        if len(usr_w_p) > 1:
            # Look at each pronuciation and find if there is a rhyme
            for pronun in usr_w_p:
                find_rhyme(usr_wd, pronun, p_w_dict, words_out)

        else:
            find_rhyme(usr_wd, usr_w_p[0], p_w_dict, words_out)

    else:
        words_out = None

    return words_out

def print_out(usr, lst):
    """ This function prints out the list of Rhyming owrds if they are present.
        Arguements: str, list of strings
        Return Value: none.
        Pre-conditions: none.
    """

    print("Rhymes for: {}".format(usr.upper()))
    if lst:
        lst.sort()
        for word in lst:
            print("  {}".format(word))

    else:
        print("  -- none found --")

def main():
    # Grab file name from user
    file_lst = file_handler(file_input_cond())
    # load pronuciation dictionary into memory
    word_pron_dict, pron_word_dict = list_to_dicts(file_lst)

    # grab words from user to check for rhymes.
    for line in sys.stdin:
        usr_word = line.strip().upper()

        if check_input(usr_word):
            f_words = scan_dictionary(usr_word, word_pron_dict, pron_word_dict)
            print_out(usr_word, f_words)
            print()



if __name__ == "__main__":
    main()
