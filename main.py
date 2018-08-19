# -*- coding: utf-8 -*-
# @Time    : 2017/8/10 上午9:42
# @Author  : Qi MO
# @File    : BFS.py
# @Software: PyCharm Community Edition

level_file_path = 'level_file.txt'


class GameShortest:
    def __init__(self, line, col=10):
        '''
        给一个图，长度为100的字符串表示。
        0空地 1墙 2箱子起始位置 3箱子终点位置 4人起始位置
        5箱子起始就在终点位置 6人起始就在终点位置
        :param line: 地图，用字符串表示。如 level_file.txt 中的每一行表示每一关的地图。
        :param col: 地图的长宽，由于设定为10*10，默认为10
        '''

        self.line = line
        # start和end 表示开始的状态，结束的状态
        # start只有2,4,0 2表示箱子开始位置,4表示人的位置,0表示其他。
        # end只有1,3,0 1表示墙,3表示箱子结束位置,0表示其他。
        # 现在只需要把start状态中的2位置移动到end的3的位置即满足条件
        self.start = ''
        self.end = ''
        self.col = col
        # px, py表示4(人)的位置
        self.px, self.py = -1, -1
        # paths记录最短路径（可能有多条）
        self.paths = []
        # len记录最短路径长度
        self.len = -1

        self.pre()
        self.BFS()
        print(self.paths)

    def pre(self):
        '''
        1.获得start开始状态和end结束状态
        2.获得人的起始位置px,py
        第一关的地图可视化为
        1111111111
        1111111111
        1110001111
        1110221111
        1114201111
        1111100111
        1111300111
        1113300111
        1111111111
        1111111111
        '''
        # 现在只需要把start状态中的2位置移动到end状态中的3位置即满足条件
        start_dict = {'0': '0', '1': '0', '2': '2', '3': '0', '4': '4', '5': '2', '6': '4'}
        end_dict = {'0': '0', '1': '1', '2': '0', '3': '3', '4': '0', '5': '3', '6': '3'}
        for x in self.line:
            self.start += start_dict[x]
            self.end += end_dict[x]
        for pos, enum in enumerate(self.start):
            if enum == '4':
                self.px, self.py = pos // self.col, pos % self.col

    def is_ok(self, start):
        '''
        start状态中的2(盒子)位置移动到end的3(终点)的位置。
        :param start:
        '''
        for s, e in zip(start, self.end):
            if e == '3' and s != '2':
                return False
        return True

    def BFS(self):
        '''
        BFS获得最短路径保存到paths中
        '''
        # 4个方向，小写代表只是人移动，大写表示人推着箱子一起移动
        dirs = [[-1, 0, 'u', 'U'], [1, 0, 'd', 'D'], [0, 1, 'r', 'R'], [0, -1, 'l', 'L']]
        # 把开始的状态进入队列(list模拟)，状态包括字符串表示的当前状态、当前的路径、当前人的位置
        states = [[self.start, '', self.px, self.py]]
        # 访问集合，访问过的状态(字符串)不再访问
        visi = set()
        visi.add(self.start)

        s_len = 1000
        while states:
            start, path, px, py = states.pop(0)
            if len(path) > s_len:
                break
            # 保存最短路径到paths中
            if self.is_ok(start):
                if self.len == -1 or len(path) == self.len:
                    self.paths.append(path)
                    self.len = len(path)
                continue
            # 4(人)状态的位置
            ppos = px * self.col + py

            for dir in dirs:
                cx, cy = px + dir[0], py + dir[1]
                # 4(人)挨着的状态的位置
                pos = cx * self.col + cy
                nx, ny = px + 2 * dir[0], py + 2 * dir[1]
                # 4挨着挨着的状态的位置
                npos = nx * self.col + ny
                if not (0 <= nx < self.col and 0 <= ny < self.col):
                    continue
                if start[pos] == '2' and start[npos] == '0' and self.end[npos] != '1':
                    # 人和箱子一起推动，start中连着的状态为4 2 0，end中第三个不能为1。推完之后start变为0 4 2
                    # python中字符串不可更改，于是把字符串变成list更改状态后再转换为字符串
                    digits = list(start)
                    digits[ppos], digits[pos], digits[npos] = '0', '4', '2'
                    new_start = ''.join(digits)
                    if new_start not in visi:
                        visi.add(new_start)
                        states.append([new_start, path + dir[3], cx, cy])
                elif start[pos] == '0' and self.end[pos] != '1':
                    # 人动箱子不动，start中连着的状态为4 0，end中第二个不能为1。
                    digits = list(start)
                    digits[ppos], digits[pos] = '0', '4'
                    new_start = ''.join(digits)
                    if new_start not in visi:
                        visi.add(new_start)
                        states.append([new_start, path + dir[2], cx, cy])


if __name__ == '__main__':
    f = open(level_file_path)
    for line in f:
        line = line.strip('\n')
        gs = GameShortest(line)

'''
每一关的最短路径:
['uurrDDDDuuuulldRurDDDrddLLrruLuuulldRurDDDrdL']
['drrRRurDDDDDrdLLL']
['rrdrUrrrdLLulDullldR']
['lluRRdrUllluuurrDDuulldRurD']
['urrrrdrruulullllDurrrrdrddllullLrrrdrruLLL']
['uurrrrDulllddrrRuulDrdL']
['drrdddrdLLLuLDlUUUluRRRRurDDD']
['uullLLddrrUdlllluuRurDrRddrruuLLL']
['lUlLLdlluururrrrDDrdLullldlluRRRRllluurrrrdD']
['ddrddLLulLdlUrrrdrruuluulldDuurrddrddllLLrruLL']
['luurrrdrdLLLrrrddlUruuulllldDrddlUUrrRdrU']
['ddlluluRuurrrDrddlluLrdrruLLddlluU']
['dddlluluuRDrruulDrdLLulDrDLurrrddlLL']
['drrdDrrddllUUUUruLdrDldR', 'drrdDrrddllUUUUrDldRuuuL']
['drruLLLuulldRurDurDD']
['urRdddrrUULLulldRururrD']
['uLrddlluluuRDrrruullDldRRdrUU']
['dddlUllllddrUUddrrUruLLrrruulDrdLL']
['llldlUUUluurDrrrDDrdLLLulUluRRlddrddlUUUluR']
['ulldRurDrrddllUUluurrDLLdrddrruuLrddlluU']
'''
