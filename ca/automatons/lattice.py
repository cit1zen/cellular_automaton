"""
Lattice of cells.
"""

import copy
import logging

LOG = logging.getLogger(__name__)


class Lattice(object):
    """
    Lattice for cellular automatons.
    """

    def __init__(self, height, width, infinite=True):
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
        Set value of a cell. Lattice where changes will be saved is
        plus one generation from lattice from where we get cell value.

        Args:
            row - Row.
            col - Column.
            value - New value of cell.
        """
        # If future has to be removed
        if self._gen < len(self._lat) - 1:
            LOG.debug('Removing invalid history')
            self._lat = self._lat[:self._gen]
        # We do not have future lattice, where we save
        # this new value
        if self._gen < len(self._lat) - 1:
            self._lat.append(copy.deepcopy(self._lat[self._gen]))
        LOG.debug('Setting value of cell {}x{} to {}'
                  .format(row, col, value))
        self._lat[self._gen + 1][row][col] = value

    def get(self, row, col):
        """
        Get value of the cell. Lattice from where we get
        value is one generation behind lattice where we save value.

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
    def add_args(cls, parser):
        """
        Add module specific args.

        Args:
            parser - ArgumentParser.
        """
        parser.add_argument('-h', '--height', type=int,
                            help="height of the lattice")
        parser.add_argument('-w', '--width', type=int,
                            help="width of the lattice")
        # parser.add_argument('--infinite', default=False, action='store_true')

    @classmethod
    def get_instance(cls, args=None, config=None):
        """
        Get configured instance of the class.

        Args:
            args - CMD arguments.
            config - Configuration from file.

        Returns:
            Configured class or None.
        """
        try:
            return cls(args.height if args and args.height
                       else config.get('lattice', 'height'),
                       args.width if args and args.width
                       else config.get('lattice', 'width'))
        except (ValueError, AttributeError):
            LOG.exception("Unable to configure {} class"
                          .format(cls.__name__))
            raise

