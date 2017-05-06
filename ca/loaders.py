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
        parser.add_argument('--json', nargs='+', default=[],
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
                # HACK
                # so it doesn't matter how rows is writter
                # example: rows, Rows, ROWS
                data = json.loads(f.read().lower())
                try:
                    templ.append({'rows': int(data['rows']),
                                  'cols': int(data['cols']),
                                  'rule_type': 'CMR',
                                  'rules': data['rules'],
                                  'hood': data['hood'],
                                  'name': name,
                                  'states': int(data['states'])
                                  }
                                )
                except IndexError:
                    continue
                if 'origin' in data:
                    templ[-1]['origin'] = data['origin']
                else:
                    templ[-1]['origin'] = [[1]]
        return templ
