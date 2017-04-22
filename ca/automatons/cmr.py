"""
Cellular automaton based on conditionally matching rules.

CMR coding:
SCSCSCSCS
S = State
C = Condition
    * 0  cell_state >= condition_state
    * 1  cell_state <= condition_state
    * 2  cell_state == condition_state
    * 3  cell_state != condition_state
"""

import copy
import logging

from ca.automatons.automaton import Automaton

LOG = logging.getLogger(__name__)


class CMRNeumann(Automaton):
    """
    CMR automating with Von Neumann's neighborhood.
    """

    def __init__(self, height, width, states, rules, infinite=True):
        """
        Constructor.

        Args:
            height - Height of lattice.
            width - Width of lattice.
            states - Number of automaton states.
            rules - CMR rules.
            infinite - If lattice is "infinite".
        """
        self._rules = rules
        super(self.__class__, self).__init__(height, width, states,
                                             infinite=infinite)

    @classmethod
    def _valid_rule(cls, rule):
        """
        # TODO
        """
        if len(rule) == 11:
            return True
        return False

    def _right_rule(self, hood, rule):
        """
        If rule is right rule.

        Args:
            hood - Cell neighborhood.
            rule - CMR rule.

        Returns:
            True or False.
        """
        # TODO
        index = 0
        for state in hood:
            # cell_state >= condition_state
            if rule[index + 1] == 0:
                if state < rule[index]:
                    return False
            # cell_state <= condition_state
            elif rule[index + 1] == 1:
                if state > rule[index]:
                    return False
            # cell_state == condition_state
            elif rule[index + 1] == 2:
                if state != rule[index]:
                    return False
            # cell_state != condition_state
            elif rule[index + 1] == 3:
                if state == rule[index]:
                    return False
            else:
                # TODO
                raise AttributeError('Unknown condition in {}'
                                     .format(rule))
            index += 2
        return True

    def _hood(self, row, col):
        """
        Get Von Neumann's neighborhood of the cell.

        Args:
            row - Row.
            col - Column.

        Returns:
            Von Neumann's neighborhood.
        """
        return [self.get(row - 1, col),
                self.get(row, col - 1),
                self.get(row, col),
                self.get(row, col + 1),
                self.get(row + 1, col)]

    def _next_gen(self):
        """
        Next generation of automaton.
        """
        LOG.info('Next generation of automaton')
        # Append new lattice
        self._lat.append(copy.deepcopy(self._lat[self._gen]))
        # Do CA magic
        for x in range(len(self._lat[0])):
            for y in range(len(self._lat[0][0])):
                hood = self._hood(x, y)
                for rule in self._rules:
                    if self._right_rule(hood, rule):
                        super().next()
                        self.set(x, y, rule[10])
                        super().back()
                        break

    def move(self, offset):
        """
        Move between generations.

        Args:
            offset - How many generations we want to move.
        """
        # Forward
        if offset > 0:
            for off in range(1, offset + 1):
                # New generation is needed
                if self._gen + 1 == len(self._lat) :
                    self._next_gen()
                self._gen += 1
            LOG.debug("Moved forward, current gen is {}"
                      .format(self._gen))
        # Back
        # Moving into the past
        elif offset < 0 and offset + self._gen != -1:
            super().move(offset)

    @classmethod
    def is_right(cls, templ):
        """
        If template belongs to this class.

        Args:
            templ: Automaton template.

        Returns:
            True if yes, False otherwise.
        """
        try:
            if (
                templ['rows'] > 1 
                and templ['cols'] > 1
                and templ['hood'] == 'vonneumann'
                and templ['rule_type']
                and templ['origin']
                and templ['rules']
               ):
                return True
        except KeyError:
            pass
        return False

    @classmethod
    def get_instance(cls, templ, args=None, config=None):
        """
        Get configured instance of automaton.
        """
        # We try to get number of rows
        rows = templ['rows'] if templ and 'rows' in templ else 0
        rows = (args.rows
                if (args
                    and args.rows
                    and args.rows > rows)
                else rows)
        try:
            if not (args and args.rows):
                rows = (int(config['ca']['rows'])
                        if int(config['ca']['rows']) > rows
                        else rows)
        except KeyError:
            pass
        # Number of cols
        cols = templ['cols'] if templ and 'cols' in templ else 0
        cols = (args.cols
                if (args
                    and args.cols
                    and args.cols > cols)
                else cols)
        try:
            if not (args and args.cols):
                cols = (int(config['ca']['cols'])
                        if int(config['ca']['cols']) > cols
                        else cols)
        except KeyError:
            pass
        instance = cls(rows, cols, templ['states'], templ['rules'])
        instance._origin(templ['origin'])
        print("AHOJ")
        return instance

    # TODO better name
    def _origin(self, lattice):
        """
        # TODO
        """
        # TODO rename to offset
        lat_row = int(-((len(self._lat[0])-len(lattice))/2))
        lat_col = int(-((len(self._lat[0][0])-len(lattice[0]))/2))
        for row in range(len(self._lat[0])):
            # Ski
            if lat_row + row < 0:
                continue
            # Finish
            if lat_row + row >= len(lattice):
                break 
            for col in range(len(self._lat[0][0])):
                print(col)
                # Skip
                if lat_col + col < 0:
                    continue
                if lat_col + col >= len(lattice[0]):
                    break
                self.set(row, col, lattice[lat_col + col]
                                          [lat_row + row])
