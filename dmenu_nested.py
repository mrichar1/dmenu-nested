#!/usr/bin/python

"""dmenu wrapper script that calls sub-menus based on JSON structure.

Dictionary keys are command names.
Values can be:
 - null : command name is called as-is (must be in your path).
 - text : this text is assumed to be command (+ args)
 - dictionary : a sub-menu to be displayed.

 Sub-menus can be nested repeatedly to any depth.

 Order of json should be preserved in the menu display."""


import json
from collections import OrderedDict
from subprocess import Popen, call, PIPE
from argparse import ArgumentParser, FileType


def show_menu(menus):
    """Recursive function to walk menus dict and call dmenu cmd/exec result."""
    proc = Popen(['dmenu'], stdin=PIPE, stdout=PIPE)
    choice, _ = proc.communicate('\n'.join(menus))
    choice = choice.strip()
    if choice:
        if isinstance(menus[choice], OrderedDict):
            # Sub-menu selected. Loop again
            show_menu(menus[choice])
        elif menus[choice]:
            # Specific command defined
            call(menus[choice].split())
        else:
            # Call the command title
            call([choice])


def parse_args():
    """Parse command-line arguments."""

    parser = ArgumentParser()
    parser.add_argument('-j', '--json', type=FileType(), required=True,
                        help='JSON menu config file.')

    args = parser.parse_args()
    return args


def main(args):
    """Define menu and call show_menu()"""

    jsonmenu = args.json.read()
    show_menu(json.JSONDecoder(object_pairs_hook=OrderedDict).decode(jsonmenu))


if __name__ == "__main__":
    main(parse_args())
