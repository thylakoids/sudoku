import unittest

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
        self._sudo = np.empty([9, 9])

    @property
    def sudo(self):
        return self._sudo

    @sudo.setter
    def sudo(self, sudo):
        # require: 9*9 numpy array&int&>=0&<=9
        if isinstance(sudo, np.ndarray) and sudo.shape == (9, 9):
            if sudo.dtype.type in (int, np.int, np.int8, np.int16, np.int32,
                                    np.int64) and sudo.min() >= 0 and sudo.max() <= 9:
                self._sudo = sudo
            else:
                raise(TypeError('Input data for sudo be int and in the range of 0~9'))
        else:
            raise(TypeError('Input data for sudo should be 9*9 np.ndarray'))

    def checkSolved(self):
        # 检查数独是否被正确解答了
        #
        # 思路：依次检查每一行（*9）， 每一列（*9）， 每一个九宫格（*9）
        # 是否满足条件。

        if self._sudo.min() == 0:
            return False
        for i in range(9):
            # 行
            #  print(i)
            if len(np.unique(self._sudo[i, :])) != 9:
                print('hang')
                return False
            # 列
            if len(np.unique(self._sudo[:, i])) != 9:
                print('lie')
                return False
            # 九方格
            a = int(np.floor(i/3))
            b = i % 3
            if len(np.unique(self._sudo[a*3:a*3+3, b*3:b*3+3])) != 9:
                print('fangge')
                return False
        return True


class testSuduku(unittest.TestCase):
    mysudo = sudoku()

    def test_setter(self):
        self.mysudo.sudo = np.random.randint(1, 9, (9, 9)).astype(int)
        with self.assertRaises(TypeError):
            self.mysudo.sudo = np.random.randint(1, 9, (9, 9)).astype(float)

    def test_checksolved(self):
        self.mysudo.sudo = np.array([[7, 3, 5, 6, 1, 4, 8, 9, 2],
                                     [8, 4, 2, 9, 7, 3, 5, 6, 1],
                                     [9, 6, 1, 2, 8, 5, 3, 7, 4],
                                     [2, 8, 6, 3, 4, 9, 1, 5, 7],
                                     [4, 1, 3, 8, 5, 7, 9, 2, 6],
                                     [5, 7, 9, 1, 2, 6, 4, 3, 8],
                                     [1, 5, 7, 4, 9, 2, 6, 8, 3],
                                     [6, 9, 4, 7, 3, 8, 2, 1, 5],
                                     [3, 2, 8, 5, 6, 1, 7, 4, 9]]).astype(int)
        self.assertTrue(self.mysudo.checkSolved())


if __name__ == '__main__':
    unittest.main()
