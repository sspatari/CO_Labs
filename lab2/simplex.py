from __future__ import division
from numpy import *
from pprint import pprint

class Tabel:

    def __init__(self, obj):
        self.obj = [1] + obj
        self.rows = []
        self.cons = []
        self.compare_symbol = [] #added
        self.solution_dict = {"x"+str(i+1):0 for i in range(len(obj))}
        self.max_result = None
        self.star_list = []
        set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    def add_constraint(self, expression, value, symbol):
        self.rows.append([0] + expression)
        self.cons.append(value)
        self.compare_symbol.append(symbol)

    def _pivot_column(self):
        if self._star_check():
            selected_row_index = self.star_list.index("*")
            return self.rows[selected_row_index][1:-1].tolist().index( #find pivot colomn
                max(self.rows[selected_row_index][1:-1])) + 1
        else:
            low = 0
            idx = 0
            for i in range(1, len(self.obj)-1):
                if self.obj[i] < low:
                    low = self.obj[i]
                    idx = i
            if idx == 0: return -1
            return idx

    def _pivot_row(self, col):
        rhs = [self.rows[i][-1] for i in range(len(self.rows))]
        lhs = [self.rows[i][col] for i in range(len(self.rows))]
        ratio = []
        for i in range(len(rhs)):
            if lhs[i] <= 0:
                ratio.append(99999999 * abs(max(rhs))) #creates big an artificial big number to be able to compare to
                continue
            ratio.append(rhs[i]/lhs[i])
        return argmin(ratio) #for sure need to modify for thw star case

    def display(self):
        print('\n', around(matrix([self.obj] + self.rows),3))

    def _pivot(self, row, col): #this method modifies the table based on the pivot
        e = self.rows[row][col] # e is the pivot
        self.rows[row] /= e
        for r in range(len(self.rows)):
            if r == row: continue
            self.rows[r] = self.rows[r] - self.rows[r][col]*self.rows[row]
        self.obj = self.obj - self.obj[col]*self.rows[row]

    def _check(self):
        if min(self.obj[1:-1]) >= 0: return 1
        return 0

    def _star_check(self):
        if "*" in self.star_list:
                return 1
        return 0

    def _eliminate_star(self):
        c = self._pivot_column()    #find pivot column
        r = self._pivot_row(c)      #find pivot row
        self._pivot(r,c)
        print('\npivot column: %s\npivot row: %s'%(c+1,r+2))
        self.display()
        self.star_list[r] = ""

    def _extract_solutions(self):
        for i in range(1,len(matrix(self.rows).tolist()[0])): #i represents matrix colomn
            counter1 = 0
            counter2 = 0
            for j in range(len(matrix(self.rows).tolist())):  #j represents matrix row
                if matrix(self.rows).tolist()[j][i] == 1:
                    counter1 += 1
                elif matrix(self.rows).tolist()[j][i] == 0:
                    counter2 += 1
            if counter1 == 1 and counter2 == len(matrix(self.rows).tolist())-1:
                if "x"+str(i) in self.solution_dict.keys():
                    for l in range(len(matrix(self.rows).tolist())):
                        if matrix(self.rows).tolist()[l][i] == 1:
                            self.solution_dict["x"+str(i)] = around(matrix(self.rows),3).tolist()[l][-1]
        self.max_result = self.obj[len(self.obj) - 1]

    def solve(self):
        # build full table
        for i in range(len(self.rows)):
            self.obj += [0]
            ident = [0 for r in range(len(self.rows))]
            if(self.compare_symbol[i] == "<="):
                ident[i] = 1
                self.star_list.append("")
            elif(self.compare_symbol[i] == ">="):
                ident[i] = -1
                self.star_list.append("*")
            self.rows[i] += ident + [self.cons[i]]
            self.rows[i] = array(self.rows[i], dtype=float)
        self.obj = array(self.obj + [0], dtype=float)

        # solve
        self.display()

        #the star simplex solver
        while self._star_check():
            print(self.star_list)
            c = self._pivot_column()    #find pivot column
            r = self._pivot_row(c)      #find pivot row
            self._pivot(r,c)
            print('\npivot column: %s\npivot row: %s'%(c+1,r+2))
            self.display()
            self.star_list[r] = ""

        #simple simplex
        while not self._check():
            c = self._pivot_column()    #find pivot column
            r = self._pivot_row(c)      #find pivot row
            self._pivot(r,c)
            print('\npivot column: %s\npivot row: %s'%(c+1,r+2))
            self.display()

        self._extract_solutions()

if __name__ == '__main__':

    """
    max z = 2x + 3y + 2z
    st
    2x + y + z <= 4
    x + 2y + z <= 7
    z          <= 5
    x,y,z >= 0
    """

    t = sm.Tabel([-2,-3,-2])
    t.add_constraint([2, 1, 1], 4, "<=")
    t.add_constraint([1, 2, 1], 7, "<=")
    t.add_constraint([0, 0, 1], 5, "<=")
    t.solve()
