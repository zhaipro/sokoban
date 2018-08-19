# -*- coding: utf-8 -*-
# @Time    : 2017/8/10 上午9:42
# @Author  : Qi MO
# @File    : BFS.py
# @Software: PyCharm Community Edition

level_file_path = '../数据/level_file.txt'

class GameShortest:
    def __init__(self,line, col=10):
        """
        给一个图，长度为100的字符串表示。
        0空地 1墙 2箱子起始位置 3箱子终点位置 4人的起始位置
        :param line: 地图，用字符串表示。如代码最后的每一行表示每一关的地图。
        :param col: 地图的长宽，由于设定为10*10，默认为10
        """

        self.line = line
        # sta和en 表示开始的状态，结束的状态
        # sta只有2,4,0 2表示箱子开始位置,4表示人的位置,0表示其他。
        # en只有1,3,0 1表示墙,3表示箱子结束位置,0表示其他。
        # 现在只需要把sta状态中的2位置移动到en的3的位置即满足条件
        self.sta = ''
        self.en = ''
        self.col = col
        # px, py表示4的位置
        self.px,self.py = -1,-1
        # paths记录最短路径（可能有多条）
        self.paths = []
        # len记录最短路径长度 如
        self.len = -1

        self.pre()
        self.BFS()
        print(self.paths)

    def pre(self):
        """
        1.获得sta开始状态和en结束状态
        2.获得人的起始位置px,py
        代码最后的第一关的地图可视化为
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
        :return:
        """
        mp = []
        for pos in range(0, 100, 10):
            mp.append(self.line[pos:pos + 10])
        # print(self.line)
        # for x in mp:
        #     print(x)

        for pos, enum in enumerate(self.line):
            cx, cy = pos // 10, pos % 10
            if enum == '4':
                self.px, self.py = cx, cy
        # 现在只需要把sta开始的状态中的2位置移动到en的3的位置即满足条件
        staDic = {'0': '0', '1': '0', '2': '2', '3': '0', '4': '4'}
        enDic = {'0': '0', '1': '1', '2': '0', '3': '3', '4': '0'}
        for x in self.line:
            self.sta += staDic[x]
            self.en += enDic[x]
        # print(self.sta)
        # print(self.en)

    def is_ok(self,sta):
        """
        sta状态中的2位置移动到en的3的位置。
        :param sta:
        :return:
        """
        for s,e in zip(sta,self.en):
            if e == '3' and s != '2':
                return False
        return True

    def BFS(self):
        """
        BFS获得最短路径保存到paths中
        :return:
        """
        # 4个方向，小写代表只是人移动，大写表示人推着箱子一起移动
        dirs = [[-1,0,'u','U'],[1,0,'d','D'],[0,1,'r','R'],[0,-1,'l','L']]
        # 把开始的状态进入队列(list模拟)，状态包括字符串表示的当前状态、当前的路径、当前人的位置
        states = [[self.sta,'',self.px,self.py]]
        # 访问数组(dict模拟)，访问过的状态（字符串）不再访问
        visi = {}
        visi[self.sta] = 1

        s_len = 1000
        while len(states)>0:
            sta, path, px, py = states[0]
            # 4状态的位置
            ppos = px*self.col + py
            states = states[1:]
            if len(path)>s_len:
                break
            # 保存最短路径到paths中
            if self.is_ok(sta):
                if self.len == -1 or len(path) == self.len:
                    self.paths.append(path)
                    self.len = len(path)
                continue

            for dir in dirs:
                cx, cy = px + dir[0], py + dir[1]
                # 4挨着的状态的位置
                pos = cx*self.col+cy
                nx, ny = px + 2*dir[0], py + 2*dir[1]
                # 4挨着挨着的状态的位置
                npos = nx*self.col+ny
                if not (nx>=0 and nx<self.col and ny>=0 and ny<self.col):
                    continue
                # python中字符串不可更改，于是把字符串变成list更改状态后再转换为字符串
                if sta[pos] == '2' and sta[npos] == '0' and self.en[npos] != '1':
                # 人和箱子一起推动，sta中连着的状态为4 2 0，en中第三个不能为1。推完之后sta变为0 4 2
                    digits = [int(x) for x in sta]
                    digits[ppos],digits[pos],digits[npos] = 0,4,2
                    new_sta = ''.join(str(x) for x in digits)
                    if new_sta not in visi:
                        visi[new_sta] = 1
                        states.append([new_sta, path+dir[3], cx, cy])
                elif sta[pos] == '0' and self.en[pos] !='1':
                # 人动箱子不动，sta中连着的状态为4 0，en中第二个不能为1。
                    digits = [int(x) for x in sta]
                    digits[ppos], digits[pos]  = 0, 4
                    new_sta = ''.join(str(x) for x in digits)
                    if new_sta not in visi:
                        visi[new_sta] = 1
                        states.append([new_sta, path + dir[2], cx, cy])

if __name__ == '__main__':
    f = open(level_file_path, encoding='utf-8')
    cnt = 0
    while(1):
        line = f.readline()
        line = line.strip('\n')
        if len(line)==0 :
            break
        gs = GameShortest(line)

"""
level_file.txt中内容:
1111111111111111111111100011111110221111111420111111111001111111300111111330011111111111111111111111
1111111111104000000110000200111001101011100100101110010010111001011001110030000111111111111111111111
1111111111111111111111111111111110311111140020001110230020111111311111111111111111111111111111111111
1111111111111111111111100011111110221111111013311111102301111110040111111111111111111111111111111111
1111111111111111111111111111111100000111112111001113030020111400100011111111111111111111111111111111
1111111111111111111111111111111110011111100000011111001220111140300311111111111111111111111111111111
1111111111110040001110000000111001110011110011001111020130111100002011111311111111111111111111111111
1111111111111111111111111111111100111111100320001110131210111000000411111111111111111111111111111111
1111111111111111111111111111111100000111100111011110002020111000133411111111111111111111111111111111
1111111111111111111111100111111110004111111101011111312100111132001011113000201111111111111111111111
1111111111111111111111000001111131103111110402011111001201111100100111111111111111111111111111111111
1111111111111111111111100001111113112011110234001111001000111100001111111111111111111111111111111111
1111111111111111111111111001111110204111111020011111300101111130000111111111111111111111111111111111
1111111111111111111111143001111100000111110010211111001203111111101011111110001111111111111111111111
1111111111111111111111111111111100001111110202111111033420111111130011111111111111111111111111111111
1111111111111111111111110001111100230111114032301111110120111111000111111111111111111111111111111111
1111111111111111111111110031111102010111110020011111031401111100001111111111111111111111111111111111
1111111111111111111111111104111113110011110330201111021200111100001111111111111111111111111111111111
1111111111111111111111000111111100330111110011211111100100111112000411111001111111111111111111111111
1111111111111111111111100001111103032111110024001111111010111111100011111111111111111111111111111111
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
"""
