#coding: utf-8
import sys
import numpy as np
import numpy.linalg as la
import sl2z
import division as divi

class Generate:
    # Constructor
    def __init__(self):
        # target
        self.target = np.eye(2)
        # result
        self.result = np.eye(2)
        # Define Seed Matrix
        self.SIGMA = np.array([[1, 1], [0, 1]])
        self.OMEGA = np.array([[0, 1], [-1, 0]])
        # Show Calc Process(You can print the process)
        self.isshowprocess = False
        # Seed Matrix's Exponent
        self.exp_seed_matrix = []
        self.exp_i_seed_matrix = []

    # Method

    # Getter
    def get_target(self):
        return self.target

    # FIFO
    def get_exp_seed_matrix(self):
        return self.exp_seed_matrix

    def get_exp_i_seed_matrix(self):
        return self.exp_i_seed_matrix

    def get_result(self):
        return self.result

    # Setter
    def set_target(self, target):
        if sl2z.judge_sl2Z(target):
            self.target = target

    def set_isShowProcess(self, isshowprocess):
        self.isshowprocess = bool(isshowprocess)

    def set_exp_seed_matrix(self, seed_type, exp):
        self.exp_seed_matrix.append({'type': seed_type, 'exp': exp})
        self.exp_i_seed_matrix.append({'type': seed_type, 'exp': -1 * exp})

    # Search
    def proof(self):
        if self.target[0, 0] == 0:
            self.result = self.OMEGA.dot(self.target)
            # append Exp val

        elif self.target[1, 0] == 0:
            self.result = self.target
        else:
            self.result = self.search_loop()

    # loop algorithm
    def search_loop(self):
        target_calc = self.target

        # Show Calc Process
        if self.isshowprocess:
            print(target_calc)

        while True:
            target_calc = self.search_algorithm(target_calc)

            # Show Calc Process
            if self.isshowprocess:
                print(target_calc)

            if np.array_equal(self.SIGMA.dot(la.matrix_power(self.OMEGA, 2)), target_calc):
                target_calc = la.matrix_power(self.SIGMA, -1).dot(target_calc)

                # Show Calc Process
                if self.isshowprocess:
                    print(target_calc)

                self.set_exp_seed_matrix('sigma', 1)
                # -E
                self.set_exp_seed_matrix('omega', -2)
                return target_calc

            elif np.array_equal(self.SIGMA, target_calc):
                self.set_exp_seed_matrix('sigma', 1)
                # Sort reverse
                self.exp_seed_matrix.reverse()
                return target_calc

    # if Part a * Part c != 0
    def search_algorithm(self, target_calc):
        # if |Part a| < |Part c|
        if np.fabs(target_calc[(0, 0)]) < np.fabs(target_calc[(1, 0)]):
            # ω・target_calc
            target_calc = self.OMEGA.dot(target_calc)
            # append Exp val
            self.set_exp_seed_matrix('omega', 1)

        # Part a // Part c, Part a % Part c
        division = divi.euclidean(target_calc[0, 0], target_calc[1, 0])

        # ω・σ^(-quotient)・target_calc
        target_calc = self.OMEGA.dot(la.matrix_power(self.SIGMA, -1 * division["quotient"]).dot(target_calc))
        # append Exp val
        self.set_exp_seed_matrix('sigma', -1 * division["quotient"])
        self.set_exp_seed_matrix('omega', 1)

        return target_calc
