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

    def __init__(self, height, width, states, rules, name=""):
        """
        Constructor.

        Args:
            height: Height of lattice.
            width: Width of lattice.
            states: Number of automaton states.
            rules: CMR rules.
        """
        self._rules = [[int(x) for x in rule] for rule in rules]
        super(CMRNeumann, self).__init__(height, width, states, name)

    @classmethod
    def _valid_rule(cls, rule):
        """
        Returns this ruse is valid rule of this automaton.

        Returns:
            True if valid, False otherwise
        """
        if len(rule) == 11:
            return True
        return False

    def _right_rule(self, hood, rule):
        """
        If rule is right rule.

        Args:
            hood: Cell neighborhood.
            rule: CMR rule.

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
            row: Row.
            col: Column.

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
            offset: How many generations we want to move.
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
                int(templ['rows']) > 1 
                and int(templ['cols']) > 1
                and templ['hood'] == 'von_neumann'
                and templ['rule_type']
                and templ['origin']
                and templ['rules']
               ):
                return True
        except KeyError:
            pass
        return False

    @classmethod
    def get_instance(cls, templ, args, config):
        """
        Get configured instance of automaton.
        """
        # We try to get number of rows
        if args.rows:
            rows = args.rows
        else:
            rows = templ['rows']
        # Number of cols
        if args.cols:
            cols = args.cols
        else:
            cols = templ['cols']
        instance = cls(int(rows), int(cols), templ['states'],
                       templ['rules'], templ['name'])
        # We need to flip lattice for lattice to be
        # properly oriented
        instance._copy(templ['origin'])
        return instance
