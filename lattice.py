#!/usr/bin/env python3

import copy
import logging

logger = logging.getLogger(__name__)


class LatticeBasic():
    """
    1D or 2D lattice of cells.

     0 1 2 3 4
    0
    1    N
    2  W C E
    3    S
    4
    """

    def __init__(self, rows, cols):
        """
        Constructor.

        :param rows: Number of rows.
        :type rows: int
        :param cols: Number of columns.
        :type cols: int
        :param default_state: Begining state of cells.
        :type default_state: int
        """
        self._lattice = [[0 for x in range(cols)]
                         for x in range(rows)]
        self._rows = rows
        self._cols = cols

    def set_cell(self, row, col, value):
        """
        Sets cell to value. If value out of range, nothing happens.

        :param row: Row.
        :type row: int
        :param col: Column.
        :type col: int
        :param value: New value/state of cell.
        :type value: int        
        """
        try:
            logger.debug("set_cell row {} col {} val {}".format(row, col,
                                                                value))
            self._lattice[row][col] = value
        except IndexError:
            logger.error("set_cell out of range")

    def get_cell(self, row, col):
        """
        Returns value of cell.

        :param row: Row.
        :type row: int
        :param col: Column.
        :type col: int
        :returns: Value/state of cell.
        :rtype: int or 0
        """
        try:
            logger.debug("get_cell row {} col {} ".format(row, col))
            return self._lattice[row][col]
        except IndexError:
            return 0

    def copy(self, template):
        """
        Copies template into lattice.

        :param template: Lattice to be copied into our lattice.
        :type template: list
        """
        try:
            temp_lattice = self._lattice
            for row in len(template):
                for col in len(template[row]):
                    temp_lattice = template[row][col]
            self._lattice = temp_lattice
        except IndexError:
            logger.error("template bigger than lattice")

    def neumann(self, row, col):
        """
        Returns von neumann's neighborhood.

        Order: N W C E S

        :param row: Row.
        :type row: int
        :param col: Column.
        :type col: int
        :returns: Von neumann's neighborhood.
        :rtype: list
        """
        return [self.get_cell(row - 1, col),
                self.get_cell(row, col - 1),
                self.get_cell(row, col),
                self.get_cell(row, col + 1),
                self.get_cell(row + 1, col)]

    def moore(self, row, col):
        """
        Returns moore's neighborhood.

        Order: NW N NE W C E SW S SE

        :param row: Row.
        :type row: int
        :param col: Column.
        :type col: int
        :returns: Moore's neighborhood.
        :rtype: list
        """
        hood = []
        for row_off in range(-1, 2):
            for col_off in range(-1, 2):
                hood.append(self.get_cell(row + row_off, col + col_off))
        return hood


class LatticeHistory(LatticeBasic):
    """
    Saves previus states of lattice.
    """

    def __init__(self, rows, cols):
        """
        Constructor.

        :param rows: Number of rows.
        :type rows: int
        :param cols: Number of columns.
        :type cols: int
        :param default_state: Begining state of cells.
        :type default_state: int
        """
        super().__init__(rows, cols)
        self._history = []
        # In case we go back and create new branch of history
        # we need to remove old one
        self._hist_index = 0
        self.save()

    def save(self):
        """
        Saves state of lattice.
        """
        self._hist_index += 1
        self._history = self._history[:self._hist_index]
        self._history.append(copy.deepcopy(self._lattice))
        logger.debug("Lattice saved.")

    def save_count(self):
        """
        Number of saved states of lattice.
        """
        return len(self._history)

    def load(self, index):
        """
        Loads save from history.

        :param index: Index of saved state.
        :type index: int
        """
        if index < self.save_count():
            self._hist_index = index
            self._lattice = self._history[index]
            logger.debug("Lattice loaded.")
        else:
            logger.warning("No such save.")

    def __iter__(self):
        """
        Iterator.
        """
        return self

    def next(self):
        """
        Saves lattice.
        """
        self.save()
        return self

    def get_cell(self, row, col, history=None):
        """
        Returns value of cell.

        :param row: Row.
        :type row: int
        :param col: Column.
        :type col: int
        :param history: Get state from saved state.
        :type history: int or None
        :returns: Value/state of cell.
        :rtype: int or 0
        """
        if history == None:
            return super().get_cell(row, col)
        else:
            if history < self.save_count():
                temp = self._lattice
                self._lattice = self._history[history]
                value = super().get_cell(row, col)
                self._lattice = temp
                return value
            else:
                logger.warning("No such save.")

    def neumann(self, row, col, history=None):
        """
        Returns von neumann's neighborhood.

        Order: N W C E S

        :param row: Row.
        :type row: int
        :param col: Column.
        :type col: int
        :param history: Get from saved state.
        :type history: int or None
        :returns: Von neumann's neighborhood.
        :rtype: list
        """
        if history == None:
            return super().neumann(row, col)
        else:
            if history < self.save_count():
                temp = self._lattice
                self._lattice = self._history[history]
                value = super().neumann(row, col)
                self._lattice = temp
                return value
            else:
                logger.warning("No such save.")

    def moore(self, row, col, history=None):
        """
        Returns moore's neighborhood.

        Order: NW N NE W C E SW S SE

        :param row: Row.
        :type row: int
        :param col: Column.
        :type col: int
        :param history: Get from saved state.
        :type history: int or None
        :returns: Moore's neighborhood.
        :rtype: list
        """
        if history == None:
            return super().moore(row, col)
        else:
            if history < self.save_count():
                temp = self._lattice
                self._lattice = self._history[history]
                value = super().moore(row, col)
                self._lattice = temp
                return value
            else:
                logger.warning("No such save.")

    def reset(self):
        """
        Reset lattice to default state and delete history.
        """
        self.load(0)
        self.save()


class LatticeFile(LatticeHistory):
    """
    Layer adds functions for loading and saving CA into files.
    """

    def __init__(self, rows, cols):
        """
        Constructor.

        :param rows: Number of rows.
        :type rows: int
        :param cols: Number of columns.
        :type cols: int
        :param default_state: Begining state of cells.
        :type default_state: int
        """
        super().__init__(rows, cols)

    def load_from_file(self, file_name, resize=False, delimiter=" "):
        """
        Loads lattice from file.

        :param file_name: Name of file.
        :type file_name: str
        :param resize: If CA schould be resized, if loaded lattice do not fit.
        :type resize: boolean
        :param delimiter: Delimiter used to split cells inside file.
        :type delimiter: str
        """
        with open(file_name, "r") as f:
            logger.debug("Loading lattice from {}".format(file_name))
            temp = [[y for y in x.split(delimiter) if not None] for x in f]
            rows = len(temp)
            cols = max([len(x) for x in temp])
            if rows <= self._rows and cols <= self._cols:
                self.reset()
                # Copy temp into center of lattice
                for row in range(rows):
                    for col in range(cols):
                        try:
                            self._lattice[
                                self._rows - rows + row][self._cols - cols + col] = int(temp[row][col])
                        except IndexError:
                            break
            else:
                logger.debug("Resize lattice")
                if resize:
                    # Create new lattice with good size
                    super().__init__(rows, cols)
                    # Copy temp lattice into CA
                    self.copy(temp)

    def save_to_file(self, file_name, delimiter=" "):
        """
        Saves lattice into file in form of text.

        :param file_name: Name of file.
        :type file_name: str
        :param delimiter: Delimiter used to split cells inside file.
        :type delimiter: str
        """
        with open(file_name, "w") as f:
            for row in self._rows:
                for col in self._cols:
                    f.write(str(col) + delimiter)
                f.write("\n")


class Lattice(LatticeFile):
    """
    1D or 2D lattice of cells.

     0 1 2 3 4
    0
    1    N
    2  W C E
    3    S
    4
    """
