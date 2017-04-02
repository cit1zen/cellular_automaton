"""
Cellular automaton based on conditionally matching rules.

CMR coding:
SCSCSCSCS
S = State
A = Automaton
    * 0  cell_state >= condition_state
    * 1  cell_state <= condition_state
    * 2  cell_state == condition_state
    * 3  cell_state != condition_state
"""

import logging

from ca.lattice import Lattice

LOG = logging.getLogger(__name__)


class CMRNeumann(Lattice):
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
        self._states = states
        self._rules = [self._parse_rule(x) for x in rules]
        super(self.__class__, self).__init__(height, width, infinite=infinite)

    @classmethod
    def add_args(cls, parser):
        """
        Add module specific args.

        Args:
            parser - ArgumentParser.
        """
        parser.add_argument('--states', type=int,
                            help="number of automaton states")
        parser.add_argument('--cmr-rules', nargs='+',
                            help="CMR rules")
        super(CMRNeumann, self).add_args(parser)

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
            if args and args.cmr_rules:
                rules = [x for x in args.cmr_rules if cls._valid_rule(x)]
            else:
                rules = [x for x in config.get(automaton, rules).split(',')
                         if cls._valid_rule(x)]
            return cls(args.height if args and args.height
                       else config.get('lattice', 'height'),
                       args.width if args and args.width
                       else config.get('lattice', 'width'),
                       args.states if args and args.states
                       else config.get('automaton', 'states'),
                       rules)
        except (ValueError, AttributeError):
            LOG.exception("Unable to configure {} class"
                          .format(cls.__name__))
            raise

    @classmethod
    def _valid_rule(cls, rule):
        """
        # TODO
        """
        # TODO what if 2 digits states
        if len(rule.count('|')) == 10:
            return True
        return False

    def _parse_rule(self, rule):
        """
        Parse rule from string.

        Args:
            rule - Rule in form of string.

        Returns:
            Parsed rule.
        """
        parsed = [int(x) for x in rule.split('|')]
        if len(parsed) == 11:
            return parsed
        else:
            # TODO exception
            raise AttributeError('Invalid CMR rule {}'.format(rule))

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
        return [self.get_cell(row - 1, col),
                self.get_cell(row, col - 1),
                self.get_cell(row, col),
                self.get_cell(row, col + 1),
                self.get_cell(row + 1, col)]

    def _next_gen(self):
        """
        Next generation of automaton.
        """
        LOG.info('Next generation of automaton')
        for x in len(self._lat[0]):
            for y in len(self._lat[0][0]):
                hood = self._hood(x, y)
                for rule in self._rules:
                    if self._right_rule(hood, rule):
                        self.set(x, y, rule[8])
                        break

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
                    self._next_gen()
                self._gen += 1
            LOG.debug("Moved forward, current gen is {}"
                      .format(self._gen))
        # Back
        # Moving into the past
        elif offset < 0 and offset + self._gen != -1:
            super(self.__class__, self).move(offset)
