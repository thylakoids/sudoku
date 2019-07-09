import numpy as np

class sudoPoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.available = set(range(1, 10))

    def getValue():
        if len(self.available) == 1:
            return self.available[0]
        else:
            return 0


class sudoku():
    def __init__(self):
        # 用9*9 array代表数独，空的格子用0表示。
        self._sudo = np.empty([9, 9])

    @property
    def sudo(self):
        return self._sudo

    @sudo.setter
    def sudo(self, sudo):
        # require: 9*9 numpy array&int&>=0&<=9
        if isinstance(sudo, np.ndarray) and sudo.shape == (9, 9):
            if type(sudo[0, 0]) in (int, np.int, np.int8, np.int16, np.int32,
                                    np.int64) and sudo.min() >= 1 and sudo.max() <= 9:
                self._sudo = sudo
            else:
                raise(TypeError('Input data for sudo be int and in the range of 0~9'))
        else:
            raise(TypeError('Input data for sudo should be 9*9 np.ndarray'))

    def checkSolved(self):
        # 检查数独是否被正确解答了
        #
        # 思路：
        # 1. 是否有格子没有填完
        # 2. 依次检查每一行（*9）， 每一列（*9）， 每一个九宫格（*9）
        #    是否满足条件。
        if 0 in self._sudo:
            return False
        for i in range(9):
            # 行
            if len(np.unique(self._sudo[i, :])) != 9:
                return False
            # 列
            if len(np.unique(self._sudo[:, i])) != 9:
                return False
            # 九方格
            a = np.floor(i/3)
            b = i % 3 - 1
            if len(np.unique(self._sudo[a*3:a*3+3, b*3:b*3+3])) != 9:
                return False
        return True

    def exclusion(self):
        # 排除法， 输出每个格子的待选项
        # 排除法分两步：
        # 1. 根据行， 列， 9方格规则生成候选项
        # 2. 如果在某9方格(行， 列)中，某两个空格候选项相同，且都为2个时候，那么这个9方
        #    格其他位置都能排除这两个数字。


if __name__ == '__main__':
    mysudo = sudoku()
    mysudo.sudo = np.random.randint(1, 9, (9, 9)).astype(int)
