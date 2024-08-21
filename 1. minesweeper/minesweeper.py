import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = [[False] * width for _ in range(height)]

        # Add mines randomly
        while len(self.mines) < mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are within one row and column of a given cell,
        not including the cell itself.
        """
        count = 0
        for i, j in itertools.product(range(cell[0] - 1, cell[0] + 2), range(cell[1] - 1, cell[1] + 2)):
            if (i, j) == cell:
                continue
            if 0 <= i < self.height and 0 <= j < self.width:
                if self.board[i][j]:
                    count += 1
        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Adds a new sentence to the AI's knowledge base and performs
        inference to update knowledge base and discover new safe cells or mines.
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Find the unmarked neighbors
        unmarked_neighbors = self.get_unmarked_neighbors(cell)

        # Adjust count by removing known mines
        adjusted_count = count - sum(1 for neighbor in unmarked_neighbors if neighbor in self.mines)
        unmarked_neighbors -= self.mines

        # Add the new sentence to the knowledge base
        if unmarked_neighbors:
            new_sentence = Sentence(unmarked_neighbors, adjusted_count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        # Infer new knowledge
        self.infer_knowledge()

    def get_unmarked_neighbors(self, cell):
        """
        Returns all neighbors of the given cell that are not marked as safe or mines.
        """
        i, j = cell
        neighbors = set(itertools.product(range(i - 1, i + 2), range(j - 1, j + 2)))
        neighbors.discard(cell)
        neighbors = {neighbor for neighbor in neighbors
                     if 0 <= neighbor[0] < self.height and 0 <= neighbor[1] < self.width and neighbor not in self.moves_made and neighbor not in self.safes and neighbor not in self.mines}
        return neighbors

    def infer_knowledge(self):
        """
        Applies inference rules to update knowledge base and deduce new safe cells or mines.
        """
        made_progress = True
        while made_progress:
            made_progress = False
            safes_to_mark = set()
            mines_to_mark = set()

            for sentence in self.knowledge:
                if len(sentence.cells) == 0:
                    continue
                if len(sentence.cells) == sentence.count:
                    mines_to_mark.update(sentence.cells)
                elif sentence.count == 0:
                    safes_to_mark.update(sentence.cells)

            for safe in safes_to_mark:
                if safe not in self.safes:
                    self.mark_safe(safe)
                    made_progress = True
            for mine in mines_to_mark:
                if mine not in self.mines:
                    self.mark_mine(mine)
                    made_progress = True

            # Combining sentences
            new_sentences = []
            for s1, s2 in itertools.combinations(self.knowledge, 2):
                if s1.cells.issubset(s2.cells) and s2.count > s1.count:
                    new_cells = s2.cells - s1.cells
                    new_count = s2.count - s1.count
                    if new_cells:
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge:
                            new_sentences.append(new_sentence)
                            made_progress = True

            if new_sentences:
                self.knowledge.extend(new_sentences)

            # Remove empty sentences
            self.knowledge = [sentence for sentence in self.knowledge if len(sentence.cells) > 0]

    def make_safe_move(self):
        """
        Returns a safe move that has not been made yet, if possible.
        """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return random.choice(list(safe_moves))
        return None

    def make_random_move(self):
        """
        Returns a random move that has not been made yet, if possible.
        """
        all_moves = set(itertools.product(range(self.height), range(self.width)))
        possible_moves = all_moves - self.moves_made - self.safes - self.mines
        if possible_moves:
            return random.choice(list(possible_moves))
        return None
