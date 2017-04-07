"""
Automaton template loaders.
"""

import json


class LoaderInterface(object):
    """
    Loader interface.
    """
    @classmethod
    def add_args(cls, parser):
        """
        Add module specific arguments.

        Args:
            parser - ArgumentParser.
        """
        raise NotImplementedError("{} haven't implemented add_args"
                                  .format(cls.__name__))

    @classmethod
    def load(cls, args, config):
        """
        Load configuration.

        Args:
            args - Parsed CMD arguments.
            config - Configuration file.
        """
        raise NotImplementedError("{} haven't implemented load"
                                  .format(cls.__name__))


class JSONLoader(LoaderInterface):
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
                print(data)
                try:
                    templ.append({'rows': data['rows'],
                                  'cols': data['cols'],
                                  'rule_type': 'CMR',
                                  'rules': data['rules'],
                                  'states': data['states'],
                                  'hood': data['hood'],
                                  'origin': data['origin']}
                                )
                except IndexError:
                    pass
        return templ
