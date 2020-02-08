import argparse
import scanner as sc
import codeGen
import csv

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-p", "--path", default='sampleText.txt', help='path to your code')
arg = vars(arg_parser.parse_args())
input_path = arg['path']
output_path = ".".join(input_path.split('.')[:-1])+'.ll'
#print(output_path)
file = open(input_path)

scanner = sc.Scanner(file)
parse_table_reader = csv.DictReader(open('feb81807.csv', 'r'), delimiter = ',')
parse_table_list = []
for row in parse_table_reader:
    parse_table_list.append(row)
state = 0
token = scanner.parseToken()
PS = []
ST = {}
SS = []
#print(SS)
res_dic = {}
codeGen = codeGen.CodeGenerator(SS, ST, res_dic)


def generate_code(func_name, token):
    if func_name == 'NoSem':
        return
    getattr(codeGen, func_name[1:])(token)


while True:
    #print('first: ',state)
    # print(token.type, token.value)
    table_cell = parse_table_list[state][token.type]
    tc_splitted = table_cell.split()
    if tc_splitted[0] == 'REDUCE':
        state = PS.pop()
        # print('reduce: ', tc_splitted)
        graph_name = tc_splitted[1]
        goto = parse_table_list[state][graph_name]
        tc_splitted = goto.split()
        if tc_splitted[0] == 'GOTO':
            #print('goto: ',state)
            # print(tc_splitted)
            state = int("".join(list(tc_splitted[1])[1:]))
            generate_code(tc_splitted[2], token)
        else:
            print('ERROR in reduce')

    elif tc_splitted[0] == 'PUSH_GOTO':
        PS.append(state)
        # print(tc_splitted)
        state = int("".join(list(tc_splitted[1])[1:]))
        generate_code(tc_splitted[2], token)
    elif tc_splitted[0] == 'SHIFT':
        state = int("".join(list(tc_splitted[1])[1:]))
        generate_code(tc_splitted[2], token)
        token = scanner.parseToken()
    elif tc_splitted[0] == 'ACCEPT':
        #print('parsing done!')
        break
    else:
        #print(state)
        #print(token.type, token.value)
        #print(tc_splitted)
        #print('error in line filan')
        break

res_text = ''
for i in range(0, codeGen.pc):
    res_text += " ".join(res_dic[i])
    res_text += '\n'
# print(res_text)
with open(output_path, 'w') as output:
    output.write(res_text)
# print(codeGen.SS)