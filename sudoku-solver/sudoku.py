from multiprocessing import Pool
import time


class InvalidSudoku(Exception): pass


class SudokuPuzzle(object):

    def __init__(self, grid, empty_spaces=None):
        """
        grid: list, length 9 to represent grid
        empty_spaces: number of blanks in the grid
        """
        self.grid = grid
        if empty_spaces is None:
            empty_spaces = self.grid.count(0)
        self.empty_spaces = empty_spaces

    def get_moves(self, i):
        """
        For a given square, i, in the grid, find possible values
        """
        moves = [1] * 9  # Zero-indexed bit-map of possible values

        row_start = (i//9)*9
        col_start = i % 9
        block_start = (row_start // (3*9)) * (3*9) + (((col_start // 3)*3) % 9)

        for j in range(9):
            row_i = row_start + j
            col_i = col_start + (j*9)
            block_i = block_start + (j//3)*9 + (j%3)

            for square_i in (row_i, col_i, block_i):
                if self.grid[square_i] != 0:
                    moves[self.grid[square_i]-1] = 0 # -1 because of zero-index

        return [(k + 1) for k, value in enumerate(moves) if value == 1]

    def get_puzzles(self, i, moves):
        """
        Convert list of possible values for a square i into a list of
        SudokuPuzzle instances.
        """
        puzzles = []
        for move in moves:
            grid = [o for o in self.grid]
            grid[i] = move
            puzzles.append(SudokuPuzzle(grid, self.empty_spaces-1))
        return puzzles

    def get_children(self):
        """
        Pick the child puzzle with least possible moves.
        """
        moves, best_i = [], -1
        for i, value in enumerate(self.grid):
            if value != 0:
                continue

            new_moves = self.get_moves(i)

            # Shortcut if only 0 or 1 moves
            if len(new_moves) <= 1:
                return self.get_puzzles(i, new_moves)

            # Pick the square i with the least # of moves
            if len(moves) == 0 or len(new_moves) < len(moves):
                moves, best_i = new_moves, i

        return self.get_puzzles(best_i, moves)

    def solve(self):
        """
        Solve the puzzle, using a stack.
        """
        puzzle_stack = self.get_children()
        while puzzle_stack:
            puzzle = puzzle_stack.pop()
            for child_puzzle in puzzle.get_children():
                if child_puzzle.empty_spaces == 0:
                    return child_puzzle
                puzzle_stack.append(child_puzzle)

        raise InvalidSudoku()



def parse_puzzles(filename):
    puzzles = []
    with open(filename) as f:
        puzzles_raw = ''.join([line[:9] for line in f.readlines() if not 'Grid' in line])
        for i in range(0,len(puzzles_raw),81):
            puzzle = SudokuPuzzle([int(o) for o in puzzles_raw[i:(i+81)]])
            puzzles.append(puzzle)
    return puzzles


def main():
    t0 = time.time()
    puzzles = parse_puzzles('p096_sudoku.txt')

    pool = Pool(3)
    solutions = map(lambda o:o.solve(), puzzles)

    top_lefts = [solved.grid[0] * 100 + solved.grid[1] * 10 + solved.grid[2] * 1 for solved in solutions]
    print sum(top_lefts)
    
    t1 = time.time()
    print 'Took {0} secs'.format(t1-t0)

if __name__ == '__main__':
    main()