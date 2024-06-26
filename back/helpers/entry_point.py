from argparse import ArgumentParser


def get_params():
    parser = ArgumentParser(description='ejecucion manual')
    parser.add_argument('params', type=str, metavar='<params>', help='')
    parser.add_argument('--debug', action="count", default=0, help='')
    parser.add_argument(
        '--function',
        type=str,
        metavar='<function>',
        help=''
    )
    args = parser.parse_args()

    return (
        args.params,
        None,
        args.debug,
        args.function,
    )
