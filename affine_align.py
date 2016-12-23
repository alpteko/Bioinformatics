import collections
import sys

second_string = []
first_string = []
input_file = 'test-pair2.txt'
score_matrix = collections.defaultdict(dict)
gap_penalty = -11
extend_penalty = -1
h = 0
w = 0
score_file = 'matrix.txt'
optimum_score = 0
max_print =  60


####### movement types
diagonal_mov = 'diagonal'
left_mov = '  left  '
up_mov = '   up   '
stop_mov = '  stop  '
to_lower = 'to_lower'
to_upper = 'to_upper'
lower_to_main = 'low__main'
upper_to_main = '_up_main'
delete = 'deletion'
insert = 'insertion'
match = 'match'



######Matricessss
main_value_matrix = [[]]
lower_value_matrix = [[]]
upper_value_matrix = [[]]
main_movement_matrix = [[]]
lower_movement_matrix = [[]]
upper_movement_matrix = [[]]


def parse_input():
    global input_file
    input_file = sys.argv[1]
    global gap_penalty
    gap_penalty = -1 * float(sys.argv[2])
    global extend_penalty
    extend_penalty = -1 * float(sys.argv[3])


def read_strings():
    global input_file
    global first_string
    global second_string
    global h
    global w
    global main_value_matrix
    global lower_value_matrix
    global upper_value_matrix
    global main_movement_matrix
    global upper_movement_matrix
    global lower_movement_matrix
    file = open(input_file, 'rU')
    i = 0
    for line in file:
        if i == 0:
            for c in line:
                if c == "\n":
                    break
                first_string.append(c)
            i += 1
        else:
            for c in line:
                if c == "\n":
                    break
                second_string.append(c)
    h = len(first_string) + 1
    w = len(second_string) + 1
    main_value_matrix = [[0 for x in range(w)] for y in range(h)]
    upper_value_matrix = [[0 for x in range(w)] for y in range(h)]
    lower_value_matrix = [[0 for x in range(w)] for y in range(h)]
    main_movement_matrix = [['  stop  ' for x in range(w)] for y in range(h)]
    upper_movement_matrix = [['  stop  ' for x in range(w)] for y in range(h)]
    lower_movement_matrix = [['  stop  ' for x in range(w)] for y in range(h)]


def print_matrix(matrix):
    global h
    global w
    for i in range(h):
        for j in range(w):
            print(matrix[i][j], end=' ')
        print()


def get_score(first_index, second_index):
    global score_matrix
    global first_string
    global second_string
    first_letter = first_string[first_index - 1]
    second_letter = second_string[second_index - 1]
    score = float(score_matrix[first_letter][second_letter])
    # print(score, first_letter , second_letter)
    return score

def read_score_matrix():
    global score_matrix
    global score_file
    file = open(score_file, 'r')
    raw_matrix = []
    for i in range(0, 25):
        raw_matrix.append(file.readline().split())
    # print(raw_matrix)
    # print(len(raw_matrix))
    for i in range(1, 25):
        score_matrix[raw_matrix[i][0]] = {}
        for j in range(1, 25):
            score_matrix[raw_matrix[i][0]].update({raw_matrix[0][j]: raw_matrix[i][j]})


def affine_aline():
    global upper_value_matrix
    global main_value_matrix
    global lower_value_matrix
    global main_movement_matrix
    global upper_movement_matrix
    global lower_movement_matrix
    global left_mov
    global diagonal_mov
    global up_mov
    global to_lower
    global lower_to_main
    global upper_to_main
    global to_upper
    global gap_penalty
    global extend_penalty
    global stop_mov
    global h
    global w
    ###### INITIALIZATION
    #######
    #########
    main_value_matrix[0][0] = 0
    main_movement_matrix[0][0] = stop_mov
    upper_value_matrix[0][0] = -10000
    lower_value_matrix[0][0] = -10000
    for i in range(1, h):
        upper_value_matrix[i][0] = gap_penalty + (i-1)*extend_penalty
        upper_movement_matrix[i][0] = up_mov
        main_value_matrix[i][0] = -1000
        lower_value_matrix[i][0] = -1000
    for j in range(1, w):
        lower_value_matrix[0][j] = gap_penalty + (j-1)*extend_penalty
        lower_movement_matrix[0][j] = left_mov
        main_value_matrix[0][j] = -10000
        upper_value_matrix[0][j] = -1000
    #################
    ################
    ###############

    for i in range(1, h):
        for j in range(1, w):
            start = main_value_matrix[i-1][j] + gap_penalty
            cont = upper_value_matrix[i-1][j] + extend_penalty
            if start > cont:
                upper_value_matrix[i][j] = start
                #####
                upper_movement_matrix[i][j] = upper_to_main
                #####
            else:
                upper_value_matrix[i][j] = cont
                ####
                upper_movement_matrix[i][j] = up_mov
                #####
            start = main_value_matrix[i][j-1] + gap_penalty
            cont = lower_value_matrix[i][j-1] + extend_penalty
            if start > cont:
                lower_value_matrix[i][j] = start
                #####
                lower_movement_matrix[i][j] = lower_to_main
                ######
            else:
                lower_value_matrix[i][j] = cont
                ###########
                lower_movement_matrix[i][j] = left_mov
                ###########
            match = main_value_matrix[i-1][j-1] + get_score(i, j)
            lower_end = lower_value_matrix[i-1][j-1] + get_score(i, j)
            upper_end = upper_value_matrix[i-1][j-1] + get_score(i, j)
            choices = [match, lower_end, upper_end]
            optimum = max(choices)
            index = choices.index(optimum)
            main_value_matrix[i][j] = optimum
            ########################
            if index == 0:
                main_movement_matrix[i][j] = diagonal_mov
            elif index == 1:
                main_movement_matrix[i][j] = to_lower
            else:
                main_movement_matrix[i][j] = to_upper
            ##########################


def traceback():
    global main_movement_matrix
    global upper_movement_matrix
    global lower_movement_matrix
    global left_mov
    global diagonal_mov
    global up_mov
    global to_lower
    global lower_to_main
    global upper_to_main
    global to_upper
    global stop_mov
    global h
    global w
    global match
    global insert
    global delete
    global first_string
    global second_string
    global optimum_score
    current = main_movement_matrix[h-1][w-1]
    current_matrix = main_movement_matrix
    i = h-1
    j = w-1
    optimum_sol = [main_value_matrix[i][j],lower_value_matrix[i][j],upper_value_matrix[i][j]]
    index = optimum_sol.index(max(optimum_sol))
    optimum_score = optimum_sol[index]
    if index == 0:
        current = main_movement_matrix[i][j]
        current_matrix = main_movement_matrix
    elif index == 1:
        current = lower_movement_matrix[i][j]
        current_matrix = lower_movement_matrix
    else:
        current = upper_movement_matrix[i][j]
        current_matrix = upper_movement_matrix
    trace_list = []
    while current != stop_mov:
        if current == diagonal_mov:
            i -= 1
            j -= 1
            trace_list.append(match)
        elif current == left_mov:
            j -= 1
            trace_list.append(insert)
        elif current == up_mov:
            i -= 1
            trace_list.append(delete)
        elif current == to_lower:
            current_matrix = lower_movement_matrix
            i -= 1
            j -= 1
            trace_list.append(match)
        elif current == to_upper:
            current_matrix = upper_movement_matrix
            i -= 1
            j -= 1
            trace_list.append(match)
        elif current == upper_to_main:
            current_matrix = main_movement_matrix
            i -= 1
            trace_list.append(delete)
        elif current == lower_to_main:
            current_matrix = main_movement_matrix
            j -= 1
            trace_list.append(insert)
        current = current_matrix[i][j]
    trace_list.reverse()
    first_aligned = []
    second_aligned = []
    i = 0
    j = 0
    for mov in trace_list:
        if mov == match:
            first_aligned.append(first_string[i])
            second_aligned.append(second_string[j])
            i += 1
            j += 1
        elif mov == insert:
            first_aligned.append('-')
            second_aligned.append(second_string[j])
            j += 1
        elif mov == delete:
            first_aligned.append(first_string[i])
            second_aligned.append('-')
            i += 1
    return [first_aligned,second_aligned]


def separate(value):
    for i in range(value):
        print('=',end='')
    print()


def print_result(align_result):
    global optimum_score
    global max_print
    print('OPTIMUM SCORE = ', optimum_score)
    alignment = []
    length = len(align_result[0])
    for i in range(length):
        if align_result[0][i] == align_result[1][i]:
            alignment.append('|')
        elif align_result[0][i] == '-':
            alignment.append(' ')
        elif align_result[1][i] == '-':
            alignment.append(' ')
        else:
            if 0 < int(score_matrix[align_result[0][i]][align_result[1][i]]):
                alignment.append(':')
            else:
                alignment.append('.')
    separation = 0
    for x in range(int(length / max_print) + 1):
        j = x * max_print
        k = x * max_print + max_print
        if k >= length:
            k = length
        separation = k-j
        separate(2*separation)
        for i in range(j, k):
            print(align_result[0][i], end=' ')
        print()
        for i in range(j, k):
            print(alignment[i], end=' ')
        print()
        for i in range(j, k):
            print(align_result[1][i], end=' ')
        print()
        if k == length:
            break
    separate(2*separation)
parse_input()
read_strings()
read_score_matrix()
affine_aline()
print_result(traceback())

