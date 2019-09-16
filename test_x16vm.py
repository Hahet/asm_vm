# coding=UTF-8
import x16asm
import x16vm

cases = [
    ('set a1 1', [0, 16, 1]),
    ('load @100 a1', [1, 100, 0, 16]),
    ('add a1 a2 a1', [2, 16, 32, 16]),
    ('save a1 @100', [3, 16, 100, 0]),
    ('compare a1 a2', [4, 16, 32]),
    ('jump_if_less @200', [5, 200, 0]),
    ('jump @256', [6, 0, 1]),
    ('save_from_register a1 a2', [7, 16, 32]),
    ('halt', [255]),
    ('set2 a1 65535', [8, 16, 255, 255]),
    ('load2 @65534 a3', [9, 254, 255, 48]),
    ('add2 a1 a2 a3', [10, 16, 32, 48]),
    ('save2 a1 @65533', [11, 16, 253, 255]),
    ('subtract2 a1 a2 a3', [12, 16, 32, 48]),
    ('load_from_register a1 a2', [13, 16, 32]),
    ('load_from_register2 a1 a2', [14, 16, 32]),
    ('save_from_register2 a1 c1', [15, 16, 64]),
    ('jump_from_register a1', [16, 16]),
    (
        """
            @label1
            jump @label1
            @label2
            @label3
            jump @label3
            jump @label4
            @label4
            """,
        [6, 0, 0, 6, 3, 0, 6, 9, 0]
    ),
    (
        """
            ; top comments
            @label1 ; inline comments
            jump @label1
            @label2
            @label3
            jump @label3
            jump @label4
            @label4
            ; last line comments
            """,
        [6, 0, 0, 6, 3, 0, 6, 9, 0]
    )
]

# set


def test1():
    AxePU = x16vm.AxePU
    code = cases[0][1] + [255]
    memory = code + [0] * (65536 - len(code))
    cpu = AxePU(memory)
    x16vm._run(cpu)
    output = cpu.data['a1']
    expected = 1
    assert expected == output, output


def test2():
    AxePU = x16vm.AxePU
    case = cases[1]
    code = case[1] + [255]
    memory = code + [0] * (65536 - len(code))
    memory[100] = 23
    cpu = AxePU(memory)
    x16vm._run(cpu)
    output = cpu.data['a1']
    expected = 23
    assert expected == output, output


def test3():
    asm = """
    set a1 1
    set a2 2
    add a1 a2 a1
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    output = cpu.data['a1']
    expected = 3
    assert expected == output, output


def test4():
    asm = """
    set a1 1
    set a2 2
    add a1 a2 a1
    save a1 @100
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    output = memory[100]
    expected = 3
    assert expected == output, output


def test_compare():
    asm = """
    set a1 1
    set a2 2
    add a1 a2 a1
    save a1 @100
    compare a1 a2
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    output = cpu.data['c1']
    # output = memory[100]
    expected = 2
    assert expected == output, output


def test_save_from_register():
    asm = """
    set a1 4
    set a2 100
    save_from_register a1 a2
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    output = memory[100]
    # output = memory[100]
    expected = 4
    assert expected == output, output


def test_save_from_register2():
    asm = """
    set2 a1 65535
    set2 a2 100
    save_from_register2 a1 a2
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    output = memory[100]
    print(output)
    print(memory[101])
    assert memory[100] == 255
    assert memory[101] == 255


def test_load_from_register():
    asm = """
    set a1 4
    set a2 100
    save_from_register a1 a2
    load_from_register2 a2 a3
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    # output = memory[100]
    output = cpu.data['a3']

    expected = 4
    assert expected == output, output


def test_load_from_register2():
    asm = """
    set2 a1 65535
    set2 a2 100
    save_from_register2 a1 a2
    load_from_register2 a2 a3
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    # output = memory[100]
    output = cpu.data['a3']
    expected = 65535
    assert expected == output, output


def test_subtract2():
    asm = """
    set2 a1 2000
    set2 a2 1000
    subtract2 a1 a2 a1
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    # output = memory[100]
    output = cpu.data['a1']
    expected = 1000
    assert expected == output, output


def test_add2():
    asm = """
    set2 a1 2000
    set2 a2 1000
    add2 a1 a2 a1
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    # output = memory[100]
    output = cpu.data['a1']
    expected = 3000
    assert expected == output, output


def test_call_and_return():
    asm = """
    jump @1024
    .memory 1024
    set2 f1 3

    ; 我们要在接下来的的内存存放函数定义，所以直接跳转到 @function_end 避免执行函数
    jump @function_end

    ; a1, a2 用来存参数
    @function_multiply
    ; 局部变量空间
    ;
    set2 a3 8                  ; f1 += 8 对应 .return 8
    add2 f1 a3 f1               ;

    set2 a3 2                   ; 保存「变量 1」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a3 4                   ; 保存「变量 2」
    subtract2 f1 a3 a3          ;
    save_from_register2 a2 a3   ;

    set2 a1 1                   ; 用于 while 判断
    set2 a3 6                   ; 保存「变量 3」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 0                   ; 作为累加的 result
    set2 a3 8                   ; 保存「变量 4」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    @while_start
    ; 判断循环条件
    ;
    set2 a3 4                   ; 读取「变量 2」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    set2 a3 6                   ; 读取「变量 3」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a2   ;

    compare a1 a2
    jump_if_less @while_end

    ;「变量 3」 += 1
    ;
    set2 a3 6                   ; 读取「变量 3」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    set2 a3 1
    add a1 a3 a1

    set2 a3 6                   ; 保存「变量 3」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    ;「变量 4」 += 「变量 1」
    ;
    set2 a3 8                   ; 读取「变量 4」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    set2 a3 2                   ; 读取「变量 1」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a2   ;

    add2 a1 a2 a1

    set2 a3 8                   ; 保存「变量 4」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    jump @while_start
    @while_end

    ; 「变量 4」作为函数返回值，放入 a1
    ;
    set2 a3 8                   ; 读取「变量 4」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    .return 8


    ; 所有函数定义结束的标记（但我们这个例子中，只有一个函数定义）
    @function_end

    ; 调用函数
    set2 a1 300
    set2 a2 10

    .call @function_multiply


    save2 a1 @65530 ; 用于校验测试结果

    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    # output = memory[100]
    output = cpu.data['a1']
    expected = 3000
    assert expected == output, output


def test_factorial_a16():

    func_asm = """

    jump @1024
    .memory 1024
    set2 f1 3
    jump @function_end

    ; a1, a2 用来存参数
    @multiply
    ; 局部变量空间
    ;
    set2 a3 8                ; f1 += 8 对应 .return 8
    add2 f1 a3 f1               ;

    set2 a3 2                   ; 保存「变量 1」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a3 4                   ; 保存「变量 2」
    subtract2 f1 a3 a3          ;
    save_from_register2 a2 a3   ;

    set2 a1 1                   ; 用于 while 判断
    set2 a3 6                   ; 保存「变量 3」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 0                   ; 作为累加的 result
    set2 a3 8                   ; 保存「变量 4」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    @while_start
    ; 判断循环条件
    ;
    set2 a3 4                   ; 读取「变量 2」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    set2 a3 6                   ; 读取「变量 3」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a2   ;

    compare a1 a2
    jump_if_less @while_end

    ;「变量 3」 += 1
    ;
    set2 a3 6                   ; 读取「变量 3」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    set2 a3 1
    add2 a1 a3 a1

    set2 a3 6                   ; 保存「变量 3」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    ;「变量 4」 += 「变量 1」
    ;
    set2 a3 8                   ; 读取「变量 4」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    set2 a3 2                   ; 读取「变量 1」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a2   ;

    add2 a1 a2 a1

    set2 a3 8                   ; 保存「变量 4」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    jump @while_start
    @while_end

    ; 「变量 4」作为函数返回值，放入 a1
    ;
    set2 a3 8                   ; 读取「变量 4」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    .return 8


    @factorial

    set2 a3 4
    add2 f1 a3 f1 ;申请了4个内存

    set2 a3 2                   ; 保存「变量 1」
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a2 2

    set2 a3 4                   ; 保存「变量 2」
    subtract2 f1 a3 a3          ;
    save_from_register2 a2 a3   ;


    set2 a3 2                   ; 读取「变量 1」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    set2 a3 4                   ; 读取「变量 2」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a2   ;


    compare a1 a2
    jump_if_less @label1


    set2 a3 1                   ; a1 = a1 -1
    subtract2 a1 a3 a1          ;

    .call @factorial

    set2 a3 0
    add2 a3 a1 a2

    set2 a3 2                   ; 读取「变量 1」
    subtract2 f1 a3 a3          ;
    load_from_register2 a3 a1   ;

    .call @multiply

    @label1
    .return 4
    @function_end


    ;set a1 3
    ;.call @factorial

    ;halt
    """

    AxePU = x16vm.AxePU
    call_asm = """
    ; 调用函数
    set2 a1 5
    .call @factorial

    ; 校验测试结果
    save2 a1 @65530
    halt
    """
    asm = func_asm + call_asm
    memory = x16asm.machine_code(asm)
    cpu = AxePU(memory)
    x16vm._run(cpu)
    assert memory[65530] == 24 * 5


def test_shift_right():

    asm = """
    set a1 20
    shift_right a1
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    # output = memory[100]
    output = cpu.data['a1']
    expected = 10
    assert expected == output, output


def test_and():
    asm = """
    set a1 15
    set a2 1
    and a1 a2 a3
    halt
    """
    AxePU = x16vm.AxePU
    # case = cases[2]
    memory = x16asm.machine_code(asm)
    # memory = code
    cpu = AxePU(memory)
    x16vm._run(cpu)
    # output = memory[100]
    output = cpu.data['a3']
    expected = 1
    assert expected == output, output


def test_draw_point():

    with open('hello.a16') as f:
        func_asm = f.read()
    asm = """
    set2 a3 4
    add2 f1 a3 f1

    set2 a1 3
    set2 a3 4                   ; 保存「变量 1」x
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set a1 2
    set2 a3 2                  ; 保存「变量 2」y
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    .call @function_draw_point
    set2 a3 4
    subtract2 f1 a3 a3

    halt

    .memory 64512
    .data
    92 214 116 0 238 16 238 0 132 254 128 0 254 146 242 0
    """
    asm = func_asm + asm
    AxePU = x16vm.AxePU
    memory = x16asm.machine_code(asm)
    cpu = AxePU(memory)
    x16vm._run(cpu)
    output = memory[65091]
    expected = 195
    canvas = x16vm.Canvas(20)
    canvas.draw(memory[65024:])
    assert expected == output, output


def test_draw_column():

    with open('hello.a16') as f:
        func_asm = f.read()
    asm = """
    set2 a3 6
    add2 f1 a3 f1
    set2 a1 16
    set2 a3 6                  ; 保存「变量 1」column
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 4
    set2 a3 4                   ; 保存「变量 2」x
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 0
    set2 a3 2                  ; 保存「变量 3」y
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;
    .call @function_draw_column
    set2 a3 6
    subtract2 f1 a3 a3

    halt

    .memory 64512
    .data
    92 214 116 0 238 16 238 0 132 254 128 0 254 146 242 0
    """
    asm = func_asm + asm
    AxePU = x16vm.AxePU
    memory = x16asm.machine_code(asm)
    cpu = AxePU(memory)
    x16vm._run(cpu)
    output1 = memory[65089]
    output2 = memory[65153]
    expected = 195
    canvas = x16vm.Canvas(20)
    canvas.draw(memory[65024:])
    # assert expected == output1, output1
    # assert expected == output2, output2


def test_draw_char():

    with open('hello.a16') as f:
        func_asm = f.read()
    asm = """
    ; 0
    set2 a3 6
    add2 f1 a3 f1
    set2 a1 0
    set2 a3 6                  ; 保存「变量 code
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 0
    set2 a3 4                   ; 保存「变量 2」x
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 0
    set2 a3 2                  ; 保存「变量 3」y
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;
    
    .call @function_draw_char
    set2 a3 6
    subtract2 f1 a3 a3

    ; 1
    set2 a3 6
    add2 f1 a3 f1
    set2 a1 1
    set2 a3 6                  ; 保存「变量 code
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 4
    set2 a3 4                   ; 保存「变量 2」x
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 0
    set2 a3 2                  ; 保存「变量 3」y
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;
    
    .call @function_draw_char
    set2 a3 6
    subtract2 f1 a3 a3

    ; 2
    set2 a3 2
    add2 f1 a3 f1
    set2 a1 2
    set2 a3 6                  ; 保存「变量 code
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 8
    set2 a3 4                   ; 保存「变量 2」x
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 0
    set2 a3 2                  ; 保存「变量 3」y
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;
    
    .call @function_draw_char
    set2 a3 6
    subtract2 f1 a3 a3

    ;3
    set2 a3 6
    add2 f1 a3 f1
    set2 a1 3
    set2 a3 6                  ; 保存「变量 code
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 12
    set2 a3 4                   ; 保存「变量 2」x
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;

    set2 a1 0
    set2 a3 2                  ; 保存「变量 3」y
    subtract2 f1 a3 a3          ;
    save_from_register2 a1 a3   ;
    
    .call @function_draw_char
    set2 a3 6
    subtract2 f1 a3 a3

    halt

    .memory 64512
    .data
    92 214 116 0 238 16 238 0 132 254 128 0 254 146 242 0
    """
    asm = func_asm + asm
    # AxePU = x16vm.AxePU
    # cpu = AxePU(memory)
    # x16vm._run(cpu)
    memory = x16asm.machine_code(asm)
    x16vm.run(memory)
    canvas = x16vm.Canvas(20)
    canvas.draw(memory[65024:])
