import re


class CodeGenerator:
    def __init__(self, SS, ST, res_dic):
        self.ST = ST
        self.SS = SS
        #print("SS: ", self.SS)
        self.res_dic = res_dic
        self.pc = 0
        self.min_pc = 0
        self.temp_num = 1
        self.lab_num = 0
        self.func_arg_count = 0
        self.string_const = 3
        self.res_dic[0] = ['@.str = private unnamed_addr constant [3 x i8] c"%d\\00", align 1\n']
        self.res_dic[0][0] += '@.str.1 = private unnamed_addr constant [3 x i8] c"%c\\00", align 1\n'
        self.res_dic[0][0] += '@.str.2 = private unnamed_addr constant [3 x i8] c"%s\\00", align 1\n'
        self.res_dic[0][0] += '@.str.3 = private unnamed_addr constant [3 x i8] c"%f\\00", align 1\n'
        self.res_dic[1] = ['declare i32 @scanf(i8*, ...)\n']
        self.res_dic[1][0] += 'declare i32 @printf(i8*, ...)'
        self.pc += 2

    def add_printf_scanf(self):
        printf_dscp = {'value':None, 'type':'func', 'size':'INT'}
        scanf_dscp = {'value': None}
        self.ST['write'] = printf_dscp

    def get_temp(self):
        temp = ''
        temp += str(self.temp_num)
        self.temp_num += 1
        return temp

    def get_string_temp(self):
        self.string_const += 1
        return '.str.'+str(self.string_const)

    def make_stdscp(self, value, type, size, string_size=None):
        dscp = {}
        dscp['value'] = value
        dscp['type'] = type
        dscp['size'] = size
        if size == 'STRING':
            dscp['string_size'] = string_size
        return dscp

    def pop_var(self, token):
        self.SS.pop()


    def push_new_id(self, token):
        # self.ST[token.value] = {}
        self.SS.append(token.value)

    def push_id(self, token):
        if token.value in self.ST:
            if self.ST[token.value]['type'] == 'var_ptr':
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
            elif self.ST[token.value]['type'] == 'func':
                self.SS.append(token.value)
        else:
            print('error :', token.value,'not declared')


    def assign_simple(self,token):
        pass
        # var_name = self.SS.pop()
        # res_name = self.SS[-1]
        # type = check

    def dcl_assign(self, token):
        expr_res = self.SS.pop()
        ass_var = self.SS[-1]
        self.res_dic[self.pc] = ['store ', '', ', ']
        #print('vars: ', expr_res, ass_var)
        #print('ss: ', self.ST)
        type = self.check_type(expr_res, ass_var)
        if type == 'INT':
            self.res_dic[self.pc][0] += 'i32'
            self.res_dic[self.pc][2] += 'i32* '
            self.res_dic[self.pc][1] += '%' + expr_res
            self.res_dic[self.pc][2] += '%' + ass_var
        # TODO: rest of types
        self.pc += 1

    def assign(self, token):
        expr_res = self.SS.pop()
        ass_var = self.SS.pop()
        self.res_dic[self.pc] = ['store ', '', ', ']
        #print('vars: ', expr_res, ass_var)
        #print('ss: ',self.ST)
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

    # string handling
    def push_const_string(self, token):
        const_name = self.get_string_temp()
        string = token.value
        slash_count = 1
        strlen = len(string)
        self.res_dic[0][0] += '@' + const_name + ' = private unnamed_addr constant ['+str(strlen  + slash_count)+' x i8] c"'+string+'\\00", align 1\n'
        self.ST[const_name] = self.make_stdscp(string, 'temp', 'STRING', strlen)
        self.SS.append(const_name)


    def check_type(self, op1, op2):
        st1 = self.ST[op1]
        st2 = self.ST[op2]
        if st1['size'] == st2['size']:
            return st1['size']
        else:
            # error
            pass


    # loop functions:

    def start_loop(self, token):
        loop_label = self.get_temp()
        self.res_dic[self.pc] = ['br label %'+loop_label]
        self.res_dic[self.pc + 1] = [";<label>:" + loop_label + ": "]
        self.SS.append(loop_label)
        self.pc += 2

    def loop_first_comp(self, token):
        var = self.SS.pop()
        self.res_dic[self.pc] = ['br', 'i1', '%' + var, ', label %', ', label %']
        true_label = self.get_temp()
        self.SS.append(self.pc)
        self.pc += 1
        self.res_dic[self.pc] = [";<label>:" + true_label + ": "]
        self.res_dic[self.pc - 1][3] += true_label
        self.pc += 1

    def comp_loop(self, token):
        #print("Stack: ", self.SS)
        loop_pc = self.SS.pop()
        false_label = self.get_temp()
        loop_label = self.SS.pop()
        self.res_dic[self.pc + 1] = [";<label>:"+false_label + ": "]
        self.res_dic[self.pc] = ['br label %' + loop_label]
        self.res_dic[loop_pc][4] += false_label
        self.pc += 2


    # return functions:
    def return_int(self, token):
        value = token.value
        self.res_dic[self.pc] = ['ret i32 ' + value]
        self.pc += 1

    def return_real(self,token):
        value = token.value
        self.res_dic[self.pc] = ['ret float' + value]
        self.pc += 1

    def return_id(self, token):
        self.res_dic[self.pc] = ['%', '=load ', '']
        self.res_dic[self.pc + 1] = ['ret ']
        temp_var = self.get_temp()
        self.res_dic[self.pc][0] += temp_var
        id_name = token.value
        if self.ST[id_name]['size'] == 'INT':
            self.res_dic[self.pc][1] += 'i32, '
            self.res_dic[self.pc][2] += 'i32* %' + id_name
            self.res_dic[self.pc + 1][0] += 'i32 %' + temp_var
        elif self.ST[id_name]['size'] == 'REAL':
            self.res_dic[self.pc][1] += 'float'
            self.res_dic[self.pc][2] += 'float* %' + id_name
            self.res_dic[self.pc + 1][0] += 'float %' + temp_var
        else:
            pass
            #TODO
        self.pc += 2


    #declaration functions:

    def push_type(self, token):
        self.SS.append(token.type)

    def var_dcl_simple(self, token):
        type = self.SS.pop()
        id_token = self.SS[-1]
        self.res_dic[self.pc] = ['%', '=', 'alloca', '']
        self.res_dic[self.pc][0] += id_token
        #print('type: ', type)
        #print(id_token)
        if type == 'INTEGER':
            #print('vared')
            self.res_dic[self.pc][3] += 'i32'
            self.ST[id_token] = self.make_stdscp(None, 'var_ptr', 'INT')
            #print(self.ST)
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
        self.res_dic[self.pc] = ['%', '=', '', '%', '%']
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

    def rem(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'srem i32'
            self.res_dic[self.pc][3] += first_op_token + ', '
            self.res_dic[self.pc][4] += second_op_token
        elif type == 'FLOAT':
            self.res_dic[self.pc][2] = 'frem float'
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

# --- 2 operand bitwise commands

    def bitwise_and(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '%', '%']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'and i32'
            self.res_dic[self.pc][3] += first_op_token + ','
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1

    def bitwise_or(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '%', '%']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'or i32'
            self.res_dic[self.pc][3] += first_op_token + ','
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1

    def bitwise_xor(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '%', '%']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'INT':
            self.res_dic[self.pc][2] = 'xor i32'
            self.res_dic[self.pc][3] += first_op_token + ','
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1

    # negate
    def negate(self, token):
        op_token = self.SS.pop()
        type = self.ST[op_token]['size']
        self.res_dic[self.pc] = ['%', '=', '', '', '%']
        if type == 'INT':
            self.res_dic[self.pc][2] = 'sub i32'
            self.res_dic[self.pc][3] += '0,'
            self.res_dic[self.pc][4] += op_token
        elif type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fsub float'
            self.res_dic[self.pc][3] += '0,'
            self.res_dic[self.pc][4] += op_token
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1

    # ---- 1-bit operations ---
    # not command
    def bitnot(self, token):
        op_token = self.SS.pop()
        type = self.ST[op_token]['size']
        if type == 'BOOL':
            self.res_dic[self.pc] = ['%', '=', '', '%']
            self.res_dic[self.pc][2] = 'xor i1'
            self.res_dic[self.pc][3] += op_token
            self.res_dic[self.pc][3] += ', 1'
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1

    #logical and
    def logical_and(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '%', '%']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'BOOL':
            self.res_dic[self.pc][2] = 'and i1'
            self.res_dic[self.pc][3] += first_op_token + ','
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1

    #logical or
    def logical_or(self, token):
        second_op_token = self.SS.pop()
        first_op_token = self.SS.pop()
        self.res_dic[self.pc] = ['%', '=', '', '%', '%']
        type = self.check_type(first_op_token, second_op_token)
        if type == 'BOOL':
            self.res_dic[self.pc][2] = 'or i1'
            self.res_dic[self.pc][3] += first_op_token + ','
            self.res_dic[self.pc][4] += second_op_token
        else:
            # TODO: other types
            pass
        temp = self.get_temp()
        self.ST[temp] = self.make_stdscp(None, 'temp', type)
        self.res_dic[self.pc][0] += temp
        self.SS.append(temp)
        self.pc += 1


# ---- Comparing Commands ---

    def les(self, token):
        #print("les stack: ", self.SS)
        first_op_token = self.SS.pop()
        second_op_token = self.SS.pop()
        #print(first_op_token, second_op_token)
        #print(self.res_dic)
        temp_var = self.get_temp()
        self.res_dic[self.pc] = ['%', '=', '', '', ', ']
        type = self.check_type(first_op_token, second_op_token)
        self.res_dic[self.pc][0] += temp_var
        self.ST[temp_var] = self.make_stdscp(None, 'temp', 'BOOL')
        if type == 'INT':
            self.res_dic[self.pc][2] = 'icmp slt i32'
            self.res_dic[self.pc][3] += '%' + first_op_token
            self.res_dic[self.pc][4] += '%' + second_op_token
        if type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fcmp olt'
            self.res_dic[self.pc][3] += '%' + first_op_token
            self.res_dic[self.pc][4] += '%' + second_op_token
        self.SS.append(temp_var)
        self.pc += 1

    def greater(self, token):
        first_op_token = self.SS.pop()
        second_op_token = self.SS.pop()
        temp_var = self.get_temp()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        self.res_dic[self.pc][0] += temp_var
        self.ST[temp_var] = self.make_stdscp(None, 'temp', 'BOOL')
        if type == 'INT':
            self.res_dic[self.pc][2] = 'icmp sgt i32'
            self.res_dic[self.pc][3] = '%' + first_op_token
            self.res_dic[self.pc][4] = '%' + second_op_token
        if type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fcmp ogt'
            self.res_dic[self.pc][3] = '%' + first_op_token
            self.res_dic[self.pc][4] = '%' + second_op_token
        self.SS.append(temp_var)
        self.pc += 1

    def is_equal(self, token):
        first_op_token = self.SS.pop()
        second_op_token = self.SS.pop()
        temp_var = self.get_temp()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        self.res_dic[self.pc][0] += temp_var
        self.ST[temp_var] = self.make_stdscp(None, 'temp', 'BOOL')
        if type == 'INT':
            self.res_dic[self.pc][2] = 'icmp eq i32'
            self.res_dic[self.pc][3] += '%' + first_op_token
            self.res_dic[self.pc][4] += ', %' + second_op_token
        if type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fcmp oeq'
            self.res_dic[self.pc][3] += '%' + first_op_token
            self.res_dic[self.pc][4] += ', %' + second_op_token
        self.SS.append(temp_var)
        self.pc += 1

    def isnot_equal(self, token):
        first_op_token = self.SS.pop()
        second_op_token = self.SS.pop()
        temp_var = self.get_temp()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        self.res_dic[self.pc][0] += temp_var
        self.ST[temp_var] = self.make_stdscp(None, 'temp', 'BOOL')
        if type == 'INT':
            self.res_dic[self.pc][2] = 'icmp ne i32'
            self.res_dic[self.pc][3] += '%' + first_op_token
            self.res_dic[self.pc][4] += ', %' + second_op_token
        if type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fcmp one'
            self.res_dic[self.pc][3] += '%' + first_op_token
            self.res_dic[self.pc][4] += ', %' + second_op_token
        self.SS.append(temp_var)
        self.pc += 1

    def less_equal(self, token):
        first_op_token = self.SS.pop()
        second_op_token = self.SS.pop()
        temp_var = self.get_temp()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        self.res_dic[self.pc][0] += temp_var
        self.ST[temp_var] = self.make_stdscp(None, 'temp', 'BOOL')
        if type == 'INT':
            self.res_dic[self.pc][2] = 'icmp sle i32'
            self.res_dic[self.pc][3] += '%' + first_op_token
            self.res_dic[self.pc][4] += ', %' + second_op_token
        if type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fcmp ole'
            self.res_dic[self.pc][3] += '%' + first_op_token
            self.res_dic[self.pc][4] += ', %' + second_op_token
        self.SS.append(temp_var)
        self.pc += 1

    def greater_equal(self, token):
        first_op_token = self.SS.pop()
        second_op_token = self.SS.pop()
        temp_var = self.get_temp()
        self.res_dic[self.pc] = ['%', '=', '', '', '']
        type = self.check_type(first_op_token, second_op_token)
        self.res_dic[self.pc][0] += temp_var
        self.ST[temp_var] = self.make_stdscp(None, 'temp', 'BOOL')
        if type == 'INT':
            self.res_dic[self.pc][2] = 'icmp sge i32'
            self.res_dic[self.pc][3] = '%' + first_op_token
            self.res_dic[self.pc][4] = '%' + second_op_token
        if type == 'FLOAT':
            self.res_dic[self.pc][2] = 'fcmp oge'
            self.res_dic[self.pc][3] = '%' + first_op_token
            self.res_dic[self.pc][4] = '%' + second_op_token
        self.SS.append(temp_var)
        self.pc += 1

    # ---- End of comparing commands ---

    # function declaration functions
    def make_fdcsp(self):
        dcsp = {}
        dcsp['type'] = 'func'
        dcsp['size'] = None
        dcsp['vars'] = []
        return dcsp

    def add_arg(self,token):
        pass

    def push_func_id(self, token):
        self.SS.append(token.value)


    def define_func(self, token):
        self.res_dic[self.pc] = ['define ', '@', '( ', ') {']
        func_name = token.value
        self.res_dic[self.pc][1] += func_name
        self.ST[func_name] = self.make_fdcsp()


    def set_type(self, token):
        function_name = self.res_dic[self.pc][1][1:]
        type = self.SS.pop()
        if type == 'INTEGER':
            self.res_dic[self.pc][0] += 'i32'
            self.ST[function_name]['size'] = 'INT'
        elif type == 'CHAR':
            self.res_dic[self.pc][0] += 'i8'
            self.ST[function_name]['size'] = 'CHAR'
        elif type == 'REAL':
            self.res_dic[self.pc][0] += 'float'
            self.ST[function_name]['size'] = 'REAL'
        elif type == 'STRING':
            # TODO
            pass
        self.pc += 1

    def end_func(self, token):
        self.res_dic[self.pc] = ['}']
        self.pc += 1

    def func_call(self, token):
        temp_var = self.get_temp()
        self.res_dic[self.pc] = ['%' + temp_var, ' =', 'call', '',  '(', ') @', '(']
        arg_size = [', '] * self.func_arg_count
        arg_size[0] = ['']
        args = [', '] * self.func_arg_count
        args[0] = ['']
        while self.func_arg_count >= 0:
            arg = self.SS.pop()
            self.func_arg_count -= 1
            if self.ST[arg]['size'] == 'INT':
                arg_size[self.func_arg_count] += 'i32'
                args[self.func_arg_count] += 'i32 %' + arg
            elif self.ST[arg]['size'] == 'FLOAT':
                arg_size[self.func_arg_count] += 'float'
                args[self.func_arg_count] += 'float %' + arg
            else:
                pass
                # TODO
        self.res_dic[self.pc][4] += "".join(arg_size)
        self.res_dic[self.pc][6] += ''.join(args)
        self.res_dic[self.pc][6] += ')'
        func_name = self.SS.pop()
        if self.ST[func_name]['size'] == 'INT':
            self.res_dic[self.pc][3] = 'i32'
            self.ST[temp_var] = self.make_stdscp(None, 'temp', 'INT')
        elif self.ST[func_name]['size'] == 'FLOAT':
            self.res_dic[self.pc][3] = 'float'
            self.ST[temp_var] = self.make_stdscp(None, 'temp', 'REAL')
        else:
            pass
            #TODO
        self.res_dic[self.pc][5] += func_name
        self.pc += 1

    def write(self, token):
        var = self.SS.pop()
        temp = self.get_temp()
        if self.ST[var]['size'] == 'INT':
            self.res_dic[self.pc] = ['%'+temp, '= call i32 (i8*, ...) @printf(i8* getelementptr inbounds'
                            ' ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), ', 'i32 %'+var + ')']
        elif self.ST[var]['size'] == 'FLOAT':
            self.res_dic[self.pc] = ['%' + temp, '= call i32 (i8*, ...) @printf(i8* getelementptr inbounds'
                            ' ([3 x i8], [3 x i8]* @.str.2, i32 0, i32 0), ', 'float %' + var + ')']
        elif self.ST[var]['size'] == 'STRING':
            string = self.ST[var]['value']
            slash_count = 1
            self.res_dic[self.pc] = ['%' + temp, '= call i32 (i8*, ...) @printf(i8* getelementptr inbounds'
                            ' (['+str(self.ST[var]['string_size'] + slash_count)+' x i8],'
                                 ' ['+str(self.ST[var]['string_size'] + slash_count)+' x i8]* @'+var+', i32 0, i32 0))']
        else:
            pass
            #TODO
        self.pc += 1

    def read_id(self, token):
        self.SS.append(token.value)

    def read(self, token):
        read_id = self.SS.pop()
        temp_var = self.get_temp()
        self.res_dic[self.pc] = ['%'+temp_var, '']
        if self.ST[read_id]['size'] == 'INT':
            self.res_dic[self.pc][1] += '= call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]' \
                                     '* @.str, i32 0, i32 0), i32* %' + read_id + ')'
        elif self.ST[read_id]['size'] == 'CHAR':
            self.res_dic[self.pc][1] += '= call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]*' \
                                     ' @.str.1, i32 0, i32 0), i8* %' + read_id + ')'
        self.pc += 1

    #---if_codes
    def start_branch_if(self, token):
        var = self.SS.pop()
        self.res_dic[self.pc] = ['br', 'i1', '%' + var, ', label %', ', label %']
        true_label = self.get_temp()
        self.SS.append(self.pc)
        self.pc += 1
        self.res_dic[self.pc] = [";<label>:" + true_label + ": "]
        self.res_dic[self.pc - 1][3] += true_label
        self.pc += 1

    def end_if(self, token):
        if_pc = self.SS.pop()
        false_label = self.get_temp()
        self.res_dic[self.pc ] = ['br label %'+false_label]
        self.res_dic[self.pc + 1]  = [';<label>: ' + false_label + ": "]
        self.res_dic[if_pc][4] += false_label
        self.pc += 2

    def start_else(self, token):
        self.res_dic[self.pc - 2] = ['br label %']
        self.SS.append(self.pc - 2)

    def comp_else(self, token):
        if_pc = self.SS.pop()
        label_num = self.get_temp()
        self.res_dic[self.pc] = ['br label %'+label_num]
        self.res_dic[self.pc+1] = [';<label>: '+label_num+":"]
        self.res_dic[if_pc][0] += label_num
        self.pc+=2

