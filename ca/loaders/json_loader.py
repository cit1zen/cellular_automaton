"""
Load automaton from JSON file.
"""

import json


class JSONLoader(object):
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
                            help=("JSON files with automaton "
                                  "rules and configuration"))

    @classmethod
    def load(cls, args, config):
        """
        Load configuration.

        Args:
            args - Parsed CMD arguments.
            config - Configuration file.
        """
        templ = []
        for name in args.json:
            with open(name) as f: 
                data = json.load(f)
                try:
                    templ.append({'rows': data['ROWS'],
                                  'cols': data['COLS'],
                                  'rule_type': 'CMR',
                                  'rules': data['RULES'],
                                  'states': data['STATES'],
                                  'origin': data['ORIGIN']}
                                )
                except:
                    pass
        return templ
