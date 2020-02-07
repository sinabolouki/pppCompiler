class CodeGenerator:
    def __init__(self, SS, ST, res_dic):
        self.ST = ST
        self.SS = SS
        print("SS: ", self.SS)
        self.res_dic = res_dic
        self.pc = 0
        self.temp_num = 1
        self.lab_num = 0

    def get_temp(self):
        temp = ''
        temp += str(self.temp_num)
        self.temp_num += 1
        return temp


    def push_id(self, token):
        self.SS.append(token)

    def make_stdscp(self, value,type, size, string_size=None):
        dscp = {}
        dscp['value'] = value
        dscp['type'] = type
        dscp['size'] = size
        if size == 'STRING':
            dscp['string_size'] = string_size
        return dscp

    def push_const(self, token):
        var_name = self.get_temp()
        if token.type == 'STRING':
            st_row = self.make_stdscp(token.value, 'im', token.type, len(token.value))
        else:
            st_row = self.make_stdscp(token.value, 'im', token.type)
        self.ST[var_name] = st_row
        self.SS.append(var_name)

    def check_type(self, op1, op2):
        st1 = self.ST[op1]
        st2 = self.ST[op2]
        if st1['size'] == st2['size']:
            return st1['size']
        else:
            # error
            pass

    def start_branch_if(self, token):
        var = self.SS.pop()
        self.res_dic[self.pc] = ['br', 'i1', '%' + var + ',', 'label %', 'label %']
        self.pc += 1
        true_label = self.get_temp()
        self.res_dic[self.pc] = ["<label>: " + true_label + ": "]
        self.res_dic[self.pc - 1][3] += true_label
        self.SS.append(self.pc - 1)

    def start_loop(self, token):
        loop_label = self.get_temp()
        self.res_dic[self.pc] = ["<label>: " + loop_label + ": "]
        self.SS.append(loop_label)
        self.pc += 1

    def loop_first_comp(self, token):
        var = self.SS.pop()
        self.res_dic[self.pc] = ['br', 'i1', '%' + var, ', label %', ', label %']
        true_label = self.get_temp()
        false_label = self.get_temp()
        self.SS.append(false_label)
        self.res_dic[self.pc] += true_label
        self.pc += 1
        self.res_dic[self.pc] = ["<label>: " + true_label + ": "]
        self.res_dic[self.pc - 1][3] += true_label
        self.SS.append(self.pc - 1)
        self.pc += 1

    def comp_loop(self, token):
        loop_pc = self.SS.pop()
        false_label = self.SS.pop()
        loop_label = self.get_temp()
        self.res_dic[self.pc + 1] = ["<label>: "+false_label + ": "]
        self.res_dic[self.pc] = ['br label %' + loop_label]
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

    def add(self, token):
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

    def sub(self, token):
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

    def mul(self, token):
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

    def div(self, token):
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

    def les(self, token):
        first_op_token = self.SS.pop()
        second_op_token = self.SS.pop()
        print(first_op_token, second_op_token)
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'icmp  slt i1'
            self.res_dic[self.pc][3] = '%' + first_op_token
            self.res_dic[self.pc][4] = '%' + second_op_token

    def var_dcl_array(self, id):
        self.res_dic[self.pc] = []
        pass
