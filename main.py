# -*- coding: utf-8 -*-
# @Time    : 2017/8/10 上午9:42
# @Author  : Qi MO
# @File    : BFS.py
# @Software: PyCharm Community Edition


# 游戏关卡
class Levels:
    def __init__(self, fn='levels.txt'):
        self.fn = fn

    def __iter__(self):
        # 文件中的每一行表示每一关的地图
        for line in open(self.fn, encoding='utf-8'):
            # 非注释和空行
            if line[0] not in ('#', '\n'):
                # 地图，用字符串表示
                yield line.strip('\n')


class Game:
    def __init__(self, level, col=10):
        '''
        给一个图，长度为10n的字符串表示。
        0空地 1墙 2箱子 3终点 4人
        5箱子在终点 6人在终点
        :param level
        :param col: 地图的宽度，由于设定为10，默认为10
        '''
        self.level = level
        self.col = col
        # paths记录最短路径(可能有多条)
        self.paths = []
        # len记录最短路径长度
        self.len = -1

    def pre(self):
        '''
        获得人的起始位置px,py
        '''
        for pos, enum in enumerate(self.level):
            if enum in ('4', '6'):
                self.ppos = pos

    def is_ok(self, line):
        '''
        如果 line 状态中的已经没有2(箱子)，则说明箱子已经被推到终点。
        '''
        return '2' not in line

    def BFS(self):  # NOQA
        '''
        BFS获得最短路径保存到paths中
        '''
        # 4个方向，小写代表只是人移动，大写表示人推着箱子一起移动
        dirs = [[-self.col, 'u', 'U'], [self.col, 'd', 'D'], [1, 'r', 'R'], [-1, 'l', 'L']]
        # 把开始的状态进入队列(list模拟)，状态包括字符串表示的当前状态、当前的路径、当前人的位置
        states = [[self.level, '', self.ppos]]
        # 访问集合，访问过的状态(字符串)不再访问
        visi = set()
        visi.add(self.level)

        s_len = 1000
        while states:
            line, path, ppos = states.pop(0)
            if len(path) > s_len:
                break
            # 保存最短路径到paths中
            if self.is_ok(line):
                if self.len == -1 or len(path) == self.len:
                    self.paths.append(path)
                    self.len = len(path)
                continue

            for dir in dirs:
                # 4(人)挨着的状态的位置
                cpos = ppos + dir[0]
                # 4挨着挨着的状态的位置
                npos = cpos + dir[0]
                if line[cpos] in ('2', '5') and line[npos] in ('0', '3'):
                    # python中字符串不可更改，于是把字符串变成list更改状态后再转换为字符串
                    digits = list(line)
                    a = {'0': '2', '2': '4', '3': '5', '4': '0', '5': '6', '6': '3'}
                    digits[ppos] = a[digits[ppos]]
                    digits[cpos] = a[digits[cpos]]
                    digits[npos] = a[digits[npos]]
                    new_line = ''.join(digits)
                    if new_line not in visi:
                        visi.add(new_line)
                        states.append([new_line, path + dir[2], cpos])
                elif line[cpos] in ('0', '3'):
                    # 人动箱子不动，line中连着的状态为4 0。
                    a = {'0': '4', '3': '6', '4': '0', '6': '3'}
                    digits = list(line)
                    digits[ppos] = a[digits[ppos]]
                    digits[cpos] = a[digits[cpos]]
                    new_line = ''.join(digits)
                    if new_line not in visi:
                        visi.add(new_line)
                        states.append([new_line, path + dir[1], cpos])

    def gen_shortest_paths(self):
        self.pre()
        self.BFS()
        return self.paths


def main():
    levels = Levels()
    for level in levels:
        game = Game(level)
        yield game.gen_shortest_paths()


if __name__ == '__main__':
    for paths in main():
        print(paths)
