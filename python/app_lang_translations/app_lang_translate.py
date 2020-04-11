# Script toconvert XLSX language translation files for HelpinOUt to the
# Android XML format
#
# Usage:
#     python app_lang_translate.py <langfile.xlsx>
# where:
#     lang_file.xlsx: language translations file in HelpinOut format
#
# Try:
#     python app_lang_translate.py --hel
# for a detailed help message
import argparse
import sys

from  constants import LANG_ROW, LOG_LEVELS, START_COL, START_ROW
from utils import AppLangTranslate

COLS = '{},0'.format( START_COL )
ROWS = '{},0'.format( START_ROW )

EXIT_SUCCESS = 0
EXIT_FAILURE_MISSING_ARG = 1
EXIT_FAILURE_RUNTIME_ERROR = 2

def _parse_command_line():
    parser = argparse.ArgumentParser(
        description='Convert language translation files from XLSX to '
        'Android app XML'
    )

    parser.add_argument(
        '-c', '--cols', default=COLS,
        help='<min_col>,<max_col>: if <max_col>  is zero it is set to the '
        'last column. Default "{}"'.format( COLS )
    )

    parser.add_argument(
        '-r', '--rows', default=ROWS,
        help='<min_row>,<max_row>: if <max_row>  is zero it is set to the '
        'last row. Default "{}"'.format( ROWS )
    )

    parser.add_argument(
        '-l','--lang_row', default=LANG_ROW,
        help='Row for name of language un Enflish.Used in naming the output '
        'file. Default "{}"'.format( LANG_ROW )
    )

    parser.add_argument(
        '--level', choices=LOG_LEVELS,
        help='Logging level in library. Default "ERROR"'
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
            start_row=start_row, end_row=end_row, lang_row=args.lang_row,
            stop_on_null=not args.continue_on_null,
            stop_on_err=args.stop_on_err
        )

        if args.level:
            app_lang_translate.set_log_level( args.level )

        app_lang_translate.to_xml()
    except Exception as e:
        print(
            'Processing failed. {}:{}'.format( e.__class__.__name__, e )
        )
        exit( EXIT_FAILURE_RUNTIME_ERROR )

    exit( EXIT_SUCCESS )

if __name__ == "__main__":
    main()
