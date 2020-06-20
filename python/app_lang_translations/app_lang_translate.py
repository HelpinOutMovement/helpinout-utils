# Script to convert XLSX language translation files for HelpinOUt to the
# Android XML format
#
# Usage:
#     python app_lang_translate.py <langfile.xlsx>
# where:
#     lang_file.xlsx: language translations file in HelpinOut format
#
# Try:
#     python app_lang_translate.py --help
# for a detailed help message
import argparse
import logging
import sys

from  constants import (
    ENGLISH_COL, JSON_LANG_ROW, JSON_ZIP_FILE_NAME, LOG_LEVELS, START_COL,
    START_ROW, XML_CDATA_COL, XML_KEY_COL, XML_LANG_ROW, XML_TRANS_COL,
    XML_ZIP_FILE_NAME
)
from utils import AppLangTranslate

COLS = '{},0'.format( START_COL )
ROWS = '{},0'.format( START_ROW )

LANG_ROWS = '{},{}'.format( JSON_LANG_ROW, XML_LANG_ROW )

FMT_JSON = 'json'
FMT_XML = 'xml'
OUTPUT_FMTS = [FMT_JSON, FMT_XML]

EXIT_SUCCESS = 0
EXIT_FAILURE_MISSING_ARG = 1
EXIT_FAILURE_RUNTIME_ERROR = 2

def _parse_command_line():
    parser = argparse.ArgumentParser(
        description='Convert language translation files from XLSX to '
        'JSON (iOS), and XML (Android) formats. By default, one JSON, and '
        'one XML file is produced for each langiage column. The JSON files '
        'are written directly to the current directory, and XML files '
        'are written inside a sub-directory. By default, a .zip file of all '
        'JSON files, and all XML directories is produced.\n'
        'Command-line options can override many default settngs.'
    )

    parser.add_argument(
        '-o', '--out', default=','.join( OUTPUT_FMTS ),
        help='Comma-separated list of output format(s) from "{}". '
        'Default is "{}"'.format( OUTPUT_FMTS, ','.join( OUTPUT_FMTS ) )
    )

    parser.add_argument(
        '-f', '--filesystem', default=False, action='store_true',
        help='If specified, output directories and files are written directly '
        'to the filesystem. else to a .zip file. Default is to write to zip '
        'file'
    )

    parser.add_argument(
        '-c', '--cols', default=COLS,
        help='<min_col>,<max_col>: if <max_col>  is zero it is set to the '
        'last column. Default is "{}"'.format( COLS )
    )

    parser.add_argument(
        '-r', '--rows', default=ROWS,
        help='<min_row>,<max_row>: if <max_row>  is zero it is set to the '
        'last row. Default is "{}"'.format( ROWS )
    )

    parser.add_argument(
        '--level', choices=LOG_LEVELS,
        help='Logging level in library. Default is "ERROR"'
    )

    parser.add_argument(
        '--lang_rows', default=LANG_ROWS,
        help='Rows for language codes for JSON (iOS), and XML (Android).Used '
        'in naming the output file. Default is "{}"'.format( LANG_ROWS )
    )

    parser.add_argument(
        '-e', '--english_col', type=int, default=ENGLISH_COL,
        help='Column number for English. Relevant only for JSON (iOS) files'
        'Default is "{}"'.format( ENGLISH_COL )
    )

    parser.add_argument(
        '--cdata_col', default=XML_CDATA_COL, type=int,
        help='Column for XML (Android) CDATA column. Default is "{}"'.format(
            XML_CDATA_COL
        )
    )

    parser.add_argument(
        '--key_col', default=XML_KEY_COL, type=int,
        help='Column for XML (Android) keys Default is "{}"'.format(
            XML_KEY_COL
        )
    )

    parser.add_argument(
        '--trans_col', default=XML_TRANS_COL, type=int,
        help='Column for XML (Android) translatable flag column '
        'Default is "{}"'.format( XML_TRANS_COL )
    )

    parser.add_argument(
        '--stop_on_err', default=False, action='store_true',
        help='Stop is there is an intermediate error. Default is to continue'
        ' processing'
    )

    parser.add_argument(
        '--continue_on_null', default=False, action='store_true',
        help='Continue processing a language column even if a blank entry is '
        'encountered. Needed as the Helpinout Excel has blank linpes at the '
        'bottom. Defaultis to stop processing when a blank entry is '
        'encountered.'
    )

    return parser.parse_known_args()

def main():
    args, files = _parse_command_line()

    try:
        start_row, end_row = map( int, args.rows.split( ',' ) )
    except ValueError:
        msg = 'The argument to --rows should be a comma-separated list: '
        '<<min_row>,<max_row>.It is "{}"'.format( args.rows )
        print( msg, file=sys.stderr )

    try:
        start_col, end_col = map( int, args.cols.split( ',' ) )
    except ValueError:
        msg = 'The argument to --cols should be a comma-separated list: '
        '<<min_col>,<max_col>.It is "{}"'.format( args.cols )
        print( msg, file=sys.stderr )

    try:
        json_lang_row, xml_lang_row = map( int, args.lang_rows.split( ',' ) )
    except ValueError:
        msg = 'The argument to --cols should be a comma-separated list: '
        '<json_lang_row>,<xml_lang_row>.It is "{}"'.format( args.lang_rows )
        print( msg, file=sys.stderr )

    if len( files ) == 0:
        print(
            'Need exactly one argument: path to .xlsx file of language '
            'translataions tobe converted to XML', file=sys.stderr
        )

        exit( EXIT_FAILURE_MISSING_ARG )
    elif len( files ) > 1:
        print(
            'Ignoring all arguments agter the first,"{}"',format( file )
        )

    try:
        app_lang_translate = AppLangTranslate(
            files[0], start_col=start_col, end_col=end_col,
            start_row=start_row, end_row=end_row, json_lang_row=json_lang_row,
            xml_lang_row=xml_lang_row, english_col=args.english_col,
            xml_cdata_col=args.cdata_col, xml_key_col=args.key_col,
            xml_trans_col=args.trans_col,
            stop_on_null=not args.continue_on_null,
            stop_on_err=args.stop_on_err, filesystem=args.filesystem
        )

        if args.level:
            app_lang_translate.set_log_level( args.level )

        if FMT_JSON in args.out:
            app_lang_translate.to_json()

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

        if FMT_XML in args.out:
            app_lang_translate.to_xml()

            if args.filesystem:
                logging.info(
                    'Wrote Android language translation files to local values* '
                    'directories'
                )
            else:
                logging.info(
                    'Wrote Android language translation files to "{}"'.format(
                        XML_ZIP_FILE_NAME
                    )
                )
    except Exception as e:
        print(
            'Processing failed. {}:{}'.format( e.__class__.__name__, e ),
            file=sys.stderr
        )
        exit( EXIT_FAILURE_RUNTIME_ERROR )

    exit( EXIT_SUCCESS )

if __name__ == "__main__":
    main()
