# Script to convert Android XML language file(s) to iOS JSON format.
# The Android XML files can be one of:
# 1. A single XML file in a sub-directory, e.g., values-mr/strings.xml, which
#    is the usual format
# 2. A .zip file with multiple XML files in a hierarchy as above, e.g., the
#    .zip file contains:
#         values-hi/strings.xml
#         values-mr/strings.xml
#         ...
#    This is the output format produced by app_lang_translate.py
# 3. A single XML file where the language name is directly in the filename,
#    e.g., mr.xml. This is just for convenience
#
# Multiple files can be specified on the command-line. For each input file,
# the output iOS JSON file is named <lang>.json, e.g., hi.json
#
# Usage:
#     python xmls2json.py mr.xml values-hi/strings.xml langs.zip
# with langs.zip containing:
#     values-or/strings.xml
#     values-kn/strings.xml
# would produce the output iOS JSON files, mr.json, hi.json, or.json, and
# kn.json. By default, these would be inside a .zip file, ios_languages.zip
#
import argparse
import logging
import sys

from constants import LOG_LEVELS, JSON_ZIP_FILE_NAME
from utils import XML2JSON

EXIT_SUCCESS = 0
EXIT_FAILURE_MISSING_ARG = 1
EXIT_FAILURE_RUNTIME_ERROR = 2

def _parse_command_line():
    parser = argparse.ArgumentParser(
        description='Parses Android XMLlanguage file(s) specified on the '
        'command line, and produces corresponding iOS JSON language files. '
        'By default, a .zip file of all JSON files is produced as output.'
    )

    parser.add_argument(
        '-f', '--filesystem', default=False, action='store_true',
        help='If specified, output directories and files are written directly '
        'to the filesystem. else to a .zip file. Default is to write to zip '
        'file'
    )

    parser.add_argument(
        '--level', choices=LOG_LEVELS,
        help='Logging level in library. Default is "ERROR"'
    )

    parser.add_argument(
        '--stop_on_err', default=False, action='store_true',
        help='Stop is there is an intermediate error. Default is to continue'
        ' processing'
    )

    return parser.parse_known_args()

def main():
    args, files = _parse_command_line()

    if len( files ) == 0:
        print(
            'Need at least one argument: an input Android language file to '
            'convert to iOS JSON format', file=sys.stderr
        )

        exit( EXIT_FAILURE_MISSING_ARG )

    try:
        xml2json = XML2JSON(
            files, stop_on_err=args.stop_on_err, filesystem=args.filesystem
        )

        if args.level:
            xml2json.set_log_level( args.level )

        xml2json.to_json()

        if args.filesystem:
            logging.info(
                'Wrote iOS language translation files to local files'
            )
        else:
            logging.info(
                'Wrote iOS language translation files to "{}"'.format(
                    JSON_ZIP_FILE_NAME
                )
            )
    except Exception as e:
        print(
            f'Processing failed for input file "{f}". '
            f'{e.__class__.__name__}:{e}', file=sys.stderr
            )

        exit( EXIT_FAILURE_RUNTIME_ERROR )

    exit( EXIT_SUCCESS )

if __name__ == "__main__":
    main()
