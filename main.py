#
# GLOBALS
#

colors = ["pink", "green", "blue", "orange", "purple", "yellow"]
possible = []
unguessed = []
possible_results = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 1],
                    [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [3, 0], [4, 0]]
num_guesses = 1


#
# SETUP AND SIMPLE FUNCTIONS
#

def setup_possible():
    global possible
    for i in range(0, 6):
        for j in range(0, 6):
            for k in range(0, 6):
                for m in range(0, 6):
                    pattern = str(i) + str(j) + str(k) + str(m)
                    possible.append(pattern)
                    unguessed.append(pattern)


def minimum_of_two(num1, num2):
    if num1 > num2:
        return num2
    else:
        return num1


def minimum_in_list(li):
    minimum = li[0]
    for el in li:
        if el < minimum:
            minimum = el
    return minimum


def maximum_in_list(li):
    maximum = li[0]
    for el in li:
        if el > maximum:
            maximum = el
    return maximum


def num_of_each_color(pattern):  # counts how many of each color are in pattern
    ret = [0, 0, 0, 0, 0, 0]
    for peg in pattern:
        ret[int(peg)] += 1  # peg's color is at index int(peg) of the list of colors
    return ret


#
# ALGORITHM
#

def eliminate_impossible(last_guess, pegs):
    global possible
    color_counts = num_of_each_color(last_guess)
    possible[:] = [poss for poss in possible if could_be_correct(last_guess, color_counts, poss, pegs)]


def get_number_eliminated(hypothetical_guess, pegs):
    ret = 0
    color_counts = num_of_each_color(hypothetical_guess)
    for poss in possible:
        if not could_be_correct(hypothetical_guess, color_counts, poss, pegs):
            ret += 1
    return ret


def could_be_correct(last_guess, color_counts, maybe_correct, last_result):
    hypothetical_result = calc_result(last_guess, color_counts, maybe_correct)
    # how many red and white would there have been if maybe_correct were the correct pattern?
    return hypothetical_result[0] == last_result[0] and hypothetical_result[1] == last_result[1]
    # peg counts don't match up; poss is no longer a possible correct pattern


def calc_result(guessed, num_of_each_g, correct):
    red = 0
    white = 0
    num_of_each_c = num_of_each_color(correct)
    for color in range(0, 6):
        white += minimum_of_two(num_of_each_g[color], num_of_each_c[color])
    for i in range(0, 4):
        if guessed[i] == correct[i]:  # found an exact match between guessed and correct
            red += 1
    white -= red  # reds are a special case of whites so we can't count these twice
    return [red, white]


def get_best_guess():
    global result
    if len(possible) == 0:  # error!
        result = [4, 5]  # pretend that guess was correct, since there was an error in the algorithm and we need to quit
        return "6666"
    if len(possible) <= 2:
        return possible[0]
    minimum_eliminated_overall = get_minimum_eliminated_list(unguessed)
    minimum_eliminated_possible = get_minimum_eliminated_list(possible)
    eliminated_for_best_overall = maximum_in_list(minimum_eliminated_overall)
    eliminated_for_best_possible = maximum_in_list(minimum_eliminated_possible)
    if eliminated_for_best_overall == eliminated_for_best_possible:
        return possible[minimum_eliminated_possible.index(eliminated_for_best_possible)]
    else:
        return unguessed[minimum_eliminated_overall.index(eliminated_for_best_overall)]


def get_minimum_eliminated_list(guesses):
    ret = []
    for poss_guess in guesses:
        eliminated = []
        for res in possible_results:
            eliminated.append(get_number_eliminated(poss_guess, res))
        ret.append(minimum_in_list(eliminated))
    return ret


#
# USER INTERFACE
#

def make_guess():
    global num_guesses
    global unguessed
    str_guess = ""
    for index in guess:
        str_guess += " "
        str_guess += colors[int(index)]
    print("Guess " + str(num_guesses) + ":" + str_guess)
    num_guesses += 1
    unguessed.remove(guess)


def get_result():
    ret = [int(input("Enter red pegs: ")), int(input("Enter white pegs: "))]
    while not (ret in possible_results):
        # peg counts that were entered don't make sense
        print("Out of range. Enter again.")
        ret = [int(input("Enter red pegs: ")), int(input("Enter white pegs: "))]
    return ret


#
# RUN
#

setup_possible()
guess = "0011"  # ideal first guess according to algorithm
make_guess()
result = get_result()
while result[0] != 4:
    eliminate_impossible(guess, result)
    guess = get_best_guess()
    if result[1] != 5:  # no error occurred
        make_guess()
        result = get_result()

if result[1] == 0:  # didn't end in an error
    print("Solved! Winning is fun.")
else:
    print("Error: Nothing possible. This is probably your fault.")
