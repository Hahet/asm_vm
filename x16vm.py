# coding=UTF-8

# from typing import List
import pygame


class Canvas(object):
    def __init__(self, scale):
        self.scale = scale

    def rgb(self, n):
        color_map = {
            '00': 0,
            '01': 100,
            '10': 175,
            '11': 255,
        }
        b = bin(n)
        s = b[2:].ljust(8, '0')
        r = color_map[s[0:2]]
        g = color_map[s[2:4]]
        b = color_map[s[4:6]]
        return (r, g, b)

    def point(self, n, m, scale):
        x = n % m
        y = int(n / m)
        return (x * scale, y * scale)

    def draw(self, array):
        scale = self.scale
        width, height = 32, 16
        screen = pygame.display.set_mode((width * scale, height * scale))
        clock = pygame.time.Clock()
        running = True
        fps = 30

        while running:
            for i, a in enumerate(array):
                color = self.rgb(a)
                position = self.point(i, 32, scale)
                # screen.set_at(position, color)
                rect_list = [position[0], position[1], scale, scale]
                pygame.draw.rect(screen, color, rect_list, 0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.image.save(screen, 'screen.bmp')
                    running = False

            pygame.display.flip()
            clock.tick(fps)

        # break


def real_number(a, b=0):
    return a + 256 * b


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


class AxePU(object):

    def __init__(self, memory):
        self.data = {
            'pa': 0,
            'a1': 0,
            'a2': 0,
            'a3': 0,
            'c1': 0,
            'f1': 0,
        }
        self.memory = memory
        # self.data = {
        #     'pa': 0,
        #     'a1': 0,
        #     'a2': 0,
        #     'a3': 0,
        #     'c1': 0,
        #     'f1': 0,
        # }
        self.registers = {
            0: 'pa',
            16: 'a1',
            32: 'a2',
            48: 'a3',
            64: 'c1',
            80: 'f1',
        }
        self.instructions = {
            0: {
                'name': 'set',
                'step': 3,
            },
            1: {
                'name': 'load',
                'step': 4,
            },

            2: {
                'name': 'add',
                'step': 4,
            },

            3: {
                'name': 'save',
                'step': 4,
            },
            4: {
                'name': 'compare',
                'step': 3,
            },

            5: {
                'name': 'jump_if_less',
                'step': 3
            },

            6: {
                'name': 'jump',
                'step': 3,
            },
            7: {
                'name': 'save_from_register',
                'step': 3
            },
            8: {
                'name': 'set2',
                'step': 4,
            },
            9: {
                'name': 'load2',
                'step': 4,
            },
            10: {
                'name': 'add2',
                'step': 4,
            },
            11: {
                'name': 'save2',
                'step': 4,
            },
            12: {
                'name': 'subtract2',
                'step': 4,
            },

            13:  {
                'name': 'load_from_register',
                'step': 3,
            },
            14: {
                'name': 'load_from_register2',
                'step': 3,
            },
            15: {
                'name': 'save_from_register2',
                'step': 3,
            },
            16: {
                'name': 'jump_from_register',
                'step': 2,
            },
            17: {
                'name': 'shift_right',
                'step': 2,
            },
            19: {
                'name': 'and',
                'step': 4,
            },

            255: {
                'name': 'halt',
                'step': 1,
            },
            235: {
                'name': 'debug',
                'step': 1,
            }

        }

    def debug(self):
        self.move_pa()
        # f1 = self.data['f1']
        # mf = self.memory[0:f1]
        # m1 = self.memory[64512:]
        # m2 = self.memory[65024:]
        # data = self.data
        # print(mf)
        # input()

    def set(self):
        # r 寄存器
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        m1 = memory[pa + 1]
        m2 = memory[pa + 2]
        r = self.registers[m1]
        self.data[r] = real_number(m2)

    def set2(self):
        # r 寄存器
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r = self.registers[memory[pa + 1]]
        self.data[r] = real_number(memory[pa + 2], memory[pa + 3])

    def load(self):
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r = self.registers[memory[pa + 3]]
        i = real_number(memory[pa + 1], memory[pa + 2])
        self.data[r] = memory[i]

    def load2(self):
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r = self.registers[memory[pa + 3]]
        i = real_number(memory[pa + 1], memory[pa + 2])
        self.data[r] = real_number(memory[i], memory[i+1])

    def add(self):
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        r2 = self.registers[memory[pa + 2]]
        r3 = self.registers[memory[pa + 3]]

        self.data[r3] = format_nummber(self.data[r1] + self.data[r2])[0]

        # add2 pa a3 a3，把pa指向下一条命令
        # if (r1 == 'pa'):
        #     self.data[r3] += 4

    def add2(self):
        # self.add()
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        r2 = self.registers[memory[pa + 2]]
        r3 = self.registers[memory[pa + 3]]
        self.data[r3] = self.data[r1] + self.data[r2]

    def save(self):
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r = self.registers[memory[pa + 1]]

        [a, b] = format_nummber(self.data[r])
        i = real_number(memory[pa + 2], memory[pa + 3])
        memory[i] = a
        memory[i + 1] = b

    def save2(self):
        self.save()

    def subtract2(self):
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        r2 = self.registers[memory[pa + 2]]
        r3 = self.registers[memory[pa + 3]]
        self.data[r3] = self.data[r1] - self.data[r2]

    def compare(self):
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        r2 = self.registers[memory[pa + 2]]
        if self.data[r1] == self.data[r2]:
            self.data['c1'] = 1
        if self.data[r1] < self.data[r2]:
            self.data['c1'] = 0
        if self.data[r1] > self.data[r2]:
            self.data['c1'] = 2

    def jump_if_less(self):

        # memory = self.memory
        # data = self.data
        # pa = self.data['pa']
        # #  跳转的内存位置
        # i = real_number(memory[pa + 1], memory[pa + 2])
        if self.data['c1'] == 0:
            self.jump()
        else:
            self.move_pa()

    def jump(self):
        memory = self.memory
        pa = self.data['pa']

        #  跳转的内存位置
        i = real_number(memory[pa + 1], memory[pa + 2])
        self.data['pa'] = i

    def save_from_register(self):
        self.save_from_register2()

    def save_from_register2(self):
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        r2 = self.registers[memory[pa + 2]]

        [a, b] = format_nummber(self.data[r1])
        i = self.data[r2]

        memory[i] = a
        memory[i + 1] = b

    def load_from_register(self):
        memory = self.memory
        data = self.data
        pa = self.data['pa']
        self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        r2 = self.registers[memory[pa + 2]]
        i = data[r1]
        data[r2] = memory[i]

    def load_from_register2(self):
        memory = self.memory
        data = self.data
        pa = self.data['pa']
        self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        r2 = self.registers[memory[pa + 2]]
        i = data[r1]
        data[r2] = real_number(memory[i], memory[i + 1])

    def jump_from_register(self):
        memory = self.memory
        data = self.data
        pa = self.data['pa']
        # self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        i = data[r1]
        self.data['pa'] = i

    def shift_right(self):
        memory = self.memory
        data = self.data
        pa = self.data['pa']
        self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        data[r1] = data[r1] >> 1

    def axe_and(self):
        memory = self.memory
        pa = self.data['pa']
        self.move_pa()
        r1 = self.registers[memory[pa + 1]]
        r2 = self.registers[memory[pa + 2]]
        r3 = self.registers[memory[pa + 3]]
        self.data[r3] = self.data[r1] & self.data[r2]

    def halt(self):
        self.move_pa()
        print('END', self.data['a1'])
        return 'halt'

    def move_pa(self):
        pa = self.data['pa']
        a = self.memory[pa]
        instructions = self.instructions
        instruction = instructions[a]
        # name = instruction['name']
        step = instruction['step']
        self.data['pa'] += step

    def pa(self):
        return self.data['pa']


def run(memory):
    cpu = AxePU(memory)
    mapper = {
        'set': cpu.set,
        'load': cpu.load,
        'add': cpu.add,
        'save': cpu.save,
        'compare': cpu.compare,
        'halt': cpu.halt,
        # 操作16位
        'set2': cpu.set2,
        'load2': cpu.load2,
        'add2': cpu.add2,
        'save2': cpu.save2,
        'subtract2': cpu.subtract2,

        'jump_if_less': cpu.jump_if_less,
        'jump': cpu.jump,
        'load_from_register': cpu.load_from_register,
        'save_from_register': cpu.save_from_register,
        'load_from_register2': cpu.load_from_register2,
        'save_from_register2': cpu.save_from_register2,
        'jump_from_register': cpu.jump_from_register,
        'shift_right': cpu.shift_right,
        'and': cpu.axe_and,
        'debug': cpu.debug,
    }
    # i = 0
    while cpu.pa() < len(memory):
        pa = cpu.pa()
        a = memory[pa]
        instructions = cpu.instructions
        instruction = instructions[a]
        name = instruction['name']

        if name == 'halt':
            return
        f = mapper[name]
        f()


def _run(cpu):
    # cpu = AxePU(memory)
    memory = cpu.memory
    mapper = {
        'set': cpu.set,
        'load': cpu.load,
        'add': cpu.add,
        'save': cpu.save,
        'compare': cpu.compare,
        'halt': cpu.halt,
        # 操作16位
        'set2': cpu.set2,
        'load2': cpu.load2,
        'add2': cpu.add2,
        'save2': cpu.save2,
        'subtract2': cpu.subtract2,

        'jump_if_less': cpu.jump_if_less,
        'jump': cpu.jump,
        'load_from_register': cpu.load_from_register,
        'save_from_register': cpu.save_from_register,
        'load_from_register2': cpu.load_from_register2,
        'save_from_register2': cpu.save_from_register2,
        'jump_from_register': cpu.jump_from_register,
        'shift_right': cpu.shift_right,
        'and': cpu.axe_and,
        'debug': cpu.debug,
    }
    # i = 0
    while cpu.pa() < len(memory):
        pa = cpu.pa()
        a = memory[pa]

        # f1 = cpu.data['f1']
        # mf = cpu.memory[0:f1]
        # m1 = cpu.memory[64512:]
        # m2 = cpu.memory[65024:]
        # ma = cpu.memory[pa:]
        # data = cpu.data

        instructions = cpu.instructions
        instruction = instructions[a]
        name = instruction['name']

        if name == 'halt':
            return
        f = mapper[name]
        f()
# test


def test():
    memory = [
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
    memory += [0] * (65536 - len(memory))
    run(memory)


if __name__ == '__main__':
    test()
