from queue import Queue as Q
from collections import Counter


class Puzzle:
    def __init__(self, grid=None, count = 0):
        if grid is None:
            self.grid = [[0] * 9 for _ in range(9)]
        else:
            self.grid = [[v for v in row] for row in grid]
        self.count = count

    def __getitem__(self, i):
        return self.grid[i]

    def __len__(self):
        return 9

    def __iter__(self):
        return self.grid.__iter__()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "\n".join(" ".join(map(str, row)) for row in self.grid)

    def __hash__(self):
        return str(self).__hash__()

    def update_count(self):
        self.count = sum(map(lambda row: len([v for v in row if v != 0]), self.grid))

    def solved(self):
        return self.complete() and self.valid()

    def complete(self):
        return self.count == 81

    def valid(self):
        def bad(c):
            mc = c.most_common(2)
            if mc[0][0] != 0 and mc[0][1] != 1:
                return True
            if len(mc) > 1 and mc[1][1] != 1:
                return True
            return False
        for row in self.grid:
            c = Counter(row)
            if bad(c):
                return False
        for col in range(9):
            c = Counter([row[col] for row in self.grid])
            if bad(c):
                return False
        for x in range(3):
            for y in range(3):
                c = Counter()
                for xx in range(3):
                    for yy in range(3):
                        c.update([self.grid[x * 3 + xx][y * 3 + yy]])
                if bad(c):
                    return False
        return True


def solve(puzzle):
    if not puzzle.valid():
        print("original puzzle isn't valid")
        return
    puzzle.update_count()
    print(puzzle.count)
    solution_found = False
    seen = set()
    q = Q()
    q.put(puzzle)
    c = 0
    while not q.empty():
        curr = q.get(False)
        c += 1
        if c % 1000 == 0:
            print(c, curr.count)
        for x in range(9):
            for y in range(9):
                if curr[x][y] == 0:
                    for i in range(1, 10):
                        n = Puzzle(curr, curr.count+1)
                        n[x][y] = i
                        if str(n) in seen:
                            continue
                        seen.add(str(n))
                        if not n.valid():
                            continue
                        if n.complete():
                            print(n)
                            print()
                            solution_found = True
                        else:
                            q.put(n)
    print(c, "tries")
    if not solution_found:
        print("no solution found")

p = Puzzle(
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
    ]
)
p[0][0] = 0
p[1][1] = 0

p = Puzzle(
    [
        [0, 6, 2, 3, 0, 8, 4, 0, 0],
        [1, 8, 5, 0, 2, 0, 7, 0, 3],
        [0, 7, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 3, 9, 6],
        [0, 9, 0, 0, 0, 0, 1, 0, 7],
        [7, 0, 0, 0, 9, 6, 2, 8, 0],
        [5, 3, 1, 9, 0, 0, 6, 0, 0],
        [0, 4, 9, 0, 5, 0, 0, 0, 1],
        [0, 2, 0, 6, 0, 0, 0, 4, 0],
    ]
)

p = Puzzle(
    [
        [0, 5, 8, 0, 7, 0, 0, 0, 2],
        [0, 4, 0, 0, 6, 2, 0, 9, 8],
        [2, 9, 1, 0, 3, 0, 7, 0, 0],
        [0, 0, 6, 9, 0, 0, 4, 0, 7],
        [3, 2, 0, 6, 0, 0, 0, 1, 5],
        [0, 7, 0, 2, 5, 4, 6, 0, 3],
        [0, 0, 0, 8, 9, 1, 2, 0, 6],
        [0, 0, 0, 0, 2, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 8, 0, 1],
    ]
)
p = Puzzle(
    [
        [0, 5, 8, 4, 7, 0, 1, 3, 2],
        [0, 4, 3, 1, 6, 2, 5, 9, 8],
        [2, 9, 1, 5, 3, 8, 7, 6, 0],
        [5, 8, 6, 9, 0, 3, 4, 2, 7],
        [3, 2, 4, 6, 8, 7, 9, 1, 5],
        [0, 7, 9, 2, 5, 4, 6, 8, 3],
        [4, 3, 7, 8, 9, 1, 2, 0, 6],
        [0, 0, 0, 7, 2, 6, 3, 4, 9],
        [0, 0, 2, 3, 4, 0, 8, 0, 1],
    ]
)
solve(p)
