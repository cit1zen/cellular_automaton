#!/usr/bin/env python3

import logging

logger = logging.getLogger(__name__)


def Lattice():
    """
    1D or 2D lattice of cells.

     0 1 2 3 4
    0
    1    N
    2  W C E
    3    S
    4
    """

    def __init__(self, rows, cols, default_state=0):
        """
        Constructor.

        :param rows: Number of rows.
        :type rows: int
        :param cols: Number of columns.
        :type cols: int
        :param default_state: Begining state of cells.
        :type default_state: int
        """
        self._lattice = [[default_state for x in range(cols)]
                         for x in range(rows)]

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
        return [self._get_cell(row - 1, col),
                self._get_cell(row, col - 1),
                self._get_cell(row, col),
                self._get_cell(row, col + 1),
                self._get_cell(row + 1, col)]

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
