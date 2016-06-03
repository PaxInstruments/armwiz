#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  █████╗ ██████╗ ███╗   ███╗██╗    ██╗██╗███████╗
# ██╔══██╗██╔══██╗████╗ ████║██║    ██║██║╚══███╔╝
# ███████║██████╔╝██╔████╔██║██║ █╗ ██║██║  ███╔╝
# ██╔══██║██╔══██╗██║╚██╔╝██║██║███╗██║██║ ███╔╝
# ██║  ██║██║  ██║██║ ╚═╝ ██║╚███╔███╔╝██║███████╗
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝╚══════╝
#                               by Pax Instruments

## Standard Python header information
__author__ = "Charles Edward Pax"
__copyright__ = "Copyright 2016, Pax Instruments LLC"
__date__ = "2016"
__credits__ = ["Charles Pax"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Charles Pax"
__email__ = "charles.pax@gmail.com"
__status__ = "Development"

import argparse

def parseArguments():
    """Parses command line arguments and returns ArgumentParser object."""
    parser = argparse.ArgumentParser(
        description='Generate a template embedded ARM project.',
        epilog="armwiz {}".format(__date__))
    parser.add_argument('-p','--projectname',
        help='Specify project name via -p <projectname>',
        metavar="<projectname>",
        default='armwizProject',
        required=False)
    parser.add_argument('-t','--targetname',
        help='Specify target microcontroller or processor via -t <targetname>',
        metavar="<targetname>",
        default=[],
        action="append",
        required=False)
    parser.add_argument('-e','--examplename',
        help='Specify which examples to copy via -e <examplename>',
        metavar="<examplename>",
        default=['blinky'],
        action="append",
        required=False)
    parser.add_argument('-l','--libraryname',
        help='Specify a library to include via -l <libraryname>',
        metavar="<libraryname>",
        default=[],
        action="append",
        required=False)
    parser.add_argument('-L',
        help='List all libraries available to -l <libraryname> and exit.',
        action="store_true",
        required=False)
    parser.add_argument('-T',
        help='List all targets available to -t <targetname> and exit',
        action="store_true",
        required=False)
    parser.add_argument('-E',
        help='List all examples available to -e <examplename> and exit',
        action="store_true",
        required=False)
    parser.add_argument('-c','--configfile',
        help='Specify a configuration file via -t <config file name>',
        default='armwiz.config',
        metavar="<config file name>",
        required=False)
    parser.add_argument('-o','--output',
        help='Target location -o <target location>',
        default='./',
        metavar="<target location>",
        required=False)
    parser.add_argument('-n','--no_header',
        help='Print the wizard',
        default=False,
        action="store_true",
        required=False)
    parser.add_argument('-g','--git',
        help='Initialize project as a git repository. Default is True. Ignored if git is not present.',
        default=True,
        action="store_true",
        required=False)
    parser.add_argument('-v','--verbose',
        help='Print extra information to the terminal',
        action="store_true",
        required=False)
    parser.add_argument('-q','--quite',
        help='Suppress terminal message as best we can',
        action="store_true",
        required=False)
    parser.add_argument('--version',
        version='%(prog)s {version}'.format(version=__version__),
        action='version')
    return parser

def main():
    pass

if __name__ == "__main__":
    main()
