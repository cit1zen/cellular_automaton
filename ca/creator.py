"""
Creates automaton from template.
"""

from ca.automatons.cmr import CMRNeumann


class Creator():


def get_automatons(args, config):
    """
    Create automatons using CMD params, configuration from config
    and loaded rule files.

    Args:
        args - CMD arguments.
        config - Configuration from file.
    """
    # Load automatons from rule files
    templates = []
    for l in LOADERS:
        for template in l.load(args, config):
            templates.append(template)
    # Get rules using templates
    auto = []
    for temp in templates:
        try:
            # 
            if (
                # If CMR based automaton
                temp['rule_type'] == "CMR" and
                # If Von Neumann neighborhood
                temp['rules'] and
                len(temp['rules'][0].count('|') == 10 and
                # If size is ok
                temp[]
               ):
                auto.append(CMRNeumann())
            else:
                # TODO
                LOG.warning("Unknown automaton.")
        except:
            # TODO
            LOG.exception("Bad configuration.")
