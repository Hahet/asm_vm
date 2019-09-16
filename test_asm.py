# coding=UTF-8

# import x16vm
import x16asm

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
    ),
    (
        """
        jump @10
        .memory 10
        set a1 2
        """,
        [6, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 2]
    ),
]


def test_set():
    asm = """
    set a1 1
    halt
    """
    input = asm
    b = [0, 16, 1, 255]

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_load():
    case = cases[1]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_add():
    case = cases[2]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_save():
    case = cases[3]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_compare():
    case = cases[4]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_jump_if_less():
    case = cases[5]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_jump():
    case = cases[6]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_save_from_register():
    case = cases[7]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_halt():
    case = cases[8]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_set2():
    case = cases[9]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_load2():
    case = cases[10]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_add2():
    case = cases[11]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_save2():
    case = cases[12]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_subtract2():
    case = cases[13]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_load_from_register():
    case = cases[14]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_load_from_register2():
    case = cases[15]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_save_from_register2():
    case = cases[16]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_jump_from_register():
    case = cases[17]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_shift_right():

    input = """
    set a1 20
    shift_right a1
    """
    b = [
        0, 16, 20,
        17, 16
    ]

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_and():

    input = """
    set a1 15
    # bbb
    set a2 1
    and a1 a2 a3
    # aaa
    """
    b = [
        0, 16, 15,
        0, 32, 1,
        19, 16, 32, 48
    ]

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_labels():
    case = cases[18]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_comments():
    case = cases[19]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_memory():
    case = cases[20]
    a, b = case
    input = a

    expected = b + [0] * (65536 - len(b))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_dot_data():
    input = """
    set a1 2
    .data
    12 23 43 2
    halt
    """
    code = [
        0, 16, 2,
        12, 23, 43, 2,
        255
    ]
    expected = code + [0] * (65536 - len(code))
    result = x16asm.machine_code(input)
    assert expected == result, result


def test_function():
    asm = """
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

    expected = [
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

    result = x16asm.machine_code(asm)
    expected = expected + [0] * (65536 - len(expected))
    assert expected == result, result


def test_call():
    asm = """
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
    ; set2 a3 14 ;1097
    ; add2 pa a3 a3
    ; save_from_register2 a3 f1 ; 3byte

    ; set2 a3 2 ; 4byte
    ; add2 f1 a3 f1 ; 4byte

    ; jump @function_multiply ; 3byte
    .call @function_multiply
    halt ;1115
    """

    expected = [
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

    result = x16asm.machine_code(asm)
    expected = expected + [0] * (65536 - len(expected))
    assert expected == result, result


def test_return():
    asm = """
        set a1 2
        .return 16
        halt
    """
    return_asm = """
        set a1 2
        set2 a3 18
        subtract2 f1 a3 f1
        load_from_register2 f1 a2
        jump_from_register a2
        halt
    """
    expected = x16asm.machine_code(return_asm)
    output = x16asm.machine_code(asm)
    assert expected == output

# def test1():
#     # case = cases[0]
#     # a, b = case
#     for (a, b) in cases:
#         input = a
#         expected = b + [0] * (65536 - len(b))
#         result = x16asm.machine_code(input)
#         assert expected == result, result
