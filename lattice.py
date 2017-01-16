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

    def __init__(self, rows, cols, states):
        """
        Constructor.

        :param rows: Number of rows.
        :type rows: int
        :param cols: Number of columns.
        :type cols: int
        :param states: Number of states.
        :type states: int
        """
        self._lattice = [[0 for x in range(cols)]
                         for x in range(rows)]
        self._rows = rows
        self._cols = cols
        self._states = states

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

    def copy(self, template, resize=True):
        """
        Copies template into lattice.

        :param template: Lattice to be copied into our lattice.
        :type template: 2D list
        :param resize: Resize original lattice if neccesary.
        :type resize: boolean
        """
        row_size = len(template)
        col_size = 0
        # Checks states
        for row in range(len(template)):
            for col in range(len(template[row])):
                if template[row][col] >= self.states:
                    logger.error("Copy lattice with unknown states.")
                    return
            if len(template[row]) > col_size:
                col_size = len(template[row])
        # If template bigger than lattice
        if (row_size > self._rows or col_size > self._cols):
            # Resize lattice
            if resize:
                if row_size > self._rows:
                    self._rows = row_size
                if col_size > self._cols:
                    self._cols = col_size
                self._lattice = [[0 for x in range(self._rows)]
                                 for x in range(self._cols)]
            else:
                logger.error("Template bigger than lattice.")
                return
        else:
            self.reset()

        # Put template inside lattice
        for row in range(row_size):
            for col in range(col_size):
                self._lattice[self._rows - row_size + row][self._cols -
                                                           col_size + col] = int(template[row][col])

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

    def reset(self):
        """
        Resets lattice to default state.
        """
        self._lattice = [[0 for x in range(self._cols)]
                         for x in range(self._rows)]


class LatticeHistory(LatticeBasic):
    """
    Saves previus states of lattice.
    """

    def __init__(self, rows, cols, states):
        """
        Constructor.

        :param rows: Number of rows.
        :type rows: int
        :param cols: Number of columns.
        :type cols: int
        :param states: Number of states.
        :type states: int
        """
        super().__init__(rows, cols, states)
        self._history = []
        # In case we go back and create new branch of history
        # we need to remove old one
        self._hist_index = 0

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

    def current_save(self):
        """
        Returns current history index.
        """
        return self._hist_index

    def load(self, index):
        """
        Loads save from history.

        :param index: Index of saved state.
        :type index: int
        """
        if index < self.save_count():
            self._hist_index = index
            self._lattice = copy.deepcopy(self._history[index])
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
        self._hist_index = 0
        self._history = []
        super().reset()


class Lattice(LatticeHistory):
    """
    1D or 2D lattice of cells.

     0 1 2 3 4
    0
    1    N
    2  W C E
    3    S
    4
    """
