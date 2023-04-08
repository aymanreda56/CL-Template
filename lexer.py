from graphviz import Digraph
import copy
import json
import re




def insert_sequence(str1, str2, index):
    '''
    just a helper function that injects str2 into str1 just after the index given.
    used when resolving the range operator
    '''
    str1_split1 = str1[:index]
    str1_split2 = str1[index:]
    new_string = str1_split1 + str2 + str1_split2
    return new_string





def ClassesPreprocessor(infix):
    '''
    loops on all square brackets, checks for consecutive alphaneumerics, inserts | between them
    so in the case of [a-zA-Z] will be [a-z|A-Z] and in the case of [abc] will be [a|b|c] and the case [a-z] will be [a-z] nothing will change here
    THIS FUNCTION IS TO BE RUN BEFORE 'preprocessor' FUNCTION or you will face some lovely bugs :)
    '''
    alphabet = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    processed_infix = []
    insideClass = False
    for i,c in enumerate(infix):
        processed_infix.append(c)
        if c == '[':
            insideClass = True
            continue
        if c == ']':
            insideClass = False
        if(insideClass and c in alphabet and infix[i+1] in alphabet):
            processed_infix.append('|')
    if(insideClass):
      raise ValueError(f"Your Regex is erronous; Square Brackets are not closed")
    return ''.join(processed_infix)

        




def preprocessor(infix):
    '''
    loop on every character c in infix :
	if c is in ['*' , '+', '?',')',']'] and if next character v is anything not in ['*' , '+', '?',')',']' , '.', '|'] :
		append ' . ' right between c and v  (right after c)

    if c is alphabet or digit and next char v is alphabet or digit or opening brackets '(' or '[' :
        append '.' right between c and v (right after c)
    '''
    specials = ['*' , '+', '?',')',']']
    others = ['.', '|']
    alphabet = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    out_string = ""
    out_index = 0

    for i, c in enumerate(infix):
        out_string = out_string + c
        out_index = out_index + 1
        if i < len(infix) - 1:
            if c in specials and not(infix[i+1] in specials or infix[i+1] in others):
                out_string = insert_sequence(out_string, '.', out_index)
                out_index = out_index + 1

            elif(c in alphabet and (infix[i+1] in alphabet or infix[i+1] in ['(', '['])):
                out_string = insert_sequence(out_string, '.', out_index)
                out_index = out_index + 1

    return out_string





def shunt(infix):
    ''' Shunting Yard algorithm, to be run after the preprocessing steps obvs '''
  
    alphabet = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    operators = {'*': 5,                  \
               '+': 4,                  \
                '?': 3,                 \
                '.': 2,                 \
                '|': 1}
  


    # Initializing empty pofix and stack strings
    postfix, stack = "", ""  #a stack is just a string or list :D
    i = 0

    #for every character c in input infix
    while infix != [] and i < len(infix):
        c = infix[i]
        #print(f'\nindex: {i} in infix: {infix} looking at character: {c}')
        
        #if opening bracket
        if c in ['(' , '[']:
            stack = stack + c  #push c to stack

        #if closing bracket
        elif c == ')':
            # pop until we reach the matching bracket
            while stack and stack[-1] != '(':
                postfix = postfix + stack[-1]  #append to postfix
                stack = stack[:-1]  #then pop stack
            if not stack:                    #if stack became empty, meaning the bracket is not opened aslan, then raise error
                raise ValueError(f"Your Regex is erronous; Brackets are opened but not closed")
                return False

            stack = stack[:-1]  # another pop to remove the open bracket in the stack, it is useless
    

        elif c == ']':
            # pop until we reach the matching bracket
            while stack and stack[-1] != '[':
                postfix = postfix + stack[-1]  #append to postfix
                stack = stack[:-1]  #pop stack
            if not stack:                    #if stack became empty, meaning the bracket is not opened aslan
              raise ValueError (f"Your Regex is erronous; Square Brackets are opened but not closed")
              return False

            stack = stack[:-1]  # another pop to remove the open bracket in the stack


        #if c is an operator
        elif c in operators:
            while stack and operators[c] <= operators.get(stack[-1], 0):      #if stack not empty and precedence(c) <= precedence(top of stack)
                postfix, stack = postfix + stack[-1], stack[:-1]                #pop and append to postfix
        
            stack = stack + c                                                 #just push c to stack



        elif c == '-':
            if(i == len(infix)):                                     #raise error in case of missing second operand bcs input is finished, ex: [A -
                return False
            first = postfix[-1]
            last = infix[i+1]
            if(not(last in alphabet)):                               #raise error in case of second operand is not in alphabet, ex: [A - ()]
                return False

            '''
            construct the new list to be injected into infix, example [a-f] we want to replace '-' by '|b|c|d|e|'
            so we want to get the starting character and the ending character, then construct the list
            then finally inject it into infix using the function insert_sequence
            '''
            processed_list = []
            for v in alphabet:
                if(alphabet.index(v) > alphabet.index(first) and alphabet.index(v) < alphabet.index(last)):
                    processed_list.append('|')
                    processed_list.append(v)
            
            processed_list.append('|')
            infix = insert_sequence(infix, ''.join(processed_list), i+1)
           



        else:   #just a normal character or digit, nothing special, just append to postfix
            postfix = postfix + c

        #print(f'postfix: {postfix}')
        i = i+1

    #finalizing step after infix is empty now, just pop all the stack and append them all to postfix
    while stack:
        if stack[-1] in ['(', '[']:                             #if we found an opened bracket but not closed when finalizing (no more inputs)
            raise ValueError (f"Your Regex is erronous; Brackets or Square Brackets are not closed")
            return False
        postfix, stack = postfix + stack[-1], stack[:-1]


    #final check by using re.compile  ;)
    try:
      re.compile(infix)
    except Exception as e:
      raise ValueError(f"Your Regex is erronous; {e}")
      return False
    #return the result
    return postfix
