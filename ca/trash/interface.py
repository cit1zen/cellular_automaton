"""
Loader interface.
"""


class LoaderInterface(object):
    """
    Interface for loaders.
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
