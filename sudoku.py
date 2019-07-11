import unittest
import numpy as np
import copy


def valid_type(type):
    if type in (int, np.int, np.int8, np.int16, np.int32, np.int64):
        return True
    else:
        return False


class sudoPoint():
    """point in a sudoku
    Possible state of the point in a sudoku.
    0 : not sure.
    -1: error.
    """

    def __init__(self, num=0):
        self._avaliable = set(range(1, 10))
        self.avaliable = num

    @property
    def avaliable(self):
        if len(self._avaliable) == 0:  # which will not occur here
            return -1
        if len(self._avaliable) == 1:
            return list(self._avaliable)[0]
        else:
            return 0

    @avaliable.setter
    def avaliable(self, num):
        if valid_type(type(num)) and num >= 0 and num <= 9:
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
        if self.avaliable == 0:
            if isinstance(exclusion, int):
                exclusion = [exclusion]
            self._avaliable = self._avaliable.difference(exclusion)


class sudoku():
    """sudoku"""

    def __init__(self):
        # using 9*9 numpy array to represent sudoku data, 0 means empty square.
        self.candidate = np.array([sudoPoint()] * 81).reshape([9, 9])

    @property
    def sudo(self):
        return self.getSudoFromCandidate(self.candidate)

    @sudo.setter
    def sudo(self, sudo):
        # require: 9*9 numpy array&int&>=0&<=9
        if isinstance(sudo, np.ndarray) and sudo.shape == (9, 9):
            if valid_type(sudo.dtype.type) and sudo.min() >= 0 and sudo.max() <= 9:
                for i in range(9):
                    for j in range(9):
                        self.candidate[i, j] = sudoPoint(sudo[i, j])
            else:
                raise(TypeError('Input data for sudo be int and in the range of 0~9'))
        else:
            raise(TypeError('Input data for sudo should be 9*9 np.ndarray'))

    @staticmethod
    def getSudoFromCandidate(candidate):
        sudo = np.empty([9, 9])
        for i in range(9):
            for j in range(9):
                sudo[i, j] = candidate[i, j].avaliable
        return sudo

    @staticmethod
    def _checkState(data):
        data_nonzero = data[np.nonzero(data)]
        unique, counts = np.unique(data_nonzero, return_counts=True)
        if len(counts) >= 1 and counts.max() >= 2:
            return -1
        elif len(unique) < 9:
            return 0
        else:
            return 1

    @classmethod
    def checkStateSudo(cls, sudo)->int:
        """check current state of sudoku
        solution:
        1. if has nonzero repeat number, return -1
        2. if no repeat and has 0, return 0
        3. if no repeat and no 0, return 1
        Returns:
            int: 1: solved
                 0: to be solved
                 -1:something went wrong
        """
        state = 1
        for i in range(9):
            data_line = sudo[i, :]
            data_column = sudo[:, i]
            a = int(np.floor(i / 3))
            b = i % 3
            data_block = sudo[a * 3:a * 3 + 3, b * 3:b * 3 + 3]
            for data in [data_line, data_column, data_block]:
                _state = cls._checkState(data)
                if _state == -1:
                    # print(data)
                    return _state
                elif _state == 0:
                    state = 0
        return state

    @classmethod
    def checkStateCandidate(cls, candidate):
        return cls.checkStateSudo(cls.getSudoFromCandidate(candidate))

    @classmethod
    def exclude(cls, candidate):
        sudo = cls.getSudoFromCandidate(candidate)
        for i in range(9):
            # line
            exclusion = np.unique(sudo[i, :])
            for j in range(9):
                candidate[i, j].exclude(exclusion)
            # column
            exclusion = np.unique(sudo[:, i])
            for j in range(9):
                candidate[j, i].exclude(exclusion)
            # block
            a = int(np.floor(i / 3))
            b = i % 3
            exclusion = np.unique(sudo[a * 3:a * 3 + 3, b * 3:b * 3 + 3])
            # print(exclusion)
            for l in range(a * 3, a * 3 + 3):
                for c in range(b * 3, b * 3 + 3):
                    candidate[l, c].exclude(exclusion)
        return candidate

    @classmethod
    def guess(cls, candidate):
        len_candidate = np.array([len(x._avaliable) for x in
                                  candidate.flatten()]).reshape([9, 9])
        l, c = np.where(len_candidate == len_candidate[len_candidate > 1].min())

        _avaliable1 = candidate[l[0], c[0]]._avaliable
        _avaliable2 = set([_avaliable1.pop()])

        candidate1 = copy.deepcopy(candidate)
        candidate1[l[0], c[0]]._avaliable = _avaliable1
        candidate2 = copy.deepcopy(candidate)
        candidate2[l[0], c[0]]._avaliable = _avaliable2

        return candidate1, candidate2

    @classmethod
    def solve(cls, candidate):
        """may have multi solution!! need improve

        Args:
            candidate (TYPE): Description

        Returns:
            TYPE: Description
        """
        candidate = cls.exclude(candidate)
        sudo = cls.getSudoFromCandidate(candidate)
        state = cls.checkStateSudo(sudo)
        if state == 1:
            return sudo
        elif state == -1:
            return -1
        else:
            candidate1, candidate2 = cls.guess(candidate)
            solution1 = cls.solve(candidate1)
            if isinstance(solution1, np.ndarray):
                return solution1
            else:
                solution2 = cls.solve(candidate2)
                if isinstance(solution2, np.ndarray):
                    return solution2
                else:
                    return -1


class testSuduku(unittest.TestCase):
    """testSuduku"""
    mysudo = sudoku()
    sudo_solved = np.array([[7, 3, 5, 6, 1, 4, 8, 9, 2],
                            [8, 4, 2, 9, 7, 3, 5, 6, 1],
                            [9, 6, 1, 2, 8, 5, 3, 7, 4],
                            [2, 8, 6, 3, 4, 9, 1, 5, 7],
                            [4, 1, 3, 8, 5, 7, 9, 2, 6],
                            [5, 7, 9, 1, 2, 6, 4, 3, 8],
                            [1, 5, 7, 4, 9, 2, 6, 8, 3],
                            [6, 9, 4, 7, 3, 8, 2, 1, 5],
                            [3, 2, 8, 5, 6, 1, 7, 4, 9]]).astype(int)
    sudo_tobesolved = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 3, 0, 8, 5],
                                [0, 0, 1, 0, 2, 0, 0, 0, 0],
                                [0, 0, 0, 5, 0, 7, 0, 0, 0],
                                [0, 0, 4, 0, 0, 0, 0, 0, 0],
                                [0, 9, 0, 0, 0, 0, 0, 0, 0],
                                [5, 0, 0, 0, 0, 0, 0, 7, 3],
                                [0, 0, 2, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 4, 0, 0, 0, 9]]).astype(int)
    sudo_error = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 3, 0, 8, 5],
                           [0, 0, 1, 0, 2, 0, 0, 0, 0],
                           [0, 0, 0, 5, 0, 7, 0, 0, 0],
                           [0, 0, 4, 0, 0, 0, 0, 0, 0],
                           [0, 9, 0, 0, 0, 0, 0, 0, 0],
                           [5, 0, 0, 0, 0, 0, 0, 7, 3],
                           [0, 0, 2, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 4, 0, 0, 0, 9]]).astype(int)

    def test_setter(self):
        self.mysudo.sudo = np.random.randint(1, 9, (9, 9)).astype(int)
        with self.assertRaises(TypeError):
            self.mysudo.sudo = np.random.randint(1, 9, (9, 9)).astype(float)

    def test_checkState(self):
        self.mysudo.sudo = self.sudo_solved
        self.assertEqual(self.mysudo.checkStateSudo(self.mysudo.sudo), 1)
        self.mysudo.sudo = self.sudo_tobesolved
        self.assertEqual(self.mysudo.checkStateSudo(self.mysudo.sudo), 0)
        self.mysudo.sudo = self.sudo_error
        self.assertEqual(self.mysudo.checkStateSudo(self.mysudo.sudo), -1)

    def test_exclude(self):
        self.mysudo.sudo = self.sudo_tobesolved
        self.mysudo.exclude(self.mysudo.candidate)
        self.assertEqual(self.mysudo.candidate[2, 7]._avaliable, set([3, 4, 6, 9]))

    def test_guess(self):
        self.mysudo.sudo = self.sudo_tobesolved
        self.mysudo.exclude(self.mysudo.candidate)
        self.mysudo.guess(self.mysudo.candidate)

    def test_solve(self):
        self.mysudo.sudo = self.sudo_tobesolved
        solution = self.mysudo.solve(self.mysudo.candidate)
        print(solution)


if __name__ == '__main__':
    unittest.main()
    #  print(x.candidate)
    # mysudo = sudoku()
    # mysudo.sudo = np.random.randint(1, 9, (9, 9)).astype(int)
