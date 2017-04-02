"""
Creates automaton from template.
"""
# TODO

from ca.automatons.cmr import CMRNeumann


def get_automatons(args, config, templ):
    """
    Create automatons using CMD params, configuration from config
    and loaded rule files.
    """
    # Load automatons from rule files

    # Get rules using templates
    return
    # auto = []
    # for temp in templ:
    #     try:
    #         # 
    #         if (
    #             # If CMR based automaton
    #             temp['rule_type'] == "CMR" and
    #             # If Von Neumann neighborhood
    #             temp['rules'] and
    #             len(temp['rules'][0].count('|') == 10 and
    #             # If size is ok
    #             temp[]
    #            ):
    #             auto.append(CMRNeumann())
    #         else:
    #             # TODO
    #             LOG.warning("Unknown automaton.")
    #     except:
    #         # TODO
    #         LOG.exception("Bad configuration.")


def is_CMRNeumann(args, config, templ):
    try:
        if (
            temp['rule_type'] == "CMR" and
            temp['rules'] and
            len(temp['rules'][0].count('|')) == 10
           ):
            return True
    except KeyError, IndexError:
        pass
    return False


def get_CMRNeumann(args, config, templ):
    rows = args.rows if args and args.rows
           else config.get('lattice', 'rows')
    cols = args.cols if args and args.cols
           else config.get('lattice', 'cols')
    # TODO
    if args.resize:
    states = templ['states']
    rules = temp['rules']
    auto = CMRNeumann(height, width, states, rules,
                      infinite=True)