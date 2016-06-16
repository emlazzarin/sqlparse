#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Andi Albrecht, albrecht.andi@gmail.com
#
# This module is part of python-sqlparse and is released under
# the BSD License: http://www.opensource.org/licenses/bsd-license.php

import argparse
import sys

import sqlparse
from sqlparse.compat import PY2
from sqlparse.exceptions import SQLParseError

_CASE_CHOICES = ['upper', 'lower', 'capitalize']

# TODO: Add CLI Tests
# TODO: Simplify formatter by using argparse `type` arguments
parser = argparse.ArgumentParser(
    prog='sqlformat',
    description='Format FILE according to OPTIONS. Use "-" as FILE '
                'to read from stdin.',
    usage='%(prog)s  [OPTIONS] FILE, ...',
)

parser.add_argument('filename')

parser.add_argument(
    '-o', '--outfile',
    dest='outfile',
    metavar='FILE',
    help='write output to FILE (defaults to stdout)')

parser.add_argument(
    '--version',
    action='version',
    version=sqlparse.__version__)

group = parser.add_argument_group('Formatting Options')

group.add_argument(
    '-k', '--keywords',
    metavar='CHOICE',
    dest='keyword_case',
    choices=_CASE_CHOICES,
    help='change case of keywords, CHOICE is one of {0}'.format(
        ', '.join('"{0}"'.format(x) for x in _CASE_CHOICES)))

group.add_argument(
    '-i', '--identifiers',
    metavar='CHOICE',
    dest='identifier_case',
    choices=_CASE_CHOICES,
    help='change case of identifiers, CHOICE is one of {0}'.format(
        ', '.join('"{0}"'.format(x) for x in _CASE_CHOICES)))

group.add_argument(
    '-l', '--language',
    metavar='LANG',
    dest='output_format',
    choices=['python', 'php'],
    help='output a snippet in programming language LANG, '
         'choices are "python", "php"')

group.add_argument(
    '--strip-comments',
    dest='strip_comments',
    action='store_true',
    default=False,
    help='remove comments')

group.add_argument(
    '-r', '--reindent',
    dest='reindent',
    action='store_true',
    default=False,
    help='reindent statements')

group.add_argument(
    '--indent_width',
    dest='indent_width',
    default=2,
    type=int,
    help='indentation width (defaults to 2 spaces)')

group.add_argument(
    '-a', '--reindent_aligned',
    action='store_true',
    default=False,
    help='reindent statements to aligned format')

group.add_argument(
    '-s', '--use_space_around_operators',
    action='store_true',
    default=False,
    help='place spaces around mathematical operators')

group.add_argument(
    '--wrap_after',
    dest='wrap_after',
    default=0,
    type=int,
    help='Column after which lists should be wrapped')


def _error(msg):
    """Print msg and optionally exit with return code exit_."""
    sys.stderr.write('[ERROR] %s\n' % msg)


def main(args=None):
    args = parser.parse_args(args)

    if args.filename == '-':  # read from stdin
        data = sys.stdin.read()
    else:
        try:
            data = ''.join(open(args.filename).readlines())
        except IOError as e:
            _error('Failed to read %s: %s' % (args.filename, e))
            return 1

    if args.outfile:
        try:
            stream = open(args.outfile, 'w')
        except IOError as e:
            _error('Failed to open %s: %s' % (args.outfile, e))
            return 1
    else:
        stream = sys.stdout

    formatter_opts = vars(args)
    try:
        formatter_opts = sqlparse.formatter.validate_options(formatter_opts)
    except SQLParseError as e:
        _error('Invalid options: %s' % e)
        return 1

    s = sqlparse.format(data, **formatter_opts)
    if PY2:
        s = s.encode('utf-8', 'replace')
    stream.write(s)
    stream.flush()
    return 0


if __name__ == '__main__':
    sys.exit(main())
