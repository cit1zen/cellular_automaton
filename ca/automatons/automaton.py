"""
Base class of provided automatons.
"""

import copy
import logging

LOG = logging.getLogger(__name__)


class Automaton():
    """
    Lattice for cellular automatons.
    """

    def __init__(self, height, width, states, infinite=True):
        """
        Constructor.

        Args:
            height - Height of lattice.
            width - Width of lattice.
            infinite - If lattice is "infinite".
        """
        LOG.info('Creating {}finite {}x{} lattice'
                 .format('in' if infinite else '',
                         height, width))
        self._lat = [[[0 for x in range(width)] for y in range(height)]]
        # Current generation of cellular
        self._gen = 0
        self._inf = infinite
        self._states = states

    def proportions(self):
        """
        Get proportions of lattice.

        Returns:
            List.
        """
        # TODO
        return [len(_lat), len(_lat[0])]

    def set(self, row, col, value):
        """
        Set value of cell.

        Args:
            row - Row.
            col - Column.
            value - New value of cell.
        """
        LOG.debug('Setting value of cell {}x{} to {}'
                  .format(row, col, value))
        self._lat[self._gen + 1][row][col] = value

    def _set_next(self, row, col, value):
        """
        Set value of cell in next generation.

        Args:
            row - Row.
            col - Column.
            value - New value of cell.
        """
        self.next()
        self.set(row, col, value)
        self.back()

    def get(self, row, col):
        """
        Get value of cell.

        Args:
            row - Row.
            col - Column.

        Returns:
            Value of the cell.
        """
        LOG.debug('Getting value of cell {}x{}'
                  .format(row, col))
        try:
            return self._lat[self._gen][row][col]
        except IndexError:
            if self._inf:
                return 0
            else:
                raise

    def get_generation(self):
        """
        Get current generation of CA.
        """
        return self._gen

    def move(self, offset):
        """
        Move between generations.

        Args:
            offset - How many generations we want to move.
        """
        # Forward
        if offset > 0:
            # Moving into the future
            for off in range(1, offset + 1):
                if len(self._lat) < self._get + 1:
                    self._lat.append(copy.deepcopy(self._lat[self._gen]))
                self._gen += 1
            LOG.debug("Moved forward, current gen is {}"
                      .format(self._gen))
        # Back
        # Moving into the past
        elif offset < 0 and offset + self._gen != -1:
            self._gen += offset
            LOG.debug("Moved back, current gen is {}"
                      .format(self._gen))

    def next(self):
        """
        Move forward in history.
        """
        self.move(1)

    def back(self):
        """
        Move back in history.
        """
        self.move(-1)

    @classmethod
    def is_right(cls, templ):
        """
        If template belongs to this class.

        Args:
            templ: Automaton template.

        Returns:
            True if yes, False otherwise.
        """
        LOG.warning('{} has not its own is_right method'
                    .format(cls.__name__))
        return False