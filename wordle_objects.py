# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 23:40:09 2022

@author: Venkatesh



Wordle Bots for Wordle Game


Basic Framework - 
# Types of characters
1 - accepted in the target at correct position
2 - accepted in the target but incorrect position
3 - rejected



Bot Versions -
V1 - regex based filtering
uses positive and negative lookaheads for type2 and type 3 characters.
type 1 characters are substituted in the normal regex


"""

# =============================================================================
# 
# =============================================================================

import random
import re

import numpy as np

# =============================================================================
# 
# =============================================================================

ALPHABETS = [(chr(ord('a')+i)) for i in range(26)]
MAX_GUESS = 5
POSITIVE_LOOK = "(?=.*%s)"
NEGATIVE_LOOK = "(?!.*%s)"
USED_WORD = "(?!%s)"

# =============================================================================
# 
# =============================================================================

def get_val(x):
    if max(x)==2:
        return 1
    elif sum(x)>1:
        return 0
    else:
        return -1

def get_mask(word):
    return np.array([[int(x==y) for y in word] for x in ALPHABETS])

def reduce_reduce(x,y):
    if x==-1:
        return -1
    else:
        return x & y

# def print_word(wrd):
#     print(wrd.upper())

def get_random_word(word_list):
    return word_list[random.randint(0,len(word_list)-1)]

def convert_to_regex(guess, mask, output):
    for ind,element in enumerate(mask):
        if element == -1:
            # output[ind] = '\w'
            pass
        elif element == 0:
            output[ind] = '[^%s]'%(re.sub(r'\[|\]|\^|\\w','',output[ind]) + guess[ind])
        else:
            output[ind] = guess[ind]
    return output

# =============================================================================
# Global Variables
# =============================================================================

with open('corpus.txt','r') as f:
    CORPUS = f.read().split('\n')

# =============================================================================
# Servers
# =============================================================================

class WordleServerTemplate:
    """Template Class for WordleServer
    """    
    def __init__(self):
        """Generates a random task for the created WordleServer object
        """        
        self.task = get_random_word(CORPUS)
    
    def compare_words(self, guess:str) -> tuple:
        """Function to take an input as guess, compare with task and return the mask and flag to indicate if guess was correct or not.
        mask is generated according to the following format - 
        1 - correct position for the character in the target word.
        0 - incorrect position for the character but present at other position in the target word.
        -1 - incorrect character for the target word.

        Args:
            guess (str): a string guess taken as input.

        Returns:
            tuple: tuple containing the output variables - mask_reduced, task_flag
            None, True - when guess matches the task
            [...], False - when guess does not match the task and the mask is generated.
        """        
        comp_flag = True
        mask_reduced = None
        return mask_reduced, comp_flag

class WordleServer(WordleServerTemplate):
    """Custom Implementation of WordleServer
    """
    def __init__(self):
        """Generates a random task for the created WordleServer object
        """   
        self.task = get_random_word(CORPUS)
    
    def compare_words(self, guess):
        """Function to take an input as guess, compare with task and return the mask and flag to indicate if guess was correct or not.
        mask is generated according to the following format - 
        1 - correct position for the character in the target word.
        0 - incorrect position for the character but present at other position in the target word.
        -1 - incorrect character for the target word.

        Args:
            guess (str): a string guess taken as input.

        Returns:
            tuple: tuple containing the output variables - mask_reduced, task_flag
            None, True - when guess matches the task
            [...], False - when guess does not match the task and the mask is generated.
        """ 
        task = self.task
        comp_flag = True
        mask_reduced = None
        if guess != task:
            mask_guess = get_mask(guess)
            mask_task = get_mask(task)
            mask_reduce = mask_task + mask_guess
            mask_reduce[(mask_reduce==mask_guess).all(axis=1)]=[0]*5
            mask_reduce1 = np.apply_along_axis(get_val, 1, mask_reduce)
            mask_reduce1 = np.array([mask_reduce1[ALPHABETS.index(x)] for x in guess])
            mask_reduce0 = np.apply_along_axis(get_val, 0, mask_reduce)
            mask_reduced = np.array([reduce_reduce(mask_reduce1[ind],mask_reduce0[ind]) for ind in range(5)])
            comp_flag = False
        return mask_reduced, comp_flag

# =============================================================================
# Wordle Bots
# V1 - regex based filtering
# uses positive and negative lookaheads for type2 and type 3 characters.
# type 1 characters are substituted in the normal regex
# =============================================================================

class WordleBot:
    def __init__(self):
        pass

    def solver1(self, server: WordleServer, guess:str = 'crane'):
        """v1
        auto solver with the next guess being the a random word from the list of possible words
        and has positional inaccuracies accounted for with square brackets
        Args:
            server (WordleServer): A Wordleserver object that follows the template class above.
            guess (str, optional): A starting guess word. Defaults to 'crane'.

        Returns:
            _type_: _description_
        """        
        current_guess = guess
        negative_chars = set()
        positive_chars = set()
        possible_words = []
        used_words = []
        mask_regex_base = ['\w']*len(guess)
        iteration = 0
        while iteration < 20:
            mask_reduced, comp_flag = server.compare_words(current_guess)
            if comp_flag:
                break
            negative_chars |= {current_guess[ind] for ind,flag in enumerate(mask_reduced) if flag==-1}
            positive_chars |= {current_guess[ind] for ind,flag in enumerate(mask_reduced) if flag==0}
        
            positive_pattern = ''.join([POSITIVE_LOOK%(char) for char in positive_chars])
            negative_pattern = ''.join([NEGATIVE_LOOK%(char) for char in negative_chars])
            used_pattern = ''.join([USED_WORD%(wrd) for wrd in used_words])
            
            mask_regex_base = convert_to_regex(current_guess, mask_reduced, mask_regex_base)
            
            mask_regex = positive_pattern + negative_pattern + used_pattern + ''.join(mask_regex_base)
            possible_words = [x for x in CORPUS if re.search(mask_regex, x)]
            used_words.append(current_guess)
            current_guess = get_random_word(possible_words)
            iteration += 1
    
        print("Solution is -", current_guess)
        return iteration, current_guess
    
    def solver2(self):
        # A sovler based on information theory and prior probabilities.
        pass
        

if __name__=='__main__':
    wordleserver = WordleServer()
    bot = WordleBot()
    total_iterations, solution = bot.solver1(server=wordleserver)
    print("Total Iterations -",total_iterations)
    print("Bot Solution -",solution)
    print("Server Task -",wordleserver.task)

