#!/usr/bin/env python3

import logging

from lattice import Lattice

logger = logging.getLogger(__name__)


class Cmr(Lattice):
    """
    CMR based cellular automaton.

    CMR coding:
    * 0  cell_state >= condition_state
    * 1  cell_state <= condition_state
    * 2  cell_state == condition_state
    * 3  cell_state != condition_state

    Structure XAXAXAXAX where X is state and A is cmr condition
    """

    @staticmethod
    def add_arguments(parser):
        """
        Adds arguments specific for this class.

        :param parser: CMD argument parser.
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument("-r", "--rules", nargs="+", required=True,
                            help="Rule files")

    def __init__(self, rows, cols):
        """
        Constructor.

        :param rows: Number of rows.
        :type rows: int
        :param cols: Number of columns.
        :type cols: int
        """
        super().__init__(rows, cols)
        self._rules = []

    def rule_size(self):
        """
        Size of CMR rule.
        """
        # TODO change to more generic solution
        # If 1D
        if self._rows == 1 or self._cols == 1:
            return 3 * 2 + 1
        # If 2D
        else:
            return 5 * 2 + 1

    def add_rule(self, rule):
        """
        Add CMR rule to rules of automaton.

        :param rule: One CMR rule.
        :type rule: string or list
        """
        if len(rule) == self.rule_size():
            if isinstance(list) or isinstance(str):
                self._rules.append([int(x) for x in rule])
        else:
            logger.warning("Bad size of rule, rule not added")

    def clear_rules(self):
        """
        Removes all rules.
        """
        self._rules = []

    def rule_count(self):
        """
        Returns number of rules.
        """
        return len(self._rules)

    def remove_rule(self, index):
        """
        Remove rule from rules.

        :param index: Index of removed rule
        :type index: int
        """
        try:
            del self._rules[index]
        except IndexError:
            logger.warning("Deleting non-existent rule.")

    def get_rules(self):
        """
        Get all current rules.
        """
        return self._rules

    @staticmethod
    def _right_rule(hood, rule):
        """
        If this CMR rule is rule for hood.

        :param hood: Neighborhood.
        :type hood: list
        :param rule: CMR rule.
        :type rule: list
        """
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
                logger.error("Unknown condition.")
                return False
            index += 2
        return True

    def __iter__(self):
        """
        Iterator.
        """
        return self

    def next(self):
        """
        Next step of automaton. 
        """
        super().next()
        for row in self._rows:
            for col in self._cols:
                hood = self.neumann(row, col, -1)
                for rule in self._rules:
                    if self._right_rule(hood, rule):
                        self.set_cell(row, col, rule[-1])