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

    def push_new_id(self, token):
        # self.ST[token.value] = {}
        self.SS.append(token.value)

    def push_id(self, token):
        if token.value in self.ST:
            temp_var = self.get_temp()
            # self.SS.append(token.value)
            self.res_dic[self.pc] = ['%'+temp_var+'= load ' , '', ', ']
            if self.ST[token.value]['size'] =='INT':
                self.res_dic[self.pc][1] += 'i32'
                self.res_dic[self.pc][2] += 'i32* %' + token.value
                self.ST[temp_var] = self.make_stdscp(temp_var, 'temp', 'INT')
                self.SS.append(temp_var)
            #TODO
            self.pc += 1
        else:
            print('error :', token.value,'not declared')


    def assign_simple(self,token):
        var_name = self.SS.pop()
        res_name = self.SS[-1]
        type = check

    def make_stdscp(self, value, type, size, string_size=None):
        dscp = {}
        dscp['value'] = value
        dscp['type'] = type
        dscp['size'] = size
        if size == 'STRING':
            dscp['string_size'] = string_size
        return dscp

    def assign(self, token):
        expr_res = self.SS.pop()
        ass_var = self.SS.pop()
        self.res_dic[self.pc] = ['store ', '', ', ']
        print('vars: ', expr_res, ass_var)
        print('ss: ',self.ST)
        type = self.check_type(expr_res, ass_var)
        if type == 'INT':
            self.res_dic[self.pc][0] += 'i32'
            self.res_dic[self.pc][2] += 'i32* '
            self.res_dic[self.pc][1] += '%'+expr_res
            self.res_dic[self.pc][2] += '%'+ass_var
        #TODO: rest of types
        self.pc += 1

    def pop_id(self, token):
        pass
        # self.SS.pop()

    def push_const(self, token):
        var_ptr = self.get_temp()
        self.res_dic[self.pc] = ['%'+var_ptr, '= alloca', '']
        self.res_dic[self.pc + 1] = ['store ', '', ', ']
        var_name = self.get_temp()
        self.res_dic[self.pc + 2] = ['%'+var_name, '= load ', ', ']
        if token.type == 'INT':
            self.res_dic[self.pc][2] += 'i32'
            self.res_dic[self.pc + 1][1] += 'i32 '
            self.res_dic[self.pc + 1][1] += token.value
            self.res_dic[self.pc + 1][2] += 'i32* %'+var_ptr
            self.res_dic[self.pc + 2][1] += 'i32'
            self.res_dic[self.pc + 2][2] += 'i32* %' + var_ptr
            # TODO:
        if token.type == 'STRING':
            st_row = self.make_stdscp(token.value, 'im', token.type, len(token.value))
        else:
            st_row = self.make_stdscp(token.value, 'im', token.type)
        self.ST[var_name] = st_row
        self.SS.append(var_name)
        self.pc += 3

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
        self.pc += 1

    def start_loop(self, token):
        loop_label = self.get_temp()
        self.res_dic[self.pc] = ["<label>: " + loop_label + ": "]
        self.SS.append(loop_label)
        self.pc += 1

    def loop_first_comp(self, token):
        print("loop stack" , self.SS)
        var = self.SS.pop()
        self.res_dic[self.pc] = ['br', 'i1', '%' + var, ', label %', ', label %']
        true_label = self.get_temp()
        false_label = self.get_temp()
        self.SS.append(false_label)
        self.pc += 1
        self.res_dic[self.pc] = ["<label>: " + true_label + ": "]
        self.res_dic[self.pc - 1][3] += true_label
        self.res_dic[self.pc - 1][4] += false_label
        self.pc += 1

    def comp_loop(self, token):
        print("Stack: ", self.SS)
        false_label = self.SS.pop()
        loop_label = self.SS.pop()
        self.res_dic[self.pc + 1] = ["<label>: "+false_label + ": "]
        self.res_dic[self.pc] = ['br label %' + loop_label]
        self.pc += 2

    def push_type(self, token):
        self.SS.append(token.type)

    def var_dcl_simple(self, token):
        type = self.SS.pop()
        id_token = self.SS[-1]
        self.res_dic[self.pc] = ['%', '=', 'alloca', '']
        self.res_dic[self.pc][0] += id_token
        print('type: ', type)
        print(id_token)
        if type == 'INTEGER':
            print('vared')
            self.res_dic[self.pc][3] += 'i32'
            self.ST[id_token] = self.make_stdscp(None, 'var_ptr', 'INT')
            print(self.ST)
        elif type == 'CHAR':
            self.res_dic[self.pc][3] += 'i8'
            self.St[id_token]['size'] = 'CHAR'
        elif type == 'REAL':
            self.res_dic[self.pc][3] += 'float'
            self.ST[self.res_dic[self.pc][0][1:]] = ('REAL')
        elif type == 'BOOLEAN':
            self.res_dic[self.pc][3] += 'i1'
            self.ST[self.res_dic[self.pc][0][1:]] = ('BOOL')
        elif type == 'STRING':
            self.res_dic[self.pc][3] = 'i64*'
            self.ST[self.res_dic[self.pc][0][1:]] = ('STRING')
        self.pc += 1

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
        self.res_dic[self.pc] = ['%', '=', '', '%', '%']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'add i32'
            self.res_dic[self.pc][3] += first_op_token + ','
            self.res_dic[self.pc][4] += second_op_token
        elif type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fadd float'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass

        temp = self.get_temp()
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1

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
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1


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
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1

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
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1


    def les(self, token):
        print("les stack: ", self.SS)
        first_op_token = self.SS.pop()
        second_op_token = self.SS.pop()
        print(first_op_token, second_op_token)
        print(self.res_dic)
        temp_var = self.get_temp()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        self.res_dic[self.pc][0] += temp_var
        self.ST[temp_var] = self.make_stdscp(None, 'temp', 'BOOL')
        if type == 'INT':
            self.res_dic[self.pc][2] = 'icmp slt i1'
            self.res_dic[self.pc][3] = '%' + first_op_token
            self.res_dic[self.pc][4] = '%' + second_op_token
        self.SS.append(temp_var)
        self.pc += 1

    def var_dcl_array(self, id):
        self.res_dic[self.pc] = []
        pass
