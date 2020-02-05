import scanner
import csv

file = open('sampleText.txt')

scanner = scanner.Scanner(file)
parse_table_reader = csv.DictReader(open('parseTable.csv', 'r'), delimiter = ',')
parse_table_list = []
for row in parse_table_reader:
    print(row['REAL'])
    parse_table_list.append(row)
state = 0
token = scanner.parseToken()
parse_stack = []


def generate_code(func_name):
    if func_name == 'NoSem':
        return




while token.type != 'EOF':
    table_cell = parse_table_list[state][token.type]
    tc_splitted = table_cell.split()
    if tc_splitted[0] == 'REDUCE':
        next_state = parse_stack.pop()
        state = next_state
    elif tc_splitted[0] == 'PUSH_GOTO':
        parse_stack.append(state)
        next_state = int(str(list(tc_splitted[1])[1:]))
        generate_code(tc_splitted[2])
    elif tc_splitted[0] == 'SHIFT':
        next_state = int(str(list(tc_splitted[1])[1:]))
        generate_code(tc_splitted[2])
    else:
        print('errror in line filan')
        break
    token = scanner.parseToken()