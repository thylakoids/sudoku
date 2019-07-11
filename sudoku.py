import unittest

import numpy as np


class sudoPoint():
    """point in a sudoku
    Possible state of the point in a sudoku.
    """

    def __init__(self):
        self._avaliable = set(range(1, 10))

    @property
    def avaliable(self):
        if len(self._avaliable) == 1:
            return list(self._avaliable)[0]
        else:
            return 0

    @avaliable.setter
    def avaliable(self, num):
        print(num)
        if isinstance(num, int) and num>=0 and num<=9:
            if num == 0:
                return
            else:
                self._avaliable = set([num])
        else:
            raise(TypeError('num should in in the range of 0~9'))

    def exclude(self, exclusion):
        """exclude

        :param exclusion: int or array
        """
        if isinstance(exclusion, int):
            exclusion = [exclusion]
        self._avaliable = self._avaliable.difference(exclusion)


class sudoku():
    """sudoku"""
    """sudoku"""

    def __init__(self):
        # using 9*9 numpy array to represent sudoku data, 0 means empty square.
        #  self._sudo = np.empty([9, 9])
        #  self._sudo_candidate = np.tile(range(1, 10), 81).reshape([9, 9, 9])
        self._sudo_candidate2 = np.array([sudoPoint()]*81).reshape([9, 9])

    @property
    def sudo(self):
        sudo = np.empty([9, 9])
        for i in range(9):
            for j in range(9):
                print(self._sudo_candidate2[i, j])
                sudo[i, j] = self._sudo_candidate2[i, j].avaliable
        return sudo

    @sudo.setter
    def sudo(self, sudo):
        # require: 9*9 numpy array&int&>=0&<=9
        if isinstance(sudo, np.ndarray) and sudo.shape == (9, 9):
            if sudo.dtype.type in (int, np.int, np.int8, np.int16, np.int32,
                                   np.int64) and sudo.min() >= 0 and sudo.max() <= 9:
                for i in range(9):
                    for j in range(9):
                        self._sudo_candidate2[i, j].avaliable = sudo[i, j]
            else:
                raise(TypeError('Input data for sudo be int and in the range of 0~9'))
        else:
            raise(TypeError('Input data for sudo should be 9*9 np.ndarray'))

    def checkSolved(self):
        # 检查数独是否被正确解答了
        #
        # 思路：
        #  1. 是否有格子没有填完
        #  2. 依次检查每一行（*9）， 每一列（*9）， 每一个九宫格（*9）
        #     是否满足条件。

        if self.sudo.min() == 0:
            return False
        for i in range(9):
            # 行
            #  print(i)
            if len(np.unique(self.sudo[i, :])) != 9:
                print('hang')
                return False
            # 列
            if len(np.unique(self.sudo[:, i])) != 9:
                print('lie')
                return False
            # 九方格
            a = int(np.floor(i/3))
            b = i % 3
            if len(np.unique(self.sudo[a*3:a*3+3, b*3:b*3+3])) != 9:
                print('block')
                return False
        return True

    def exclude(self):
        for i in range(9):
            # line
            exclusion = np.unique(self.sudo[i, :])
            for j in range(9):
                self._sudo_candidate2.exclude(exclusion)
            # column
            exclusion = np.unique(self.sudo[:, i])
            for j in range(9):
                self._sudo_candidate2.exclude(exclusion)
            # block
            a = int(np.floor(i/3))
            b = j % 3
            exclusion = np.unique(self.sudo[a*3:a*3+3, b*3:b*3+3])


class testSuduku(unittest.TestCase):
    """testSuduku"""
    """testSuduku"""
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

    def test_exclude(self):
        pass

if __name__ == '__main__':
    unittest.main()
    #  x = sudoku()
    #  print(x._sudo_candidate2)
