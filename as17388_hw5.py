import sys

def find_word(count,arr, choice):
    if choice == "beg":
        if count < 2 and count <1:
            return False
        token = arr[count - 1].strip()
        token_length = len(token)
        if token_length != 0:
            return False
        else:

            return True

    else:
        if count > len(arr) - 2:
            return False
        token = arr[count + 1].strip()
        token_length = len(token)
        if token_length != 0:
            return False
        else:

            return True



def access (count, arr, w_or_p, f_or_b):
    array_length = len(arr)
    found_word = False
    if w_or_p == 'w' and f_or_b == 'f':
        found_word = find_word(count, arr, "end")
        if count > array_length - 2:
            return '</s>'
        elif found_word==True:
            return '</s>'

        elif found_word==False and count<=array_length-2:
            return arr[count + 1].strip().split()[0]

    elif w_or_p == 'pos' and f_or_b == 'f':
        found_word = find_word(count, arr, "end")
        if count > array_length - 2:
            return '</s>'
        elif found_word == True:
            return '</s>'

        elif count <= array_length - 2 and found_word==False:
            return arr[count + 1].strip().split()[1]

    elif w_or_p == 'w' and f_or_b == 'b':
        found_word = find_word(count, arr, "beg")
        if count < 1:
            return '<s>'
        elif found_word == True:
            return '<s>'

        elif count>=1 and (found_word==False):
            return arr[count - 1].strip().split()[0]
    else:
        found_word = find_word(count, arr, "beg")
        if count < 1:
            return '<s>'
        elif found_word == True:
            return '<s>'

        elif count>=1 and found_word==False:
            return arr[count - 1].strip().split()[1]

def validate (count, arr, choice):
    found_word = False
    if choice == 'c':

        if not (arr[count].strip().split()[0][0].isupper()):
            return '0'
        else:
            return '1'
    elif choice == 'b':
        found_word = find_word(count, arr,"beg")
        if count < 1:
            return '0'
        if found_word==True:
            return '0'
        else:

            if not (arr[count - 1].strip().split()[0][0].isupper()):
                return '0'
            else:
                return '1'
    else:
        found_word = find_word(count, arr, "end")
        if count > len(arr) - 2:
            return '0'
        elif found_word == True:
            return '0'

        else:

            if not (arr[count + 1].strip().split()[0][0].isupper()):
                return '0'
            else:
                return '1'



with open(sys.argv[1] ,'r') as source:
    with open('training.feature', 'w') as main:
        lines = source.readlines()
        for i, sentence in enumerate(lines):
            sentence = sentence.strip()
            if len(sentence) == 0:
                main.write('\n')
            else:
                current_w, current_p, current_b = sentence.split()
                current_cap    = 'cur_cap='   + validate(i,lines,'c')

                old_w  = 'prev_word=' + access(i,lines,'w','b')
                old_p   = 'prev_pos='  + access(i,lines,'p','b')
                old_c   = 'prev_cap='  + validate(i,lines,'b')

                future_w  = 'next_word=' + access(i,lines,'w','f')
                future_p   = 'next_pos='  + access(i,lines,'p','f')
                future_c   = 'next_cap='  + validate(i,lines,'f')

                w_past = 'pp_word=' + access(i-1,lines,'w','b')
                p_past  = 'pp_pos='  + access(i-1,lines,'p','b')
                c_past  = 'pp_cap='  + validate(i-1,lines,'b')
                w_now = 'nn_word=' + access(i+1,lines,'w','f')
                p_now  = 'nn_pos='  + access(i+1,lines,'p','f')
                c_now  = 'nn_cap='  + validate(i+1,lines, 'f')

                sentence = '\t'.join([current_w, current_p, current_cap, old_w, \
                                  old_p, old_c, future_w, future_p, \
                                  future_c, w_past, p_past, c_past, w_now,\
                                  p_now, c_now, current_b])
                main.write(sentence + '\n')

with open(sys.argv[2], 'r') as source:
    with open('test.feature', 'w') as main:
        lines = source.readlines()
        for i, sentence in enumerate(lines):
            sentence = sentence.strip()
            sentence_length = len(sentence)
            if sentence_length == 0:
                main.write('\n')
            else:
                current_w, current_p = sentence.split()

                old_w = 'prev_word='   + access(i,lines,'w','b')
                old_p  = 'prev_pos='    + access(i,lines,'p','b')
                old_c  = 'prev_cap='    + validate(i,lines,'b')

                w_past = 'pp_word=' + access(i-1,lines,'w','b')
                p_past  = 'pp_pos='  + access(i-1,lines,'p','b')
                c_past  = 'pp_cap='  + validate(i-1,lines,'b')


                current_b   = 'cur_bio=##'
                current_cap   = 'cur_cap='     + validate(i,lines,'c')

                future_w = 'next_word='   + access(i,lines,'w','f')
                future_p  = 'next_pos='    + access(i,lines,'p','f')
                future_c  = 'next_cap='    + validate(i,lines,'f')

                w_now = 'nn_word=' + access(i+1,lines,'w','f')
                p_now  = 'nn_pos='  + access(i+1,lines,'p','f')
                c_now  = 'nn_cap='  + validate(i+1,lines,'f')

                sentence = '\t'.join([current_w, current_p, current_cap, old_w, \
                                  old_p, old_c, future_w, future_p, \
                                  future_c, w_past, p_past, c_past, w_now,\
                                  p_now, c_now, current_b])
                main.write(sentence + '\n')
