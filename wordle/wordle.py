import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-hm', '--hardmode', action='store_true', help='denotes hard mode; hard mode chooses a word from all 12920 five-letter words found on https://www.bestwordlist.com/5letterwords.htm')
args = parser.parse_args()

if args.hardmode:
    # words scraped from https://www.bestwordlist.com/5letterwords.htm
    words = np.load('five_letter_words_hard.npy', allow_pickle=True)
    valid_guesses = words ### in hard mode, accept wider range of guesses
else:
    # words scraped from https://www.wordunscrambler.net/word-list/wordle-word-list
    words = np.load('five_letter_words_normal.npy', allow_pickle=True)

    # words scraped from gist.github.com/kcwhite/bb598f1b3017b5477cb818c9b086a5d9
    valid_guesses = np.load('valid_guesses.npy', allow_pickle=True)

def newgame():
    rand_word = words[np.random.randint(0, len(words))]
    np.save('target_word.npy', rand_word)

    input_words = []
    np.save('input_words.npy', input_words)

    plt.figure(figsize=(6,8))
    f = plt.axis([0,6,0,8])

    R1 ='QWERTYUIOP'
    R1_x = np.arange(1.3,1.3+0.4*len(R1), 0.4)
    R1_y = 7
    d_R1 = dict(zip(R1, R1_x))

    R2 = 'ASDFGHJKL'
    R2_x = np.arange(1.5,1.5+0.4*len(R2), 0.4)
    R2_y = 7.4
    d_R2 = dict(zip(R2, R2_x))

    R3 = 'ZXCVBNM'
    R3_x = np.arange(1.6, 1.6+0.4*len(R3), 0.4)
    R3_y = 7.8
    d_R3 = dict(zip(R3, R3_x))

    for i in range(len(R1)):
            plt.text(R1_x[i], R1_y, R1[i], fontsize=15)
    for i in range(len(R2)):
            plt.text(R2_x[i], R2_y, R2[i], fontsize=15)
    for i in range(len(R3)):
            plt.text(R3_x[i], R3_y, R3[i], fontsize=15)

    plt.axis('off')
    plt.gca().invert_yaxis() # starting from the top

    plt.savefig('attempt.png')

def used_l(row, evals):
    used_l = []
    for letter in row:
        for l_eval in evals:
            for l, c in l_eval:
                if letter == l:
                    if c == 'grey':
                        used_l.append((l, 'white'))
                    else:
                        used_l.append((l, c))
    d_used_l = dict(used_l)

    return d_used_l

def plot_eval(let_evals):
    # xlim 6, we don't expect any words longer than 5 letters (+1 to center plot)
    # ylim 8, we don't expect more than 6 attempts (+1 to center plot, +1 for keyboard visualization)
    plt.figure(figsize=(6,8))
    f = plt.axis([0,6,0,8])

    for i in range(len(let_evals)):
        l_eval = let_evals[i]

        for j in range(len(l_eval)):
            l, c = l_eval[j]
            plt.text(j+1, i+1, l, fontsize=35, color=c)

    R1 ='QWERTYUIOP'
    R1_x = np.arange(1.3,1.3+0.4*len(R1), 0.4)
    R1_y = 7
    d_R1 = dict(zip(R1, R1_x))

    R2 = 'ASDFGHJKL'
    R2_x = np.arange(1.5,1.5+0.4*len(R2), 0.4)
    R2_y = 7.4
    d_R2 = dict(zip(R2, R2_x))

    R3 = 'ZXCVBNM'
    R3_x = np.arange(1.6, 1.6+0.4*len(R3), 0.4)
    R3_y = 7.8
    d_R3 = dict(zip(R3, R3_x))

    d_R1_used = used_l(R1, let_evals)
    for l in d_R1_used.keys():
        plt.text(d_R1[l], R1_y, str(l), fontsize=16, c=d_R1_used[l])

    d_R2_used = used_l(R2, let_evals)
    for l in d_R2_used.keys():
        plt.text(d_R2[l], R2_y, str(l), fontsize=16, c=d_R2_used[l])

    d_R3_used = used_l(R3, let_evals)
    for l in d_R3_used.keys():
        plt.text(d_R3[l], R3_y, str(l), fontsize=16, c=d_R3_used[l])

    for i in range(len(R1)):
        if R1[i] not in d_R1_used.keys():
            plt.text(R1_x[i], R1_y, R1[i], fontsize=15)
        else:
            pass
    for i in range(len(R2)):
        if R2[i] not in d_R2_used.keys():
            plt.text(R2_x[i], R2_y, R2[i], fontsize=15)
        else:
            pass
    for i in range(len(R3)):
        if R3[i] not in d_R3_used.keys():
            plt.text(R3_x[i], R3_y, R3[i], fontsize=15)
        else:
            pass


    plt.axis('off')
    plt.gca().invert_yaxis() # starting from the top

    return f

def attempt(input_word):
    win = False

    target_word = np.load('target_word.npy', allow_pickle=True)
    target_word = str(target_word) # why do i have to do this

    input_words = np.load('input_words.npy')
    input_words = list(input_words)

    input_word = input_word.upper()

    if input_word.lower() == 'exit':
        sys.exit()

    # check real word
    check = False
    while not check:
        if input_word in valid_guesses:
            check = True
            break
        if input_word.lower() == 'exit':
            sys.exit()

        print('must be a valid five letter word. (っ˘̩︵˘̩)っ\n')
        input_word = input().upper()

    # check number of attempts
    if len(input_words) < 6:
        input_words.append(input_word)
    else:
        print('out of attempts. (￢_￢;)')
        sys.exit()

    # check correct word!
    if input_word == target_word:
        print('\nyou got it! ✧ﾟ･:* ヾ(✿＾∇＾✿)ﾉ *:･ﾟ✧')
        win = True

    # evaluate each letter
    let_evals = []
    for input_word in input_words:

        let_eval = []
        for i in range(len(target_word)):
            let = input_word[i]

            if let in target_word:
                inputword_l_i = [i for i, l in enumerate(input_word) if l == let]
                targetword_l_i = [i for i, l in enumerate(target_word) if l == let]

                # correct number of repeated letters or unique letters
                if len(inputword_l_i) <= len(targetword_l_i):
                    if i in targetword_l_i:
                        let_eval.append((let, 'green'))
                    else:
                        let_eval.append((let, 'gold'))

                # incorrectly repeated letters, with some in correct positions
                elif len(inputword_l_i) > len(targetword_l_i):
                    if i in targetword_l_i:
                        let_eval.append((let, 'green'))

                    elif inputword_l_i.index(i) + 1 <= len(targetword_l_i):

                        # incorrectly repeated letters, with some in incorrect positions
                        if len(set(inputword_l_i).intersection(set(targetword_l_i))) < len(targetword_l_i):
                            let_eval.append((let, 'gold'))

                        # incorrectly repeated letters will be marked grey after correct number of
                        # repeated letters are marked green and/or gold.
                        else:
                            let_eval.append((let, 'grey'))
                    else:
                        let_eval.append((let, 'grey'))
            else:
                let_eval.append((let, 'grey')) # alliterative color names :-)

        let_evals.append(let_eval)

    np.save('input_words.npy', input_words)

    plot_eval(let_evals)
    plt.savefig('attempt.png')
    #plt.show(block=False) ### doesn't work as intended so i wrote a separate
                           ### script for continuous plotting; see viewer.py

    return win

def playgame():
    newgame()

    print('\n--- new game! ---')
    print('type your attempts and then press enter')
    print('or type "exit" to exit\n')

    # while loop for 6 valid attempts
    ### invalid attempts do not progress attempt counter
    attempts = 0
    win = False
    while attempts <6:
        input_word = input()
        win = attempt(input_word)

        if win:
            break

        elif not win and attempts >=5:
            print('\nToo bad! The word was:')
            reveal()

            break

        else:
            attempts += 1

    # play again loop
    play_again = input('Would you like to play again? (y/n)  ')

    while not play_again.lower() in set(['y', 'n']):
        print('pleaser enter "y" or "n"')
        play_again = input()

    if play_again.lower() == 'y':
        return True

    elif play_again.lower() == 'n':
        return False


def reveal():
    target_word = np.load('target_word.npy')
    print(target_word,'\n\n')

def main():
    if args.hardmode:
        mode = 'hard mode'
    else:
        mode = 'normal mode'

    print(f'\n===== ✧ﾟ❀ wordle ({mode}) ❀ﾟ✧ =====')
    play = True
    while play:
        play = playgame()

    print('\nThanks for playing! goodbye')
    sys.exit()

if __name__ == '__main__':
    main()
