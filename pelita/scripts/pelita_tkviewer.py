#!/usr/bin/env python3

import argparse

import pelita
from pelita.ui.tk_viewer import TkViewer


def geometry_string(s):
    """Get a X-style geometry definition and return a tuple.

    600x400 -> (600,400)
    """
    try:
        x_string, y_string = s.split('x')
        geometry = (int(x_string), int(y_string))
    except ValueError:
        msg = "%s is not a valid geometry specification" %s
        raise argparse.ArgumentTypeError(msg)
    return geometry

parser = argparse.ArgumentParser(description='Open a Tk viewer')
parser.add_argument('subscribe_sock', metavar="URL", type=str,
                    help='subscribe socket')
parser.add_argument('--controller-address', metavar="URL", type=str,
                    help='controller address')
parser.add_argument('--geometry', type=geometry_string,
                    help='geometry')
parser.add_argument('--delay', type=int,
                    help='delay')
parser.add_argument('--stop-after', type=int, metavar="N",
                    help='Stop after N rounds.')
parser._optionals = parser.add_argument_group('Options')
parser.add_argument('--version', help='show the version number and exit',
                    action='store_const', const=True)
parser.add_argument('--log', help='print debugging log information to'
                                  ' LOGFILE (default \'stderr\')',
                    metavar='LOGFILE', default=argparse.SUPPRESS, nargs='?')

def main():
    args = parser.parse_args()
    if args.version:
        if pelita._git_version:
            print("Pelita {} (git: {})".format(pelita.__version__, pelita._git_version))
        else:
            print("Pelita {}".format(pelita.__version__))

        sys.exit(0)

    try:
        pelita.utils.start_logging(args.log)
    except AttributeError:
        pass

    tkargs = {
        'address': args.subscribe_sock,
        'controller_address': args.controller_address,
        'geometry': args.geometry,
        'delay': args.delay,
        'stop_after': args.stop_after
    }
    v = TkViewer(**{k: v for k, v in list(tkargs.items()) if v is not None})
    v.run()

if __name__ == '__main__':
    main()
