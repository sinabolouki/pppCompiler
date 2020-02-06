class CodeGenerator:
    def __init__(self, PS, SS, ST, res_dic):
        self.ST = ST
        self.PS = PS
        self.SS = SS
        self.res_dic = res_dic
        self.pc = 0
        self.temp_num = 1
        self.lab_num = 0

    def get_temp(self):
        temp = ''
        temp += str(self.temp_num)
        self.temp_num += 1
        return temp

    def get_label(self):
        label = 'label'
        label += str(self.lab_num)
        self.lab_num += 1
        return label

    def push_id(self, token):
        self.SS.apped(token)

    def make_sdcp(self):
        pass

    def check_type(self, op1, op2):
        type1 = self.ST[op1]
        type2 = self.ST[op2]
        if type1 == type2:
            return type1
        else:
            # error
            pass

    def start_branch_if(self, token):
        var = self.SS.pop()
        self.res_dic[self.pc] = ['br', 'i1', '%' + var + ',', 'label ', 'label ']
        self.pc += 1
        true_label = self.get_label()
        self.res_dic[self.pc] = [true_label + ": "]
        self.res_dic[self.pc - 1][3] += true_label
        self.SS.append(self.pc - 1)

    def start_loop(self, token):
        loop_label = self.get_label()
        self.res_dic[self.pc] = [loop_label + ": "]
        self.SS.append(loop_label)
        self.pc += 1

    def loop_first_comp(self, token):
        var = self.SS.pop()
        self.res_dic[self.pc] = ['br', 'i1', '%' + var, ', label ', ', label ']
        true_label = self.get_label()
        false_label = self.get_label()
        self.SS.append(false_label)
        self.res_dic[self.pc] += true_label
        self.pc += 1
        self.res_dic[self.pc] = [true_label + ": "]
        self.res_dic[self.pc - 1][3] += true_label
        self.SS.append(self.pc - 1)
        self.pc += 1

    def comp_loop(self, token):
        loop_pc = self.SS.pop()
        false_label = self.SS.pop()
        loop_label = self.get_label()
        self.res_dic[self.pc + 1] = [false_label + ": "]
        self.res_dic[self.pc] = ['br label ' + loop_label]
        self.res_dic[loop_pc][4] += false_label
        self.pc += 2

    def var_dcl_simple(self, token):
        id_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', 'alloca', '']
        self.res_dic[self.pc][0] += id_token.value
        type = token.type
        if type == 'INTEGER':
            self.res_dic[self.pc][3] += 'i32'
            self.ST[self.res_dic[self.pc][0][1:]] = ('INT')
        elif type == 'CHAR':
            self.res_dic[self.pc][3] += 'i8'
            self.ST[self.res_dic[self.pc][0][1:]] = ('CHAR')
        elif type == 'REAL':
            self.res_dic[self.pc][3] += 'float'
            self.ST[self.res_dic[self.pc][0][1:]] = ('REAL')
        elif type == 'BOOLEAN':
            self.res_dic[self.pc][3] += 'i1'
            self.ST[self.res_dic[self.pc][0][1:]] = ('BOOL')
        elif type == 'STRING':
            self.res_dic[self.pc][3] = 'i64*'
            self.ST[self.res_dic[self.pc][0][1:]] = ('STRING')

    def var_dcl_array(self, token):
        id_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', 'alloca', '']
        self.res_dic[self.pc][0] += id_token.value
        type = token.type
        if type == 'INTEGER':
            pass

    def add_simple(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'add i32'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        elif type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fadd float'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass

        temp = self.get_temp()
        self.ST[temp] = type
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)

    def sub_simple(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'sub i32'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        elif type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fsub float'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = type
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)

    def mul_simple(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'mul i32'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        elif type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fmul float'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = type
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)

    def div_simple(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'sdiv i32'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        elif type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fdiv float'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = type
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)

    def var_dcl_array(self, id):
        self.res_dic[self.pc] = []
        pass
