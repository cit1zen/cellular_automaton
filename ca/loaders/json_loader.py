"""
Load automaton from JSON file.
"""

import json


class LoaderInterface(object):
    """
    Load automaton configuration from JSON file.
    """
    @classmethod
    def add_args(cls, parser):
        """
        Add module specific arguments.

        Args:
            parser - ArgumentParser.
        """
        parser.add_argument('--json', nargs='+',
                            help="JSON files with automatons' rules and configuration")

    @classmethod
    def load(cls, args, config):
        """
        Load configuration.

        Args:
            args - Parsed CMD arguments.
            config - Configuration file.
        """
