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


def main():
    """Define menu and call show_menu()"""

    jsonmenu = """\
{
    "xeyes": null,
    "terminals": {
        "xterm": "/usr/bin/xterm",
        "urxvt": null,
        "vi MOTD": "vi /etc/motd"
    },
    "web": {
        "firefox": null,
        "chromium": null
    },
    "mail": {
        "thunderbird": null,
        "evolution": null,
        "text-mail": {
            "pine": null,
            "mutt": null
        }
    }
}"""

    show_menu(json.JSONDecoder(object_pairs_hook=OrderedDict).decode(jsonmenu))


if __name__ == "__main__":
    main()
