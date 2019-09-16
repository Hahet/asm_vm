
# coding=UTF-8


class Config(object):

    def __init__(self):
        self.registers = {
            'pa': 0,
            'a1': 16,
            'a2': 32,
            'a3': 48,
            'c1': 64,
            'f1': 80,
        }
        self.instructions = {

            'set': {
                'code': 0,
                'step': 3,
            },
            'load': {
                'code': 1,
                'step': 4,
            },
            'add': {
                'code': 2,
                'step': 4,
            },
            'save': {
                'code': 3,
                'step': 4,
            },
            'compare': {
                'code': 4,
                'step': 3,
            },
            'jump_if_less': {
                'code': 5,
                'step': 3
            },
            'jump': {
                'code': 6,
                'step': 3,
            },
            'save_from_register': {
                'code': 7,
                'step': 3,
            },
            'set2': {
                'code': 8,
                'step': 4,
            },
            'load2': {
                'code': 9,
                'step': 4,
            },
            'add2': {
                'code': 10,
                'step': 4,
            },
            'save2': {
                'code': 11,
                'step': 4,
            },
            'subtract2': {
                'code': 12,
                'step': 4,
            },

            'load_from_register':  {
                'code': 13,
                'step': 3,
            },
            'load_from_register2': {
                'code': 14,
                'step': 3
            },
            'save_from_register2': {
                'code': 15,
                'step': 3
            },

            'jump_from_register': {
                'code': 16,
                'step': 2
            },
            'shift_right': {
                'code': 17,
                'step': 2,
            },
            'and': {
                'code': 19,
                'step': 4,
            },
            'halt':  {
                'code': 255,
                'step': 1,
            },
            'debug': {
                'code': 235,
                'step': 1,
            }

        }

# 将一个地址或者数字转成两个字节表示


def format_nummber(n):
    result = []
    if (n < 256):
        result = [n, 0]
    else:
        s = bin(n)[2:]
        small = s[-8:]
        small_number = int(small, 2)
        result.append(small_number)
        index = len(s) - 8
        big = s[0: index]
        big_number = int(big, 2)
        result.append(big_number)
    return result


def parse(s):
    return s.split(' ')


def not_empty(s):
    return s and s.strip()


def valid_list(array):
    r = []
    for l in array:
        index = l.find(';')
        if index != -1:
            x = l[0:index]
            r.append(x.strip())
        else:
            r.append(l.strip())

    array2 = list(filter(not_empty, r))
    r2 = []
    for l in array2:
        index = l.find('#')
        if index != -1:
            x = l[0:index]
            r2.append(x.strip())
        else:
            r2.append(l.strip())

    result2 = list(filter(not_empty, r2))

    return result2


def merge_list(array):
    r = []
    for a in array:

        r = r + a
    return r


def replace_call_and_return(array):

    old = '.call'
    new = """
    set2 a3 14 ;1097
    add2 pa a3 a3
    save_from_register2 a3 f1 ; 3byte

    set2 a3 2 ; 4byte
    add2 f1 a3 f1 ; 4byte

    ; jump @function_multiply ; 3byte
    """

    return_asm = """
        ;set2 a3 8                   ; 读取「变量 4」
        subtract2 f1 a3 f1          ;
        load_from_register2 f1 a2
        jump_from_register a2
    """
    replace_call_array = pretreated_list(new)
    replace_return_list = pretreated_list(return_asm)

    i = 0

    while i < len(array):
        a = array[i]
        if a[0] == old:
            call_address = a[1]
            # new_list.append(['jump', call_address])
            call_list = replace_call_array + [['jump', call_address]]
            left = array[0:i]
            right = array[(i + 1):]
            array = left + call_list + right
        if a[0] == '.return':
            n = 2 + int(a[1])
            return_list = [['set2', 'a3', str(n)]] + replace_return_list
            left = array[0:i]
            right = array[(i + 1):]
            array = left + return_list + right
        i = i + 1
    return array


def labels_address(array):
    instructions = Config().instructions
    labels = {

    }
    address = 0
    for i, a in enumerate(array):
        b = a[0]
        if (b == '.memory'):
            address = int(a[1])
        if (b == '.data'):
            address = address + int(len(array[i + 1]))
        if b in instructions.keys():
            instruction = instructions[b]
            address = address + instruction['step']
        if b.find('@') != -1:
            s = b[1:]
            if (not s.isdigit()):
                # 当前为label行 不占地址长度
                labels[b] = address
    return labels


def replace_one_line(line, labels):
    instructions = Config().instructions
    registers = Config().registers
    results = []
    # 每一行的第一条是指令
    instruction_key = line[0]
    results.append(instructions[instruction_key]['code'])
    array = line[1:]

    # 后面的在循环里面替换
    for a in array:
        # 是寄存器，就去寄存器dict里面替换
        if a in registers.keys():
            results.append(registers[a])
        # 如果是数字， 直接append
        if a.isdigit():
            if instruction_key == 'set':
                results = results + [int(a)]
            else:
                results = results + format_nummber(int(a))

        # 如果有@， 就是地址或者label
        if a.find('@') != -1:
            s = a[1:]
            # 数字是地址
            if s.isdigit():
                # results.append(int(a[1:]))
                results = results + format_nummber(int(a[1:]))
            # 其他的是jump的地址， 需要在之前得到的labels dict里面取机器码
            else:
                results = results + format_nummber(labels[a])
                # results.append(labels[a])
    return results


def replace_lines_list(array, labels):
    new_labels = labels
    results = []
    # index = 0
    for index, a in enumerate(array):
        # for a in array:

        # while index < len(array):
        #     a = array[index]
        # if a[0] == '.data':
        #     pass
        if a[0] == '.data':
            data = array[index + 1]
            data = list(map(lambda s: int(s), data))
            results.append(data)
            if len(data) > 0:
                array.pop(index + 1)
            # labels都需要加上 length
            continue
        if a[0] == '.memory':
            # 把前1024个内存中空余的用0填充
            t = 0
            #  计算当前result拍平的长度
            for b in results:
                t = t + len(b)
            length = int(a[1]) - t
            results = results + [[0] * length]
            continue
        # 如果当前行（数组）第一项不是label，就进行机器码替换。 是label的直接忽略，因为label只是汇编里面定位用的
        if not (a[0] in labels.keys()):
            line = replace_one_line(a, new_labels)
            results.append(line)
        index = index + 1
    return results


def pretreated_list(asm):
    # 按照行拆分
    list1 = asm.split('\n')
    # 去掉注释和空行
    list2 = valid_list(list1)
    # 按空格拆分每一行，list3是个二维数组
    list3 = list(map(parse, list2))
    return list3


def machine_code(asm):
    """
    asm 是汇编语言字符串
    返回 list, list 中每个元素是一个 1 字节的数字
    """

    list2 = pretreated_list(asm)
    list3 = replace_call_and_return(list2)
    # dict： 每个label 对应的位置
    labels = labels_address(list3)
    # 把数组的汇编字符串替换成 机器码
    replaced_list = replace_lines_list(list3, labels)
    # 拍平二维数组
    results = merge_list(replaced_list)
    # return results
    return results + [0] * (65536 - len(results))


def test():
    test_asm_code3 = """
    jump @1024
    .memory 1024

    set2 f1 3
    jump @function_end

    ; a1, a2 用来存参数
    @function_multiply ;1031
    set2 a3 2
    ; 65534(a1), 65532(a2), 65530(a3),
    save2 a1 @65534

    @while_start ;1039
    compare a2 a3
    jump_if_less @while_end

    ; a3 += 1
    save2 a2 @65532
    set2 a2 1
    add2 a3 a2 a3

    ; a1 += a1
    load2 @65534 a2
    add2 a1 a2 a1

    ;
    load2 @65532 a2
    jump @while_start
    @while_end

    ; f1 -= 2
    set2 a3 2
    subtract2 f1 a3 f1
    load_from_register2 f1 a2
    jump_from_register a2

    @function_end ;1085

    ; 调用函数
    set2 a1 300
    set2 a2 10

    ; 保存函数执行结束后去往的地址
    set2 a3 14 ;1097
    add2 pa a3 a3
    save_from_register2 a3 f1 ; 3byte

    set2 a3 2 ; 4byte
    add2 f1 a3 f1 ; 4byte

    jump @function_multiply ; 3byte
    halt ;1115
    """
    code3 = machine_code(test_asm_code3)
    test_result3 = [
        6, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        8, 80, 3, 0, 6, 61, 4, 8, 48, 2, 0, 11, 16, 254, 255, 4,
        32, 48, 5, 48, 4, 11, 32, 252, 255, 8, 32, 1, 0, 10, 48, 32,
        48, 9, 254, 255, 32, 10, 16, 32, 16, 9, 252, 255, 32, 6, 15, 4,
        8, 48, 2, 0, 12, 80, 48, 80, 14, 80, 32, 16, 32, 8, 16, 44,
        1, 8, 32, 10, 0, 8, 48, 14, 0, 10, 0, 48, 48, 15, 48, 80,
        8, 48, 2, 0, 10, 80, 48, 80, 6, 7, 4, 255,
    ]
    test_result3 = test_result3 + [0] * (65536 - len(test_result3))
    is_eq3 = (code3 == test_result3)
    print(is_eq3)


if __name__ == '__main__':
    test()
